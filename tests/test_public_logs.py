import hashlib
from pathlib import Path
import tempfile
import unittest

from evaluation.cli.public_logs import stage_accounts, strip_accounts
from production.build import ROOT
from production.store import read, digest


class PublicLogTests(unittest.TestCase):
    def test_redact_listing_without_rewriting_regular_prose_or_original(self):
        content = b'{"msg":"total 2\\ndrwxr-xr-x@  2 example-user  staff  64 Jan 7 03:04 .\\n-rw-r--r--  1 root wheel 120 Jan 7 x; ordinary example-user staff"}\n'
        safe = strip_accounts(content)
        self.assertIn(b"[local-user]  [local-group]", safe)
        self.assertIn(b"root wheel", safe)
        self.assertIn(b"ordinary example-user staff", safe)
        self.assertEqual(safe.count(b"\n"), content.count(b"\n"))
        self.assertEqual(strip_accounts(safe), safe)
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            task = "example-g2-lobby"
            rel = Path("jobs") / task / "trajectory.jsonl"
            src = base / "source"
            (src / rel.parent).mkdir(parents=True)
            (src / "report.json").write_text("{}")
            (src / rel).write_bytes(content)
            clean = stage_accounts(src, base / "clean", [task], ["trajectory.jsonl"])
            self.assertEqual((src / rel).read_bytes(), content)
            self.assertEqual((clean / rel).read_bytes(), safe)
            proof = read(clean / "redactions.json")[rel.as_posix()]
            self.assertEqual(proof["public_sha256"], digest(clean / rel))
            self.assertEqual(proof["original_sha256"], digest(src / rel))
            self.assertNotIn("prior_public_sha256", proof)
            prior = base / "previous"
            (prior / rel.parent).mkdir(parents=True)
            (prior / rel).write_bytes(content)
            new = stage_accounts(src, base / "new", [task], ["trajectory.jsonl"], prior)
            self.assertEqual(
                read(new / "redactions.json")[rel.as_posix()]["prior_public_sha256"],
                digest(prior / rel),
            )

    def test_published_logs_and_transcripts_do_not_expose_personal_listing_accounts(
        self,
    ):
        examples = ROOT / "evaluation/examples"
        for name in ("trajectory.jsonl", "transcript.md", "stderr.txt"):
            for path in examples.rglob(name):
                b = path.read_bytes()
                self.assertEqual(
                    hashlib.sha256(strip_accounts(b)).digest(),
                    hashlib.sha256(b).digest(),
                    str(path),
                )
        migrated = 0
        for path in examples.glob("featured-five-*/report.json"):
            report = read(path)
            for t in report["trials"]:
                origin = t["origin"]
                if "prior_public_events_sha256" not in origin:
                    continue
                migrated += 1
                source = next(
                    s
                    for s in report["provenance"]["source_runs"]
                    if s["sha256"] == origin["source_report_sha256"]
                )
                key = f"jobs/{t['task']}/trajectory.jsonl"
                proof = read(path.parent / source["redactions"])[key]
                self.assertEqual(
                    proof["original_sha256"], origin["original_events_sha256"]
                )
                self.assertEqual(
                    proof["prior_public_sha256"], origin["prior_public_events_sha256"]
                )
                self.assertEqual(proof["public_sha256"], digest(path.parent / key))
                self.assertNotEqual(origin["prior_public_trial_id"], origin["trial_id"])
        self.assertGreaterEqual(migrated, 4)
