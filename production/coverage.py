"""Count the evidence available to the forecaster from the frozen view alone."""

from collections import Counter


def history_card(current, history):
    appearances = Counter()
    same_patch = Counter()
    prior_games = set()
    for game in history:
        # One game counts at most once per handle. Missing box scores add no evidence.
        handles = {row["name"].casefold() for row in game["players"]}
        appearances.update(handles)
        if game["patch"] == current["patch"]:
            same_patch.update(handles)
        if game["series"] == current["series"] and game["n"] < current["n"]:
            prior_games.add(game["n"])
    starters = [
        {
            "side": side,
            "name": name,
            "games": appearances[name.casefold()],
            "same_patch_games": same_patch[name.casefold()],
        }
        for side in ("blue", "red")
        for name in current["starters"][side]
    ]
    covered = sum(row["games"] > 0 for row in starters)
    group = "partial"
    if covered == 0:
        group = "none"
    elif covered == len(starters):
        group = "all"
    return {
        "history_games": len(history),
        "starters": starters,
        "starters_with_history": covered,
        "coverage_group": group,
        "previous_series_games": sorted(prior_games),
        "missing_previous_series_games": sorted(
            set(range(1, current["n"])) - prior_games
        ),
    }
