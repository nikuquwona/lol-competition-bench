import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from evaluation.cli.boundary import SERIES, prepare, verify
from evaluation.cli.boundary_probe import inspect_files
from evaluation.suite import DEFAULT_RELEASE, select, unpack


class CanaryTest(unittest.TestCase):
    def test_visible_canary_fails_and_allowed_snapshot_stays_identical(self):
        ids = [SERIES + s for s in ("-g2-lobby", "-g2-draft-lock", "-g3-draft-lock")]
        manifest, rows = select(DEFAULT_RELEASE, ids=ids)
        for phase in ("lobby", "draft-lock"):
            with self.subTest(phase=phase), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                unpack(DEFAULT_RELEASE, manifest, rows, root)
                snapshot = (
                    root / (SERIES + "-g2-" + phase) / "environment/snapshot.json"
                )
                before = snapshot.read_bytes()
                config, commitments, command = prepare(root, phase)
                self.assertEqual(before, snapshot.read_bytes())
                for path, expected in commitments.items():
                    marker = json.loads((root / path).read_text())["acceptance_canary"]
                    self.assertEqual(
                        hashlib.sha256(marker.encode()).hexdigest(), expected
                    )
                    self.assertNotIn(marker, command)

                # Deliberately expose the complete organizer tree to the same attack routine.
                # Each planted token must be recovered and trigger a failed verdict.
                opened, found = inspect_files([root / p for p in commitments], [root])
                self.assertEqual(set(opened), {str(root / p) for p in commitments})
                self.assertEqual(
                    {f["sha256"] for f in found}, set(commitments.values())
                )
                diff = verify(
                    {"found_markers": found, "opened_forbidden_files": opened},
                    config,
                    phase,
                    [],
                )
                self.assertIn("found_markers", diff)
                self.assertIn("opened_forbidden_files", diff)
                self.assertIn("challenge", diff)
