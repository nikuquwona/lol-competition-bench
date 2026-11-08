"""Unix-socket inference relay. Only this process holds the DeepSeek credential."""
import http.client
import json
import os
import socketserver
import threading
from http.server import BaseHTTPRequestHandler
from pathlib import Path

ROUTES = {"/v1/messages":"/anthropic/v1/messages","/v1/chat/completions":"/chat/completions","/v1/responses":"/responses"}
PARAMS = set("model messages input instructions system tools tool_choice stream stream_options temperature top_p max_tokens max_output_tokens max_completion_tokens reasoning thinking stop stop_sequences text parallel_tool_calls store metadata include prompt_cache_key service_tier truncation context_management output_config".split())
REMOTE_TYPES = {"input_image","input_file","input_video","image_url","file","document","url","computer","mcp","web_search","web_fetch","file_search","code_interpreter","container_reference","item_reference"}
MAX_BODY = 4*1024*1024
MAX_CALLS = 40


def validate(data, model):
    if not isinstance(data,dict) or data.get("model")!=model or set(data)-PARAMS:
        raise ValueError("model or request field denied")
    def tool(t):
        typ=t.get("type","function")
        if typ=="namespace":
            return all(tool(x) for x in t.get("tools",[]))
        return typ in ("function","custom") and (t.get("name") or t.get("function",{}).get("name"))
    if not all(tool(t) for t in data.get("tools",[])):
        raise ValueError("hosted tool denied")
    def visit(value):
        if isinstance(value,dict):
            typ=value.get("type")
            if isinstance(typ,str) and (typ in REMOTE_TYPES or typ.startswith(("web_search","web_fetch","mcp_"))):
                raise ValueError("remote content denied")
            if set(value) & {"file_id","file_url","image_url","previous_response_id","server_url"}:
                raise ValueError("remote reference denied")
            for v in value.values():
                visit(v)
        elif isinstance(value,list):
            for v in value:
                visit(v)
    # JSON Schema property names may describe local shell tools, not provider actions.
    for key in ("messages","input","tool_choice","system"):
        visit(data.get(key))


class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args):
        pass

    def do_POST(self):
        url=self.path.split("?",1)[0]
        if url not in ROUTES or self.path not in (url,url+"?beta=true"):
            return self.send_error(403)
        try:
            n=int(self.headers.get("Content-Length",0))
            if not 0<n<=MAX_BODY:
                raise ValueError("invalid size")
            body=json.loads(self.rfile.read(n))
            validate(body,self.server.model)
            with self.server.lock:
                if self.server.remaining<=0:
                    return self.send_error(429)
                self.server.remaining-=1
        except (ValueError,TypeError,AttributeError,RecursionError) as e:
            return self.send_error(403,str(e)[:100])
        if self.server.fixture:
            from fixture import respond
            return respond(self,url,body)
        conn=http.client.HTTPSConnection("api.deepseek.com",timeout=100)
        key=os.environ["DEEPSEEK_API_KEY"]
        headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"}
        if url=="/v1/messages":
            headers.update({"x-api-key":key,"anthropic-version":"2023-06-01"})
        try:
            conn.request("POST",ROUTES[url],json.dumps(body).encode(),headers)
            response=conn.getresponse()
            self.send_response(response.status)
            self.send_header("Content-Type",response.getheader("Content-Type","application/json"))
            self.end_headers()
            while chunk:=response.read1(65536):
                self.wfile.write(chunk)
        finally:
            conn.close()


class Server(socketserver.ThreadingUnixStreamServer):
    daemon_threads=True


if __name__=="__main__":
    import sys
    path="/relay/inference"
    server=Server(path,Handler)
    Path(path).chmod(0o666)
    server.model=sys.argv[1]
    server.fixture=sys.argv[2]=="fixture"
    server.remaining=MAX_CALLS
    server.lock=threading.Lock()
    server.serve_forever()
