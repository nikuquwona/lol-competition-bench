"""Fetch public source snapshots. Keep bulk/raw upstream files off the agent image."""
import hashlib
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache"
CACHE.mkdir(exist_ok=True)
VERSION = "20261108041551"
BASE = f"https://riftwise.gg/stats/{VERSION}/hub"
EVENTS = ["lpl-2026-regional-finals", "worlds-2026-play-in", "worlds-2026-main-event"]
TENCENT = "https://lpl.qq.com/web201612/data"
last = {}


def fetch(url):
    key = hashlib.sha256(url.encode()).hexdigest()
    path = CACHE / key
    if not path.exists():
        host = urlsplit(url).netloc
        time.sleep(max(0, last.get(host, 0) + 1.1 - time.monotonic()))
        request = Request(url, headers={"User-Agent": "LoL-Competition-Bench/0.1"})
        for attempt in range(3):
            try:
                with urlopen(request, timeout=30) as response:
                    body = response.read()
                break
            except OSError:
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)
        last[host] = time.monotonic()
        tmp = path.with_suffix(f".{os.getpid()}.tmp")
        tmp.write_bytes(body)
        tmp.replace(path)
        path.with_suffix(".meta").write_text(json.dumps(dict(url=url, fetched_at=datetime.now(timezone.utc).isoformat(), sha256=hashlib.sha256(body).hexdigest())))
    return path.read_bytes()


def obj(url):
    return json.loads(fetch(url))


def main():
    for event in EVENTS:
        doc = obj(f"{BASE}/event/{event}.json")
        for stage in doc["stages"]:
            for row in stage["series"]:
                if row.get("w") in (1, 2):
                    obj(f"{BASE}/game/{row['g']}.json")
        print(event, flush=True)
    obj(f"{BASE}/rating.json")
    for number in (237, 246):
        rows = obj(f"{TENCENT}/LOL_MATCH2_MATCH_HOMEPAGE_BMATCH_LIST_{number}.js")["msg"]
        for row in rows:
            if row["MatchStatus"] == "3" and (number == 246 or "2026-09-17" <= row["MatchDate"][:10] <= "2026-09-19"):
                fetch(f"{TENCENT}/LOL_MATCH_DETAIL_{row['bMatchId']}.js")


if __name__ == "__main__":
    main()
