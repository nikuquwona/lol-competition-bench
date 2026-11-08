# Invictus Gaming vs Top Esports · G2 · BP 锁定

lpl-2026-regional-finals · Round 1 · 26.17 · BO5

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/lpl-2026-regional-finals-round-1-1-g2-draft-lock/trajectory.jsonl) · [stderr](../../jobs/lpl-2026-regional-finals-round-1-1-g2-draft-lock/stderr.txt) · [交卷文件](../../jobs/lpl-2026-regional-finals-round-1-1-g2-draft-lock/prediction.json)

## 输入与可查询证据

蓝方首发为 JiaQi, Meiko, Rookie, TheShy, Wei。

红方首发为 Creme, JackeyLove, Tian, ZUIAN, Zhuo。

冻结时可查 1 个历史小局，10 名首发有历史出场记录。

本局可见 20 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.56,
    "p_blue_ahead_15": 0.38
  },
  "observed_outcome": {
    "p_blue_win": 0,
    "p_blue_ahead_15": 0
  },
  "brier": {
    "p_blue_win": 0.31360000000000005,
    "p_blue_ahead_15": 0.1444
  },
  "reward": 0.7709999999999999
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 103495,
  "cached_input_tokens": 75456,
  "cache_write_input_tokens": 0,
  "output_tokens": 12719,
  "reasoning_output_tokens": 11255
}
```

## 执行轨迹

### 1. CLI 诊断

```
Model metadata for `nvidia/nemotron-3.5-lightning:free` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
```

### 2. 终端命令 · 退出码 0

```
/bin/zsh -lc 'cat [ephemeral]/app/snapshot.json'
```

### 3. 命令输出

```
{"phase": "draft-lock", "series_time_utc": "2026-09-17T09:00:00+00:00", "current": {"event": "lpl-2026-regional-finals", "stage": "Round 1", "series": "lpl-2026-regional-finals-round-1-1", "n": 2, "patch": "26.17", "bo": 5, "blue": "Invictus Gaming", "red": "Top Esports", "starters": {"blue": ["JiaQi", "Meiko", "Rookie", "TheShy", "Wei"], "red": ["Creme", "JackeyLove", "Tian", "ZUIAN", "Zhuo"]}, "draft_rule": "Fearless", "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Trundle"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ashe"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Ryze"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Lee Sin"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Camille"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Nautilus"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Galio"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Naafiri"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Maokai"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Ezreal"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Karma"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yone"}]}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yorick"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Yorick", "k": 2, "d": 1, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 1, "d": 5, "a": 5}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 3, "d": 1, "a": 7}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 5, "d": 5, "a": 4}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 10}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Jayce", "k": 1, "d": 1, "a": 5}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 1, "d": 6, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Orianna", "k": 7, "d": 0, "a": 1}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Lucian", "k": 2, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Milio", "k": 1, "d": 2, "a": 10}]}], "coverage": {"history_games": 1, "starters": [{"side": "blue", "name": "JiaQi", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Meiko", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Rookie", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "TheShy", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Wei", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Creme", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "JackeyLove", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Tian", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "ZUIAN", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Zhuo", "games": 1, "same_patch_games": 1}], "starters_with_history": 10, "coverage_group": "all", "previous_series_games": [1], "missing_previous_series_games": []}}
```

### 4. 模型消息

```
Now I have the snapshot data. Let me analyze the draft, historical game 1 data, and make predictions.
```

### 5. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json
with open('snapshot.json') as f:
    data = json.load(f)

# Print key sections
print('=== CURRENT GAME (Game 2) ===')
c = data['current']
print(f'Event: {c[\\\"event\\\"]}')
print(f'Stage: {c[\\\"stage\\\"]}')
print(f'Series: {c[\\\"series\\\"]}')
print(f'Patch: {c[\\\"patch\\\"]}')
print(f'BO: {c[\\\"bo\\\"]}')
print(f'Blue: {c[\\\"blue\\\"]}')
print(f'Red: {c[\\\"red\\\"]}')
print(f'Draft rule: {c[\\\"draft_rule\\\"]}')
print()

print('=== DRAFT (bp) ===')
for action in data['current']['bp']:
    print(f'Turn {action[\\\"turn\\\"]}: {action[\\\"side\\\"]} {action[\\\"action\\\"]} {action[\\\"champion\\\"]}')

print()
print('=== BLUE PICKS ===')
blue_picks = [a['champion'] for a in data['current']['bp'] if a['side'] == 'blue' and a['action'] == 'pick']
print(blue_picks)

print('=== RED PICKS ===')
red_picks = [a['champion'] for a in data['current']['bp'] if a['side'] == 'red' and a['action'] == 'pick']
print(red_picks)

print()
print('=== HISTORY GAME 1 ===')
h = data['history'][0]
print(f'Blue win: {h[\\\"blue_win\\\"]}')
print(f'Blue gold diff at 15:00: {h[\\\"blue_gd15\\\"]}')
print()

print('=== GAME 1 DRAFT ===')
for action in h['bp']:
    print(f'Turn {action[\\\"turn\\\"]}: {action[\\\"side\\\"]} {action[\\\"action\\\"]} {action[\\\"champion\\\"]}')

print()
print('=== GAME 1 PLAYERS ===')
for p in h['players']:
    print(f'  {p[\\\"name\\\"]} ({p[\\\"role\\\"]}, {p[\\\"side\\\"]}): {p[\\\"champion\\\"]} K/{p[\\\"k\\\"]}D/{p[\\\"a\\\"]}')

print()
print('=== COVERAGE ===')
cov = data['coverage']
print(f'History games: {cov[\\\"history_games\\\"]}')
print(f'Starters with history: {cov[\\\"starters_with_history\\\"]}')
print(f'Missing previous series games: {cov[\\\"missing_previous_series_games\\\"]}')
\""
```

### 6. 命令输出

```
=== CURRENT GAME (Game 2) ===
Event: lpl-2026-regional-finals
Stage: Round 1
Series: lpl-2026-regional-finals-round-1-1
Patch: 26.17
BO: 5
Blue: Invictus Gaming
Red: Top Esports
Draft rule: Fearless

=== DRAFT (bp) ===
Turn 1: red ban Qiyana
Turn 2: blue ban Cassiopeia
Turn 3: red ban Jarvan IV
Turn 4: blue ban Vi
Turn 5: red ban Trundle
Turn 6: blue ban Nocturne
Turn 7: red pick Olaf
Turn 8: blue pick Ashe
Turn 9: blue pick Seraphine
Turn 10: red pick Ryze
Turn 11: red pick Lee Sin
Turn 12: blue pick Camille
Turn 13: blue ban Nautilus
Turn 14: red ban Galio
Turn 15: blue ban Renata Glasc
Turn 16: red ban Naafiri
Turn 17: blue pick Maokai
Turn 18: red pick Ezreal
Turn 19: red pick Karma
Turn 20: blue pick Yone

=== BLUE PICKS ===
['Ashe', 'Seraphine', 'Camille', 'Maokai', 'Yone']
=== RED PICKS ===
['Olaf', 'Ryze', 'Lee Sin', 'Ezreal', 'Karma']

=== HISTORY GAME 1 ===
Blue win: True
Blue gold diff at 15:00: -38

=== GAME 1 DRAFT ===
Turn 1: red ban Qiyana
Turn 2: blue ban Cassiopeia
Turn 3: red ban Olaf
Turn 4: blue ban Vi
Turn 5: red ban Jarvan IV
Turn 6: blue ban Nocturne
Turn 7: red pick Orianna
Turn 8: blue pick Lulu
Turn 9: blue pick Yunara
Turn 10: red pick Lucian
Turn 11: red pick Milio
Turn 12: blue pick Syndra
Turn 13: blue ban Trundle
Turn 14: red ban K'Sante
Turn 15: blue ban Rumble
Turn 16: red ban Renekton
Turn 17: blue pick Skarner
Turn 18: red pick Jayce
Turn 19: red pick Cho'Gath
Turn 20: blue pick Yorick

=== GAME 1 PLAYERS ===
  TheShy (Top, blue): Yorick K/2D/6
  Wei (Jungle, blue): Skarner K/1D/5
  Rookie (Mid, blue): Syndra K/3D/7
  JiaQi (Bot, blue): Yunara K/5D/4
  Meiko (Support, blue): Lulu K/0D/10
  ZUIAN (Top, red): Jayce K/1D/5
  Tian (Jungle, red): Cho'Gath K/1D/6
  Creme (Mid, red): Orianna K/7D/1
  JackeyLove (Bot, red): Lucian K/2D/7
  Zhuo (Support, red): Milio K/1D/10

=== COVERAGE ===
History games: 1
Starters with history: 10
Missing previous series games: []
```

### 7. 模型消息

```
Now I have all the data analyzed. Let me make my estimates based on the evidence:

**Key evidence:**
- Game 1: Blue won with same teams/patch, but was -38 gold at 15:00 (Red ahead)
- Current draft is completely different (Fearless rule - no overlapping picks from Game 1)
- Red's draft: Lee Sin (early jungle), Olaf (early top), Ezreal (ADC), Ryze (mid), Karma (support) — more early-game oriented
- Blue's draft: Ashe (ADC), Seraphine (mid), Camille (top), Maokai (jng), Yone (flex) — more scaling-oriented
- Blue's comeback ability in Game 1 from early deficit
- Same teams, same patch
```

### 8. 终端命令 · 退出码 0

```
/bin/zsh -lc "cat > ./prediction.json << 'EOF'
{\"p_blue_win\": 0.56, \"p_blue_ahead_15\": 0.38}
EOF"
```

### 9. 命令输出

```

```

### 10. 终端命令 · 退出码 0

```
/bin/zsh -lc 'cat ./prediction.json'
```

### 11. 命令输出

```
{"p_blue_win": 0.56, "p_blue_ahead_15": 0.38}
```

### 12. 模型消息

```
The prediction file has been written. Here's my reasoning:

**`p_blue_win` = 0.56** — Blue side wins the game.
- Blue won Game 1 with the same teams on patch 26.17, which is the strongest predictive signal
- Camille (TheShy) vs Olaf favors blue top, as Camille's mobility counters Olaf's engage
- Ashe vs Ezreal is fairly even, with Ashe providing reliable ranged damage and CC
- Blue's composition (Maokai jungle, Camille top, Seraphine mid, Ashe ADC) is well-balanced for late game
- However, Red's early-game oriented draft (Lee Sin, Olaf, Ezreal) provides pressure that could overcome blue's slight edges

**`p_blue_ahead_15` = 0.38** — Blue has strictly more team gold at 15:00.
- Red's draft has more early-game threat: Lee Sin (high-impact early jungler), Olaf (early top lane pressure), and Ezreal provide tempo advantage
- Blue's composition (Maokai scaling jungle, Camille mid-game top, Seraphine scaling mid) is oriented toward mid-late game power
- In Game 1, blue was -38 at 15:00 against red's Orianna/Cho'Gath/Lucian; the current draft gives red similar early-pressure profiles with Lee Sin and Olaf
- Equal gold at 15:00 counts as false, so the probability is for blue *strictly* ahead

Both values are finite numbers between 0 and 1, and the file `./prediction.json` has been written with exactly those two fields.
```
