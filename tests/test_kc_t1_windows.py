"""Replay KC–T1 G2 with its real draft and outcome and an explicitly synthetic event clock."""

import json
import tempfile
import unittest
from datetime import UTC, datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from production.build import ROOT
from production.intake import close_window, freeze, settle, standings, submit
from production.store import read

SERIES = "worlds-2026-main-event-quarterfinals-4"


class KCWindows(unittest.TestCase):
    def test_both_windows(self):
        archive = read(ROOT / "production/data/games.json")
        target = next(g for g in archive if (g["series"], g["n"]) == (SERIES, 2))
        base = datetime(2026, 11, 6, 23, tzinfo=UTC)
        source = "https://example.org/synthetic-acceptance-clock"
        identity = {
            k: target[k]
            for k in (
                "series",
                "n",
                "event",
                "stage",
                "patch",
                "bo",
                "blue",
                "red",
                "series_time",
            )
        }
        identity.update(
            draft_rule="Fearless",
            starters={
                s: [p["name"] for p in target["players"] if p["side"] == s]
                for s in ("blue", "red")
            },
            source=source,
        )
        prediction = {"p_blue_win": 0.5, "p_blue_ahead_15": 0.5}
        with (
            tempfile.TemporaryDirectory() as temp,
            patch("production.intake.now") as clock,
        ):
            root = Path(temp)
            store = root / "intake"
            before_game = root / "archive.json"
            before_game.write_text(
                json.dumps([g for g in archive if g["series"] != SERIES or g["n"] == 1])
            )
            with patch("production.store.BASE_HISTORY", before_game):
                clock.return_value = base
                lobby = freeze(
                    {**identity, "phase": "lobby", "observed_at": base.isoformat()},
                    store,
                )
                submit(lobby, "before-bp", prediction)
                # The event source reports late. The receipt exactly at first BP must still lose eligibility.
                clock.return_value = first_bp = base + timedelta(minutes=1)
                submit(lobby, "at-first-bp", prediction)
                clock.return_value += timedelta(seconds=5)
                close_window(lobby, first_bp.isoformat(), source)
                with self.assertRaisesRegex(ValueError, "closed"):
                    submit(lobby, "during-bp", prediction)
                clock.return_value = base + timedelta(minutes=5)
                draft = freeze(
                    {
                        **identity,
                        "phase": "draft-lock",
                        "observed_at": clock.return_value.isoformat(),
                        "bp": target["bp"],
                    },
                    store,
                )
                with self.assertRaisesRegex(ValueError, "closed"):
                    submit(lobby, "after-lock", prediction)
                submit(draft, "before-game", prediction)
                clock.return_value = start = base + timedelta(minutes=7)
                submit(draft, "at-game-start", prediction)
                close_window(draft, start.isoformat(), source)
                with self.assertRaisesRegex(ValueError, "closed"):
                    submit(draft, "after-start", prediction)
                clock.return_value = base + timedelta(hours=1)
                result = {
                    "id": draft.name,
                    "winner": "blue" if target["blue_win"] else "red",
                    "blue_gd15": target["blue_gd15"],
                    "game_started_at": start.isoformat(),
                    "published_at": clock.return_value.isoformat(),
                    "source": source,
                }
                with self.assertRaisesRegex(ValueError, "conflicts"):
                    settle(
                        draft,
                        {
                            **result,
                            "game_started_at": (
                                start + timedelta(seconds=1)
                            ).isoformat(),
                        },
                    )
                settle(draft, result)
                rows = {
                    r["entrant"]: r["status"]
                    for case in (lobby, draft)
                    for r in standings(case)
                }
                self.assertEqual(
                    rows,
                    {
                        "before-bp": "scored",
                        "at-first-bp": "ineligible",
                        "before-game": "scored",
                        "at-game-start": "ineligible",
                    },
                )


if __name__ == "__main__":
    unittest.main()
