import copy
import hashlib
import json
import tarfile
import unittest

from evaluation.draft import ASSETS, draft_static, draft_view
from evaluation.suite import DEFAULT_RELEASE
from production.store import read


class DraftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.views = {}
        with tarfile.open(DEFAULT_RELEASE / "tasks.tar.gz") as archive:
            for entry in archive:
                if entry.name.endswith("/environment/snapshot.json"):
                    cls.views[entry.name.split("/")[0]] = json.load(
                        archive.extractfile(entry)
                    )

    def test_every_game_uses_only_its_own_phase_and_patch(self):
        phases = {"lobby": 0, "draft-lock": 0}
        sources = read(ASSETS / "champions/sources.json")["patches"]
        portraits = draft_static()
        for key, snapshot in self.views.items():
            with self.subTest(task=key):
                phase = snapshot["phase"]
                phases[phase] += 1
                result = draft_view(snapshot, phase)
                current = snapshot["current"]
                self.assertEqual(result["patch"], current["patch"])
                for side in ("blue", "red"):
                    self.assertEqual(
                        result["teams"][side],
                        {"name": current[side], "starters": current["starters"][side]},
                    )
                if phase == "lobby":
                    self.assertNotIn("actions", result)
                    self.assertNotIn("/champions/", json.dumps(result))
                    continue
                actions = result["actions"]
                self.assertEqual(
                    [
                        (a["turn"], a["side"], a["action"], a["champion"])
                        for a in actions
                    ],
                    [
                        (a["turn"], a["side"], a["action"], a["champion"])
                        for a in current["bp"]
                    ],
                )
                for side in ("blue", "red"):
                    self.assertEqual(
                        sum(
                            a["side"] == side and a["action"] == "pick" for a in actions
                        ),
                        5,
                    )
                for a in actions:
                    self.assertIn(a["icon"], portraits)
                    matches = [
                        c
                        for c in sources[result["patch"]]["champions"].values()
                        if a["champion"] in c["aliases"]
                    ]
                    self.assertEqual(len(matches), 1)
                    self.assertEqual(a["icon"], "/champions/" + matches[0]["file"])
        self.assertEqual(phases, {"lobby": 99, "draft-lock": 99})

    def test_kc_lobby_rejects_draft_and_later_results(self):
        prefix = "worlds-2026-main-event-quarterfinals-4-g2-"
        lobby = copy.deepcopy(self.views[prefix + "lobby"])
        locked = self.views[prefix + "draft-lock"]
        expected = draft_view(lobby, "lobby")
        self.assertIn("Faker", expected["teams"]["red"]["starters"])
        lobby["current"]["bp"] = locked["current"]["bp"]
        lobby["current"]["winner"] = "T1"
        lobby["history"] = [{"bp": [{"champion": "future"}]}]
        self.assertEqual(draft_view(lobby, "lobby"), expected)
        self.assertIsNone(draft_view(locked, "lobby"))
        view = draft_view(locked, "draft-lock")
        picks = {
            s: [
                (a["turn"], a["champion"])
                for a in view["actions"]
                if a["side"] == s and a["action"] == "pick"
            ]
            for s in ("blue", "red")
        }
        self.assertEqual(
            picks["blue"],
            [
                (8, "Orianna"),
                (9, "Pantheon"),
                (12, "Ambessa"),
                (17, "Rell"),
                (20, "Tristana"),
            ],
        )
        self.assertEqual(
            picks["red"],
            [
                (7, "Cassiopeia"),
                (10, "Olaf"),
                (11, "Nautilus"),
                (18, "Kai'Sa"),
                (19, "Trundle"),
            ],
        )
        self.assertEqual(view["actions"][0]["champion"], "Locke")
        self.assertEqual(
            view["actions"][14]["icon"].split("/")[-1].split("-")[0], "monkeyking"
        )
        self.assertEqual(view["actions"][17]["label"], "卡莎")
        for action in view["actions"]:
            self.assertNotIn("player", action)

    def test_unknown_art_still_has_original_names(self):
        key = "worlds-2026-main-event-quarterfinals-4-g2-draft-lock"
        snapshot = copy.deepcopy(self.views[key])
        snapshot["current"]["bp"][0]["champion"] = "Unknown champion"
        action = draft_view(snapshot, "draft-lock")["actions"][0]
        self.assertIsNone(action["icon"])
        self.assertEqual(action["label"], "Unknown champion")
        snapshot["current"]["patch"] = "99.99"
        actions = draft_view(snapshot, "draft-lock")["actions"]
        self.assertTrue(
            all(a["icon"] is None and a["label"] == a["champion"] for a in actions)
        )

    def test_all_registered_images_are_local_and_match_source_records(self):
        source = read(ASSETS / "champions/sources.json")
        self.assertEqual(
            {k: v["data_dragon"] for k, v in source["patches"].items()},
            {"26.17": "16.17.1", "26.20": "16.20.1"},
        )
        for p in source["patches"].values():
            self.assertIn(
                "https://ddragon.leagueoflegends.com/cdn/"
                + p["data_dragon"]
                + "/img/champion/",
                p["source_template"],
            )
            for ch in p["champions"].values():
                data = (ASSETS / "champions" / ch["file"]).read_bytes()
                self.assertEqual(data[:4], b"RIFF")
                self.assertEqual(data[8:12], b"WEBP")
                self.assertEqual(hashlib.sha256(data).hexdigest(), ch["sha256"])
                self.assertRegex(ch["source_sha256"], r"^[a-f0-9]{64}$")
