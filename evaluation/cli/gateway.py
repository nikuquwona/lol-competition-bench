"""Unix-socket inference relay. Keep upstream credentials outside the CLI sandbox."""

import http.client
import json
import os
import re
import urllib.error
import urllib.request
import socketserver
import threading
from http.server import BaseHTTPRequestHandler
from pathlib import Path

ROUTES = {
    "/v1/messages": "/anthropic/v1/messages",
    "/v1/chat/completions": "/chat/completions",
    "/v1/responses": "/responses",
}
PARAMS = set(
    "model messages input instructions system tools tool_choice stream stream_options temperature top_p max_tokens max_output_tokens max_completion_tokens reasoning thinking stop stop_sequences text parallel_tool_calls store metadata include prompt_cache_key service_tier truncation context_management output_config".split()
)
REMOTE_TYPES = {
    "input_image",
    "input_file",
    "input_video",
    "image_url",
    "file",
    "document",
    "url",
    "computer",
    "mcp",
    "web_search",
    "web_fetch",
    "file_search",
    "code_interpreter",
    "container_reference",
    "item_reference",
}
MAX_BODY = 4 * 1024 * 1024
MAX_CALLS = 40


def validate(data, model):
    if not isinstance(data, dict) or data.get("model") != model or set(data) - PARAMS:
        raise ValueError(
            "model or request field denied: "
            + str(sorted(set(data) - PARAMS) if isinstance(data, dict) else [])
        )

    def tool(t):
        typ = t.get("type", "function")
        if typ == "namespace":
            return all(tool(x) for x in t.get("tools", []))
        return typ in ("function", "custom") and (
            t.get("name") or t.get("function", {}).get("name")
        )

    if not all(tool(t) for t in data.get("tools", [])):
        raise ValueError("hosted tool denied")

    def visit(value):
        if isinstance(value, dict):
            typ = value.get("type")
            if isinstance(typ, str) and (
                typ in REMOTE_TYPES
                or typ.startswith(("web_search", "web_fetch", "mcp_"))
            ):
                raise ValueError("remote content denied")
            if set(value) & {
                "file_id",
                "file_url",
                "image_url",
                "previous_response_id",
                "server_url",
            }:
                raise ValueError("remote reference denied")
            for v in value.values():
                visit(v)
        elif isinstance(value, list):
            for v in value:
                visit(v)

    # JSON Schema property names may describe local shell tools, not provider actions.
    for key in ("messages", "input", "tool_choice", "system"):
        visit(data.get(key))


def free_model(model):
    return bool(re.fullmatch(r"[A-Za-z0-9._-]+/[A-Za-z0-9._-]+:free", model))


def credential_name(mode):
    if mode == "openrouter-free":
        return (
            "OPENROUTER_API_KEY"
            if not os.getenv("OPEN_ROUTER_API_KEY") and os.getenv("OPENROUTER_API_KEY")
            else "OPEN_ROUTER_API_KEY"
        )
    return {"live": "DEEPSEEK_API_KEY", "vendor": "CURSOR_API_KEY"}.get(mode)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def stream_upstream(self, response, url):
        print(
            json.dumps(
                {"route": url, "model": self.server.model, "status": response.status}
            ),
            flush=True,
        )
        self.send_response(response.status)
        self.send_header(
            "Content-Type", response.headers.get("Content-Type", "application/json")
        )
        self.end_headers()
        while chunk := response.read1(65536):
            self.wfile.write(chunk)

    def do_POST(self):
        url = self.path.split("?", 1)[0]
        if url not in ROUTES or self.path not in (url, url + "?beta=true"):
            print("Denied inference path", url[:80], flush=True)
            return self.send_error(403)
        try:
            n = int(self.headers.get("Content-Length", 0))
            if not 0 < n <= MAX_BODY:
                raise ValueError("invalid size")
            body = json.loads(self.rfile.read(n))
            if isinstance(body, dict):
                body.pop(
                    "client_metadata", None
                )  # Codex tracing hints have no inference semantics.
            validate(body, self.server.model)
            with self.server.lock:
                if self.server.remaining <= 0:
                    return self.send_error(429)
                self.server.remaining -= 1
        except (ValueError, TypeError, AttributeError, RecursionError) as e:
            if self.server.fixture:
                print("Denied:", str(e)[:100], flush=True)
            return self.send_error(403, str(e)[:100])
        print(
            json.dumps({"route": url, "model": self.server.model, "stage": "accepted"}),
            flush=True,
        )
        if self.server.fixture:
            if __package__:
                from .fixture import respond
            else:  # The Docker gateway runs /opt/gateway.py as a standalone script.
                from fixture import respond

            return respond(self, url, body)
        if getattr(self.server, "openrouter_free", False):
            if not free_model(self.server.model):
                return self.send_error(403, "A pinned :free model is required")
            key = os.environ[credential_name("openrouter-free")]
            body["provider"] = {"max_price": {"prompt": 0, "completion": 0}}
            if url == "/v1/responses":
                body["store"] = False
            request = urllib.request.Request(
                "https://openrouter.ai/api" + url,
                data=json.dumps(body).encode(),
                headers={
                    "Authorization": "Bearer " + key,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01",
                },
            )
            try:
                response = urllib.request.build_opener(NoRedirect).open(
                    request, timeout=100
                )
            except urllib.error.HTTPError as exc:
                response = exc
            except (TimeoutError, OSError):
                return self.send_error(502, "OpenRouter connection failed")
            with response:
                self.stream_upstream(response, url)
            return
        conn = http.client.HTTPSConnection("api.deepseek.com", timeout=100)
        key = os.environ["DEEPSEEK_API_KEY"]
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
        if url == "/v1/messages":
            headers.update({"x-api-key": key, "anthropic-version": "2023-06-01"})
        try:
            conn.request("POST", ROUTES[url], json.dumps(body).encode(), headers)
            with conn.getresponse() as response:
                self.stream_upstream(response, url)
        finally:
            conn.close()


class Server(socketserver.ThreadingUnixStreamServer):
    daemon_threads = True


if __name__ == "__main__":
    import sys

    path = "/relay/inference"
    server = Server(path, Handler)
    Path(path).chmod(0o666)
    server.model = sys.argv[1]
    server.fixture = sys.argv[2] == "fixture"
    server.openrouter_free = sys.argv[2] == "openrouter-free"
    server.remaining = MAX_CALLS
    server.lock = threading.Lock()
    server.serve_forever()
