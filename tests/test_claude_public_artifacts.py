import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from evaluation.cli.share_claude import stage


class PublishClaudeTests(unittest.TestCase):
    def test_original_is_preserved_and_identifiers_removed_from_public_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source"
            job = source / "jobs/a-lobby"
            job.mkdir(parents=True)
            (source / "report.json").write_text(
                json.dumps(
                    {
                        "harness": "claude",
                        "backend": "macos",
                        "planned": ["a-lobby"],
                        "summary": {"scored": 0},
                    }
                )
            )
            raw = b'{"session_id":"example-session","signature":"example-signature","cwd":"/private/tmp/lol-claude-a1b2c3/app"}\n'
            (job / "trajectory.jsonl").write_bytes(raw)
            stage(source, root / "public")
            cleaned = (root / "public/jobs/a-lobby/trajectory.jsonl").read_bytes()
            self.assertNotIn(b"example-session", cleaned)
            self.assertNotIn(b"example-signature", cleaned)
            self.assertNotIn(b"/private/tmp", cleaned)
            self.assertEqual((job / "trajectory.jsonl").read_bytes(), raw)
            mapping = json.loads((root / "public/redactions.json").read_bytes())[
                "jobs/a-lobby/trajectory.jsonl"
            ]
            self.assertEqual(
                mapping["original_sha256"], hashlib.sha256(raw).hexdigest()
            )
            self.assertEqual(
                mapping["public_sha256"], hashlib.sha256(cleaned).hexdigest()
            )
            (job / "stderr.txt").write_text("/Users/example/private")
            with self.assertRaisesRegex(ValueError, "Staging refused"):
                stage(source, root / "rejected")
            self.assertFalse((root / "rejected").exists())
