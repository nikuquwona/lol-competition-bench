"""Normalize a frozen replay release; never mount this directory into an agent."""

import json
import math
import re
from datetime import datetime, timedelta, timezone
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from production.fetch import BASE, CACHE, EVENTS, ROOT, TENCENT, fetch, obj

DATA = ROOT / "production/data"
RIOT = "https://lolesports.com/en-US/leagues/worlds"
UTC = timezone.utc
CST = timezone(timedelta(hours=8))


def write(name, data):
    (DATA / name).write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n"
    )


def draft_index(page):
    url = "https://lol.fandom.com/api.php?" + urlencode(
        dict(action="parse", page=page + "/Picks and Bans", prop="text", format="json")
    )
    soup = BeautifulSoup(obj(url)["parse"]["text"]["*"], "html.parser")
    drafts = {}
    for row in soup.select("table.column-show-hide-1 tr"):
        cells = row.select("td")
        if not cells:
            continue
        events = []
        for cell in cells[6:23]:
            classes = cell.get("class", [])
            side = (
                "blue"
                if "pbh-blue" in classes
                else "red"
                if "pbh-red" in classes
                else None
            )
            action = "ban" if "pbh-ban" in classes else "pick"
            for node in cell.select(".champion-sprite[title]"):
                events.append(
                    dict(
                        turn=len(events) + 1,
                        side=side,
                        action=action,
                        champion=node["title"],
                    )
                )
        if len(events) == 20 and all(e["side"] for e in events):
            key = (
                cells[0].get_text(strip=True),
                frozenset(c["title"] for c in cells[1:3]),
                sum(map(int, re.findall(r"\d+", cells[3].text))),
            )
            if key in drafts:
                raise ValueError(f"Ambiguous draft: {key}")
            winner = cells[4].select_one("img[data-image-key]")
            teams_by_logo = {
                c.select_one("img[data-image-key]")["data-image-key"]: c["title"]
                for c in cells[1:3]
            }
            winner_name = (
                teams_by_logo.get(winner["data-image-key"]) if winner else None
            )
            drafts[key] = (cells[5].get_text(strip=True), events, winner_name)
    return drafts


def rating(player, teammates, minutes, won, config, year):
    def share(value, total):
        return value / total if value is not None and total else None

    def total(field):
        return sum(p.get(field) or 0 for p in teammates)

    metrics = dict(
        kp=share(player["k"] + player["a"], total("k")),
        ds=share(player.get("dm"), total("dm")),
        gs=share(player.get("gd"), total("gd")),
        cs=share(player.get("cs"), minutes),
        vs=share(player.get("v"), total("v")),
        dpm=share(player["d"], minutes),
    )
    weight = score = 0
    for metric, value in metrics.items():
        dist = config["base"].get(f"{year}|{player['r']}", {}).get(metric) or config[
            "base"
        ].get(f"all|{player['r']}", {}).get(metric)
        if value is not None and dist and dist[1]:
            w = config["w"][metric]
            score += w * max(-3, min(3, (value - dist[0]) / dist[1]))
            weight += abs(w)
    if weight < 0.5:
        return None
    raw = 6 + config["scale"] * score / weight + (1 if won else -1) * config["win"]
    return math.floor(max(0, min(10, raw)) * 10 + 0.5) / 10


def tencent_matches():
    rows = []
    for n in (237, 246):
        for row in obj(f"{TENCENT}/LOL_MATCH2_MATCH_HOMEPAGE_BMATCH_LIST_{n}.js")[
            "msg"
        ]:
            if row["MatchStatus"] != "3" or (
                n == 237 and not "2026-09-17" <= row["MatchDate"][:10] <= "2026-09-19"
            ):
                continue
            start = (
                datetime.fromisoformat(row["MatchDate"])
                .replace(tzinfo=CST)
                .astimezone(UTC)
            )
            url = f"{TENCENT}/LOL_MATCH_DETAIL_{row['bMatchId']}.js"
            raw = fetch(url).decode()
            detail = json.loads(raw[raw.index("{") : raw.rindex("}") + 1])
            videos = json.loads(detail.get("sExt4") or "[]")
            total_games = int(row["ScoreA"]) + int(row["ScoreB"])
            dates = {}
            for video in videos:
                title = video.get("title", "").strip()
                number = re.search(r"_0?(\d+)$", title)
                if (
                    not video.get("url")
                    or not video.get("indexDate")
                    or " vs " not in title
                    or "【" in title
                ):
                    continue
                if number is None and total_games != 1:
                    continue
                n = int(number[1]) if number else 1
                dates[n] = (
                    datetime.fromisoformat(video["indexDate"])
                    .replace(tzinfo=CST)
                    .astimezone(UTC)
                )
            available = (
                max(dates.values()).isoformat()
                if set(dates) == set(range(1, total_games + 1))
                else None
            )
            rows.append(
                dict(
                    url=url,
                    teams=[detail["TeamNameA"], detail["TeamNameB"]],
                    scores=[int(row["ScoreA"]), int(row["ScoreB"])],
                    start=start.isoformat(),
                    bo=row["GameModeName"],
                    replay_published=available,
                )
            )
    return rows


def riot_rows():
    text = fetch(RIOT).decode()
    rows = {}
    for m in re.finditer(r'\{"__typename":"EventMatch","id":', text):
        e, _ = json.JSONDecoder().raw_decode(text, m.start())
        if e["state"] == "completed" and e["league"]["slug"] == "worlds":
            rows[e["id"]] = dict(
                start=e["startTime"],
                teams=[t["code"] for t in e["matchTeams"]],
                scores=[t["result"]["gameWins"] for t in e["matchTeams"]],
            )
    return rows


def team(name):
    return {
        "西安we": "we",
        "北京jdg": "jdg",
        "tl": "tlaw",
        "tlh": "tlaw",
        "team liquid": "tlaw",
        "ig": "ig",
    }.get(name.lower(), name.lower())


def official(series, rows):
    teams = [series[k]["c"] for k in ("a", "b")]
    expected = {team(t): s for t, s in zip(teams, [series["sa"], series["sb"]])}
    date = datetime.fromisoformat(series["date"]).replace(tzinfo=UTC)
    return [
        r
        for r in rows
        if {team(t): s for t, s in zip(r["teams"], r["scores"])} == expected
        and abs(datetime.fromisoformat(r["start"].replace("Z", "+00:00")) - date)
        < timedelta(hours=8)
    ]


def main():
    DATA.mkdir(exist_ok=True)
    games, rosters, audit = [], {}, []
    qq = tencent_matches()
    riot = riot_rows()
    config = obj(BASE + "/rating.json")
    for event in EVENTS:
        doc = obj(f"{BASE}/event/{event}.json")
        rosters[event] = {
            r["t"]: [dict(name=p[0], role=p[2]) for p in r["p"]] for r in doc["rosters"]
        }
        draft = draft_index(doc["op"])
        for stage in doc["stages"]:
            for match in stage["series"]:
                if match.get("w") not in (1, 2):
                    continue
                slug = match["g"]
                s = obj(f"{BASE}/game/{slug}.json")
                q = official(s, qq)
                rr = official(s, [dict(v, id=k) for k, v in riot.items()])
                audit.append(dict(series=slug, tencent=q, riot=[r["id"] for r in rr]))
                for g in s["games"]:
                    if g.get("w") not in (1, 2) or g.get("blue") not in ("a", "b"):
                        continue
                    blue = s[g["blue"]]["n"]
                    red = s["a" if g["blue"] == "b" else "b"]["n"]
                    win = s["ab"[g["w"] - 1]]["n"] == blue
                    players = []
                    for p in g.get("p", []):
                        peers = [x for x in g["p"] if x["s"] == p["s"]]
                        side = "blue" if p["s"] == 1 else "red"
                        players.append(
                            dict(
                                name=p["n"],
                                role=p["r"],
                                side=side,
                                champion=p["c"],
                                k=p["k"],
                                d=p["d"],
                                a=p["a"],
                                rating=rating(
                                    p,
                                    peers,
                                    g["min"],
                                    win == (side == "blue"),
                                    config,
                                    s["date"][:4],
                                ),
                            )
                        )
                    patch, actions, listed_winner = draft.get(
                        (s["stage"], frozenset((blue, red)), g["n"]), (None, [], None)
                    )
                    if actions and listed_winner != (blue if win else red):
                        raise ValueError(
                            f"Conflicting winner: {slug} game {g['n']}, {listed_winner}"
                        )
                    if actions:
                        for side in ("blue", "red"):
                            picks = {
                                e["champion"]
                                for e in actions
                                if e["side"] == side and e["action"] == "pick"
                            }
                            if (
                                picks
                                != {p["champion"] for p in players if p["side"] == side}
                                or patch != g["patch"]
                            ):
                                actions = []
                                break
                    games.append(
                        dict(
                            series=slug,
                            n=g["n"],
                            event=event,
                            stage=s["stage"],
                            patch=g["patch"],
                            bo=s["bo"],
                            blue=blue,
                            red=red,
                            series_time=min(
                                q[0]["start"], s["date"].replace(" ", "T") + ":00+00:00"
                            )
                            if len(q) == 1
                            else s["date"].replace(" ", "T") + ":00+00:00",
                            replay_published=q[0]["replay_published"]
                            if len(q) == 1
                            else None,
                            bp=actions,
                            players=players,
                            blue_win=win,
                            blue_gd15=g.get("t", {}).get("blue", {}).get("g15"),
                        )
                    )
    write("games.json", games)
    write("event-rosters.json", rosters)
    write("official-matches.json", audit)
    write(
        "sources.json",
        [json.loads(p.read_text()) for p in sorted(CACHE.glob("*.meta"))],
    )
    print(len(games), "games;", sum(bool(g["bp"]) for g in games), "verified drafts")


if __name__ == "__main__":
    main()
