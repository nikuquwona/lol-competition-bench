# Game 2 · LØS vs LYON

You are forecasting one professional League of Legends game at **the pre-draft lobby**. LØS is on blue side and LYON is on red side. This is game 2 of a best-of-3 series on patch 26.20. Starters and sides are known. The draft has not begun.

## Evidence

Open `./snapshot.json`. The `current` object identifies the teams, starters, format and draft rules. The target game's picks and bans are still unknown. The `history` array contains 79 earlier games available at the cutoff. Each record identifies its patch, sides and game number. Where recorded, it includes the draft, winner, blue-minus-red gold at 15:00, and each player's role, champion and K/D/A. A missing observation is unknown.

The `coverage` object counts earlier games with a recorded appearance for each starter, including the subset on the current patch. It also lists any missing earlier games from this series. A count of zero means the snapshot has no matching appearance.

You may search, filter and aggregate this file with local shell tools or Python's standard library. Use general League knowledge to interpret it. External search, other sessions, remembered outcomes of this game and evidence from later games are outside the forecast. Compare opponents, patch and sample size when weighing past performances. In Fearless series, picks from earlier games in that series are unavailable to both teams.

## Forecast

Estimate both events independently for **this game**:

| Output field | Event |
| --- | --- |
| `p_blue_win` | Blue side wins the game. |
| `p_blue_ahead_15` | Blue has strictly more team gold at 15:00. Equal gold counts as false. |

Write one JSON object to `./prediction.json` with exactly those two fields. Each value must be a finite number between 0 and 1. A written file is required for scoring; a chat reply alone does not submit it.

Make a first estimate from the most relevant evidence and save it early, ideally within four shell calls. Revise the file if further evidence changes your estimate. Finish once both probabilities are valid. The two squared probability errors carry equal weight: reward is one minus their mean. A missing or invalid submission earns zero.
