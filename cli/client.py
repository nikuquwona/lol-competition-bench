"""Launch one native CLI inside an otherwise empty container."""
import json
import os
import subprocess
import sys
from pathlib import Path

BIN = {"claude":"claude", "codex":"codex","pi":"pi","kimi":"kimi","cursor":"cursor-agent"}
CURSOR_HOSTS = ("api2.cursor.sh","api5.cursor.sh","api2.cursor.com","api.cursor.com","api3.cursor.sh","api4.cursor.sh","agent.api5.cursor.sh")
BASE = "http://127.0.0.1:8787"


def command(name, model, prompt):
    if name == "claude":
        os.environ.update(ANTHROPIC_BASE_URL=BASE, ANTHROPIC_API_KEY="isolated", CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC="1",
                          ANTHROPIC_DEFAULT_HAIKU_MODEL=model, ANTHROPIC_DEFAULT_SONNET_MODEL=model, ANTHROPIC_DEFAULT_OPUS_MODEL=model)
        return ["claude","-p","--model",model,"--tools","Read,Write,Edit,Bash","--permission-mode","bypassPermissions","--no-session-persistence",prompt]
    if name == "codex":
        os.environ["BENCH_DUMMY_KEY"]="isolated"
        return ["codex","exec","--skip-git-repo-check","--ephemeral","--dangerously-bypass-approvals-and-sandbox","-m",model,
                "-c",'web_search="disabled"',"-c",'model_provider="bench"',"-c",'model_providers.bench.name="bench"',
                "-c",f'model_providers.bench.base_url="{BASE}/v1"',"-c",'model_providers.bench.wire_api="responses"',
                "-c",'model_providers.bench.env_key="BENCH_DUMMY_KEY"',prompt]
    if name == "pi":
        config=Path.home()/".pi/agent/models.json"
        config.parent.mkdir(parents=True,exist_ok=True)
        config.write_text(json.dumps({"providers":{"bench":{"baseUrl":BASE+"/v1","api":"openai-completions","apiKey":"isolated",
                                      "models":[{"id":model,"name":model,"contextWindow":128000,"maxTokens":8192}]}}}))
        return ["pi","--provider","bench","--model",model,"--no-session","--tools","read,bash,write,edit","--print",prompt]
    if name == "kimi":
        os.environ.update(KIMI_MODEL_NAME=model,KIMI_MODEL_API_KEY="isolated",KIMI_MODEL_BASE_URL=BASE+"/v1",
                          KIMI_MODEL_MAX_CONTEXT_SIZE="128000",KIMI_CODE_NO_AUTO_UPDATE="true",KIMI_DISABLE_TELEMETRY="true")
        return ["kimi","--prompt",prompt,"--output-format","stream-json","--yolo"]
    return ["cursor-agent","--yolo","--print","--output-format","stream-json","--model",model,"--",prompt]


def main():
    name, model = sys.argv[1:3]
    assert {p.name for p in Path("/sys/class/net").iterdir()} == {"lo"}
    if any(Path(p).exists() for p in ("/tests","/solution","/var/run/docker.sock","/app/.git")):
        raise RuntimeError("unexpected mount in CLI environment")
    subprocess.run([BIN[name],"--version"],check=True,timeout=25)
    if sys.argv[3:] == ["--check"]:
        cmd = command(name,model,"help probe")
        subprocess.run([BIN[name],"--help"],check=True,stdout=subprocess.DEVNULL,timeout=30)
        return
    relays=[]
    if name=="cursor":
        routes=[(f"127.0.0.{i+2}",443,f"cursor-{i}") for i in range(len(CURSOR_HOSTS))]
    else:
        routes=[("127.0.0.1",8787,"inference")]
    try:
        for ip,port,sock in routes:
            relays.append(subprocess.Popen(["socat",f"TCP4-LISTEN:{port},bind={ip},reuseaddr,fork",f"UNIX-CONNECT:/relay/{sock}"]))
        prompt=Path("/input/instruction.md").read_text()
        subprocess.run(command(name,model,prompt),check=True,timeout=540,stdin=subprocess.DEVNULL)
    finally:
        for proc in relays:
            proc.terminate()
            proc.wait()


if __name__=="__main__":
    main()
