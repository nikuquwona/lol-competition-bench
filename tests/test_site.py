from contextlib import closing
import csv
import io
import json
from http.client import HTTPConnection
from http.server import ThreadingHTTPServer
from pathlib import Path
import tempfile
import threading
import unittest
import zipfile

from evaluation.site import RunIndex, make_handler
from evaluation.suite import ROOT


class LocalSiteTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        parent = Path(temp.name)
        self.folder = parent / "runs" / "my-run"
        (self.folder / "jobs" / "example-game").mkdir(parents=True)
        job = self.folder / "jobs" / "example-game"
        (job / "trajectory.jsonl").write_text('{"type":"turn.completed"}\n')
        outside = parent / "snapshot.json"
        outside.write_text("should not be served")
        (job / "snapshot.json").symlink_to(outside)
        self.fixture = {
            "release": "missing-release",
            "mode": "live",
            "backend": "macos",
            "harness": "codex",
            "model": "some-model",
            "planned": ["example-game"],
            "trials": [
                {
                    "task": "example-game",
                    "phase": "lobby",
                    "status": "failed",
                    "reward": 0,
                    "error": "=bad",
                    "trajectory": {"files": {"snapshot": str(outside)}},
                }
            ],
            "summary": {"selected": 1, "scored": 0, "mean_reward": 0},
        }
        (self.folder / "report.json").write_text(json.dumps(self.fixture))
        server = ThreadingHTTPServer(
            ("127.0.0.1", 0),
            make_handler(RunIndex([("local", parent / "runs")], ROOT / "datasets")),
        )
        self.port = server.server_port
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.server_close)
        self.addCleanup(server.shutdown)

    def get(self, path, headers=None):
        with closing(HTTPConnection("127.0.0.1", self.port, timeout=10)) as conn:
            conn.request("GET", path, headers=headers or {})
            resp = conn.getresponse()
            return resp.status, resp.read()

    def test_navigation_downloads_and_boundary(self):
        status, data = self.get("/api/runs")
        self.assertEqual(status, 200)
        (run,) = json.loads(data)["runs"]
        base = "/api/runs/" + run["id"]
        self.assertEqual(json.loads(self.get(base + "/report.json")[1]), self.fixture)
        trial = base + "/trials/example-game"
        assets = json.loads(self.get(trial)[1])["artifacts"]
        self.assertEqual(set(assets), {"events"})
        self.assertIn(b"turn.completed", self.get(assets["events"])[1])
        self.assertEqual(self.get(trial + "/snapshot")[0], 404)
        self.assertEqual(self.get("/api/runs/../../.zshrc")[0], 404)
        self.assertEqual(self.get("/api/runs", {"Host": "external.example"})[0], 403)
        self.assertEqual(
            self.get("/api/runs", {"Origin": "https://external.example"})[0], 403
        )
        (csv_row,) = csv.DictReader(
            io.StringIO(self.get(base + "/trials.csv")[1].decode("utf-8-sig"))
        )
        self.assertEqual(csv_row["error"], "'=bad")
        with zipfile.ZipFile(io.BytesIO(self.get(base + "/bundle.zip")[1])) as z:
            self.assertEqual(
                set(z.namelist()), {"report.json", "jobs/example-game/trajectory.jsonl"}
            )
        ranks = json.loads(self.get("/api/leaderboard")[1])
        self.assertEqual(ranks["groups"], [])
        self.assertTrue(ranks["excluded"])
