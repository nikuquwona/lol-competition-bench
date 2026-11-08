# Invictus Gaming vs Top Esports · G2 · BP 前

lpl-2026-regional-finals · Round 1 · 26.17 · BO5

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/lpl-2026-regional-finals-round-1-1-g2-lobby/trajectory.jsonl) · [stderr](../../jobs/lpl-2026-regional-finals-round-1-1-g2-lobby/stderr.txt) · [交卷文件](../../jobs/lpl-2026-regional-finals-round-1-1-g2-lobby/prediction.json)

## 输入与可查询证据

蓝方首发为 JiaQi, Meiko, Rookie, TheShy, Wei。

红方首发为 Creme, JackeyLove, Tian, ZUIAN, Zhuo。

冻结时可查 1 个历史小局，10 名首发有历史出场记录。

本局可见 0 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.54,
    "p_blue_ahead_15": 0.46
  },
  "observed_outcome": {
    "p_blue_win": 0,
    "p_blue_ahead_15": 0
  },
  "brier": {
    "p_blue_win": 0.2916,
    "p_blue_ahead_15": 0.2116
  },
  "reward": 0.7484
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 32699,
  "cached_input_tokens": 29696,
  "cache_write_input_tokens": 0,
  "output_tokens": 3097,
  "reasoning_output_tokens": 2325
}
```

## 执行轨迹

### 1. CLI 诊断

```
Model metadata for `deepseek-v4-pro` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
```

### 2. 模型消息

```
I'll examine the snapshot data first to build an evidence-based forecast.
```

### 3. 终端命令 · 退出码 0

```
/bin/zsh -c 'cat snapshot.json'
```

### 4. 命令输出

```
{"phase": "lobby", "series_time_utc": "2026-09-17T09:00:00+00:00", "current": {"event": "lpl-2026-regional-finals", "stage": "Round 1", "series": "lpl-2026-regional-finals-round-1-1", "n": 2, "patch": "26.17", "bo": 5, "blue": "Invictus Gaming", "red": "Top Esports", "starters": {"blue": ["JiaQi", "Meiko", "Rookie", "TheShy", "Wei"], "red": ["Creme", "JackeyLove", "Tian", "ZUIAN", "Zhuo"]}, "draft_rule": "Fearless"}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yorick"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Yorick", "k": 2, "d": 1, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 1, "d": 5, "a": 5}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 3, "d": 1, "a": 7}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 5, "d": 5, "a": 4}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 10}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Jayce", "k": 1, "d": 1, "a": 5}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 1, "d": 6, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Orianna", "k": 7, "d": 0, "a": 1}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Lucian", "k": 2, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Milio", "k": 1, "d": 2, "a": 10}]}], "coverage": {"history_games": 1, "starters": [{"side": "blue", "name": "JiaQi", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Meiko", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Rookie", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "TheShy", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Wei", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Creme", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "JackeyLove", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Tian", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "ZUIAN", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Zhuo", "games": 1, "same_patch_games": 1}], "starters_with_history": 10, "coverage_group": "all", "previous_series_games": [1], "missing_previous_series_games": []}}
```

### 5. 模型消息

```
The snapshot has only one prior game in this series (game 1): IG won on blue side despite being down 38 gold at 15, with TES mid Creme going 7/0/1. I'll write an initial estimate now.
```

### 6. 终端命令 · 退出码 0

```
/bin/zsh -c "cat > prediction.json <<'EOF'
{\"p_blue_win\": 0.54, \"p_blue_ahead_15\": 0.46}
EOF
cat prediction.json"
```

### 7. 命令输出

```
{"p_blue_win": 0.54, "p_blue_ahead_15": 0.46}
```

### 8. 模型消息

```
I've saved an initial forecast. The evidence is thin—one prior game in the series—so the estimates lean on that game plus general priors.

**Reasoning**
- Game 1 was IG (blue) winning despite TES having 12 kills to IG's 11 and a 38-gold lead at 15, with Creme's Orianna going 7/0/1. That suggests a close, comeback-oriented match rather than IG dominance.
- IG's win on the same patch and same matchup gives them a modest momentum edge, but TES remains strong on paper (JackeyLove/Tian/Creme), so `p_blue_win` sits slightly above coin-flip.
- The only gold-at-15 sample had blue behind (-38), a weak signal nudging `p_blue_ahead_15` below 0.5.

**Prediction**
- `prediction.json`: `{"p_blue_win": 0.54, "p_blue_ahead_15": 0.46}`

Both values are valid finite probabilities in [0,1], and the file is written.
```
