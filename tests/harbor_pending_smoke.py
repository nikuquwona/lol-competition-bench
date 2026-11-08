"""Remote acceptance check for an unlabeled game. All example data stays in a temporary store."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from production.intake import freeze, settle, submit
from production.score import read_prediction
from production.store import read
from test_pipeline import observation


def main():
    with tempfile.TemporaryDirectory(prefix="lol-future-ci-") as tmp:
        root = Path(tmp)
        o = observation()
        start = datetime.now(timezone.utc)
        o.update(series_time=start.isoformat(), observed_at=start.isoformat())
        case = freeze(o, root / "store")
        assert (
            not (case / "task/tests").exists() and not (case / "task/solution").exists()
        )
        env = {
            **os.environ,
            "BENCH_CLI": "codex",
            "BENCH_MODE": "fixture",
            "BENCH_MODEL": "deepseek-v4-pro",
        }
        jobs = root / "jobs"
        subprocess.run(
            [
                "harbor",
                "run",
                "-p",
                str(case / "task"),
                "-a",
                "evaluation.cli.agent:CompetitionCLI",
                "--disable-verification",
                "--jobs-dir",
                str(jobs),
            ],
            check=True,
            env=env,
        )
        (prediction,) = jobs.rglob("artifacts/app/prediction.json")
        (runtime,) = jobs.rglob("cli-run.json")
        assert read(runtime)["mode"] == "fixture" and not list(jobs.rglob("reward.txt"))
        receipt = submit(case, "ci-protocol-fixture", read_prediction(prediction))
        assert receipt["prediction"] == {"p_blue_win": 0.41, "p_blue_ahead_15": 0.57}
        played = datetime.now(timezone.utc) + timedelta(seconds=1)
        published = played + timedelta(hours=1)
        with patch("production.intake.now", return_value=published):
            rows = settle(
                case,
                dict(
                    id=case.name,
                    winner="red",
                    blue_gd15=-20,
                    game_started_at=played.isoformat(),
                    published_at=published.isoformat(),
                    source="https://example.org/ci-fixture",
                ),
            )
        assert rows[0]["status"] == "scored" and abs(rows[0]["reward"] - 0.7535) < 1e-12
        print(
            "Unlabeled Harbor task → actual CLI tool call → sealed receipt → post-game score",
            rows,
        )


if __name__ == "__main__":
    main()
