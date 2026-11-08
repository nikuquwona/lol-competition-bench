"""Single-game DeepSeek runner. The only model tool reads an in-memory frozen snapshot."""

import argparse
import json
import math
import os
import re
from pathlib import Path
from urllib.request import Request, urlopen

MODEL = "deepseek-v4-pro"
SYSTEM = (
    "You are forecasting a League of Legends game at the indicated observation point. "
    "Use only the supplied current facts, the frozen history lookup, and general LoL knowledge. "
    "Do not use or recall results of the target or later games. Query the starters' personal "
    "history and any relevant past teams/series before predicting. Evaluate side, sample size, "
    "and available draft information. Return only a JSON object with p_blue_win and "
    "p_blue_ahead_15 (strict gold lead at 15:00). Both numbers must be probabilities."
)
TOOL = {
    "type": "function",
    "function": {
        "name": "lookup_history",
        "description": "Look up past results in the snapshot, latest first. For player and team queries supply the exact current player or team names; optionally filter champion. For series use its exact identifier. Each entity returns a separate summary and most recent observations. All side-relative statistics refer to that entity's team; series rows refer to blue.",
        "parameters": {
            "type": "object",
            "properties": {
                "kind": {"type": "string", "enum": ["player", "team", "series"]},
                "names": {"type": "array", "items": {"type": "string"}, "maxItems": 10},
                "champion": {"type": "string"},
                "recent": {"type": "integer", "minimum": 1, "maximum": 8},
            },
            "required": ["kind", "names"],
        },
    },
}


def lookup(history, kind, names, champion="", recent=3):
    if (
        kind not in ("player", "team", "series")
        or not isinstance(names, list)
        or not 1 <= len(names) <= 10
    ):
        return {"error": "Supply one to ten names and a supported kind."}
    result = {}
    for name in names:
        rows = []
        for g in reversed(history):
            players = g["players"]
            if kind == "player":
                p = next(
                    (p for p in players if p["name"].casefold() == name.casefold()),
                    None,
                )
                if (
                    not p
                    or champion
                    and p["champion"].casefold() != champion.casefold()
                ):
                    continue
                side = p["side"]
            elif kind == "team":
                side = next(
                    (s for s in ("blue", "red") if g[s].casefold() == name.casefold()),
                    None,
                )
                if not side:
                    continue
            else:
                if g["series"] != name:
                    continue
                side = "blue"
            other = "red" if side == "blue" else "blue"
            gd = g["blue_gd15"]
            row = dict(
                series=g["series"],
                game=g["n"],
                patch=g["patch"],
                side=side,
                team=g[side],
                opponent=g[other],
                win=g["blue_win"] == (side == "blue"),
                gd15=(gd if side == "blue" else -gd) if gd is not None else None,
            )
            if kind == "player":
                row.update(
                    champion=p["champion"], role=p["role"], kda=[p["k"], p["d"], p["a"]]
                )
            if kind == "series":
                row.update(players=players, bp=g["bp"])
            rows.append(row)
        gold = [r["gd15"] for r in rows if r["gd15"] is not None]
        result[name] = dict(
            games=len(rows),
            wins=sum(r["win"] for r in rows),
            gd15_observations=len(gold),
            ahead15=sum(v > 0 for v in gold),
            mean_gd15=round(sum(gold) / len(gold), 1) if gold else None,
            recent=rows[: min(8, max(1, recent))],
        )
    return result


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def final_prediction(content):
    """Accept plain JSON or the single explicit JSON block at the end of a response."""
    body = content.strip()
    blocks = re.findall(r"```json\s*(\{[^`]*?\})\s*```", body)
    if len(blocks) == 1 and body.endswith("```"):
        body = blocks[0]
    pred = json.loads(body)
    if (
        not isinstance(pred, dict)
        or set(pred) != {"p_blue_win", "p_blue_ahead_15"}
        or not all(
            type(x) in (int, float) and math.isfinite(x) and 0 <= x <= 1
            for x in pred.values()
        )
    ):
        raise ValueError("Invalid prediction")
    return pred


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    view = json.loads(args.snapshot.read_text())
    args.out.mkdir(parents=True, exist_ok=False)
    initial = {k: v for k, v in view.items() if k != "history"}
    initial["history_games_available"] = len(view["history"])
    messages = [
        dict(role="system", content=SYSTEM),
        dict(role="user", content=json.dumps(initial, ensure_ascii=False)),
    ]
    settings = dict(
        model=MODEL, temperature=0, thinking={"type": "disabled"}, max_tokens=1200
    )
    trace = dict(settings=settings, tools=[TOOL], messages=messages, calls=[])
    for i in range(10):
        body = dict(
            **settings,
            messages=messages,
            tools=[TOOL],
            tool_choice="none" if i == 9 else "auto",
        )
        req = Request(
            "https://api.deepseek.com/chat/completions",
            data=json.dumps(body).encode(),
            headers={
                "Authorization": "Bearer " + os.environ["DEEPSEEK_API_KEY"],
                "Content-Type": "application/json",
            },
        )
        response = json.load(urlopen(req, timeout=120))
        trace["calls"].append(
            {
                k: response.get(k)
                for k in ("id", "model", "usage", "created", "system_fingerprint")
            }
        )
        msg = response["choices"][0]["message"]
        messages.append(
            {k: msg[k] for k in ("role", "content", "tool_calls") if k in msg}
        )
        save(args.out / "trace.json", trace)
        if not msg.get("tool_calls"):
            pred = final_prediction(msg["content"])
            save(args.out / "prediction.json", pred)
            print(args.out.name, pred, flush=True)
            return
        for call in msg["tool_calls"]:
            try:
                if call["function"]["name"] != "lookup_history":
                    raise ValueError("Unknown tool")
                result = lookup(
                    view["history"], **json.loads(call["function"]["arguments"])
                )
            except (TypeError, ValueError, AttributeError) as exc:
                result = {"error": str(exc)}
            messages.append(
                dict(
                    role="tool",
                    tool_call_id=call["id"],
                    content=json.dumps(result, ensure_ascii=False),
                )
            )
        save(args.out / "trace.json", trace)
    raise RuntimeError("No final prediction within budget")


if __name__ == "__main__":
    main()
