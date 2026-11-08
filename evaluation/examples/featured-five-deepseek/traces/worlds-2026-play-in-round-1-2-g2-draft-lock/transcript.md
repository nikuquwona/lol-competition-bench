# MVK Esports vs FURIA · G2 · BP 锁定

worlds-2026-play-in · Round 1 · 26.20 · BO5

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/worlds-2026-play-in-round-1-2-g2-draft-lock/trajectory.jsonl) · [stderr](../../jobs/worlds-2026-play-in-round-1-2-g2-draft-lock/stderr.txt) · [交卷文件](../../jobs/worlds-2026-play-in-round-1-2-g2-draft-lock/prediction.json)

## 输入与可查询证据

蓝方首发为 Chika, Gury, Harky, Kratos, SiuLoong。

红方首发为 Ayu, Guigo, JoJo, Tatu, Tutsz。

冻结时可查 13 个历史小局，10 名首发有历史出场记录。

本局可见 20 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.58,
    "p_blue_ahead_15": 0.53
  },
  "observed_outcome": {
    "p_blue_win": 1,
    "p_blue_ahead_15": 1
  },
  "brier": {
    "p_blue_win": 0.17640000000000003,
    "p_blue_ahead_15": 0.22089999999999999
  },
  "reward": 0.80135
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 125771,
  "cached_input_tokens": 117760,
  "cache_write_input_tokens": 0,
  "output_tokens": 8966,
  "reasoning_output_tokens": 7861
}
```

## 执行轨迹

### 1. CLI 诊断

```
Model metadata for `deepseek-v4-pro` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
```

### 2. 模型消息

```
I'll start by reading the snapshot to understand the matchup and draft.
```

### 3. 终端命令 · 退出码 0

```
/bin/zsh -lc 'cat ./snapshot.json'
```

### 4. 命令输出

```
{"phase": "draft-lock", "series_time_utc": "2026-10-15T23:00:00+00:00", "current": {"event": "worlds-2026-play-in", "stage": "Round 1", "series": "worlds-2026-play-in-round-1-2", "n": 2, "patch": "26.20", "bo": 5, "blue": "MVK Esports", "red": "FURIA", "starters": {"blue": ["Chika", "Gury", "Harky", "Kratos", "SiuLoong"], "red": ["Ayu", "Guigo", "JoJo", "Tatu", "Tutsz"]}, "draft_rule": "Fearless", "bp": [{"turn": 1, "side": "blue", "action": "ban", "champion": "Ezreal"}, {"turn": 2, "side": "red", "action": "ban", "champion": "Nocturne"}, {"turn": 3, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 4, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 5, "side": "blue", "action": "ban", "champion": "Akali"}, {"turn": 6, "side": "red", "action": "ban", "champion": "Caitlyn"}, {"turn": 7, "side": "blue", "action": "pick", "champion": "Lucian"}, {"turn": 8, "side": "red", "action": "pick", "champion": "Xayah"}, {"turn": 9, "side": "red", "action": "pick", "champion": "Rakan"}, {"turn": 10, "side": "blue", "action": "pick", "champion": "Milio"}, {"turn": 11, "side": "blue", "action": "pick", "champion": "Lee Sin"}, {"turn": 12, "side": "red", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "red", "action": "ban", "champion": "Locke"}, {"turn": 14, "side": "blue", "action": "ban", "champion": "Pantheon"}, {"turn": 15, "side": "red", "action": "ban", "champion": "LeBlanc"}, {"turn": 16, "side": "blue", "action": "ban", "champion": "Ambessa"}, {"turn": 17, "side": "red", "action": "pick", "champion": "Wukong"}, {"turn": 18, "side": "blue", "action": "pick", "champion": "Rumble"}, {"turn": 19, "side": "blue", "action": "pick", "champion": "Viktor"}, {"turn": 20, "side": "red", "action": "pick", "champion": "Ornn"}]}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yorick"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Yorick", "k": 2, "d": 1, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 1, "d": 5, "a": 5}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 3, "d": 1, "a": 7}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 5, "d": 5, "a": 4}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 10}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Jayce", "k": 1, "d": 1, "a": 5}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 1, "d": 6, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Orianna", "k": 7, "d": 0, "a": 1}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Lucian", "k": 2, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Milio", "k": 1, "d": 2, "a": 10}]}, {"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 2, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": false, "blue_gd15": -1351, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Trundle"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ashe"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Ryze"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Lee Sin"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Camille"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Nautilus"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Galio"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Naafiri"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Maokai"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Ezreal"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Karma"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yone"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Camille", "k": 1, "d": 6, "a": 2}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Maokai", "k": 1, "d": 2, "a": 6}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Yone", "k": 1, "d": 2, "a": 4}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Ashe", "k": 4, "d": 3, "a": 1}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Seraphine", "k": 1, "d": 1, "a": 6}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Olaf", "k": 7, "d": 2, "a": 3}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Lee Sin", "k": 3, "d": 3, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Ryze", "k": 2, "d": 0, "a": 6}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Ezreal", "k": 1, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Karma", "k": 1, "d": 1, "a": 8}]}, {"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 3, "patch": "26.17", "blue": "Top Esports", "red": "Invictus Gaming", "blue_win": true, "blue_gd15": 2775, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Ahri"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Vi"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Galio"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Viktor"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Qiyana"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Locke"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Jarvan IV"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Rumble"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Ambessa"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Nautilus"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Poppy"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Alistar"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Jhin"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Rell"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Corki"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Leona"}], "players": [{"name": "ZUIAN", "role": "Top", "side": "blue", "champion": "Ambessa", "k": 8, "d": 5, "a": 8}, {"name": "Tian", "role": "Jungle", "side": "blue", "champion": "Qiyana", "k": 4, "d": 3, "a": 12}, {"name": "Creme", "role": "Mid", "side": "blue", "champion": "Locke", "k": 13, "d": 2, "a": 8}, {"name": "JackeyLove", "role": "Bot", "side": "blue", "champion": "Jhin", "k": 4, "d": 1, "a": 18}, {"name": "Zhuo", "role": "Support", "side": "blue", "champion": "Leona", "k": 0, "d": 2, "a": 17}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "Rumble", "k": 2, "d": 6, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Jarvan IV", "k": 3, "d": 4, "a": 8}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Viktor", "k": 5, "d": 4, "a": 6}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Corki", "k": 2, "d": 7, "a": 4}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Rell", "k": 1, "d": 8, "a": 10}]}, {"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 4, "patch": "26.17", "blue": "Top Esports", "red": "Invictus Gaming", "blue_win": true, "blue_gd15": 898, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Naafiri"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Poppy"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Neeko"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Vi"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Kalista"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Renata Glasc"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Aphelios"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Thresh"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Pantheon"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Taliyah"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Vayne"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Aurora"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Ahri"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Annie"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Gnar"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Galio"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Renekton"}], "players": [{"name": "ZUIAN", "role": "Top", "side": "blue", "champion": "Renekton", "k": 3, "d": 5, "a": 10}, {"name": "Tian", "role": "Jungle", "side": "blue", "champion": "Pantheon", "k": 8, "d": 1, "a": 11}, {"name": "Creme", "role": "Mid", "side": "blue", "champion": "Annie", "k": 5, "d": 3, "a": 13}, {"name": "JackeyLove", "role": "Bot", "side": "blue", "champion": "Kalista", "k": 7, "d": 2, "a": 10}, {"name": "Zhuo", "role": "Support", "side": "blue", "champion": "Renata Glasc", "k": 0, "d": 2, "a": 13}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "Gnar", "k": 3, "d": 2, "a": 4}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Vi", "k": 1, "d": 7, "a": 6}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Galio", "k": 2, "d": 6, "a": 8}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Aphelios", "k": 7, "d": 4, "a": 2}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Thresh", "k": 0, "d": 4, "a": 8}]}, {"series": "lpl-2026-regional-finals-round-1-2", "series_time": "2026-09-18T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Team WE", "red": "JD Gaming", "blue_win": true, "blue_gd15": -3500, "bp": [{"turn": 1, "side": "blue", "action": "ban", "champion": "Orianna"}, {"turn": 2, "side": "red", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "blue", "action": "ban", "champion": "Poppy"}, {"turn": 4, "side": "red", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "blue", "action": "ban", "champion": "Akali"}, {"turn": 6, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 7, "side": "blue", "action": "pick", "champion": "Vi"}, {"turn": 8, "side": "red", "action": "pick", "champion": "Rumble"}, {"turn": 9, "side": "red", "action": "pick", "champion": "Qiyana"}, {"turn": 10, "side": "blue", "action": "pick", "champion": "Ahri"}, {"turn": 11, "side": "blue", "action": "pick", "champion": "Ezreal"}, {"turn": 12, "side": "red", "action": "pick", "champion": "Aurora"}, {"turn": 13, "side": "red", "action": "ban", "champion": "Neeko"}, {"turn": 14, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 15, "side": "red", "action": "ban", "champion": "Bard"}, {"turn": 16, "side": "blue", "action": "ban", "champion": "Alistar"}, {"turn": 17, "side": "red", "action": "pick", "champion": "Jhin"}, {"turn": 18, "side": "blue", "action": "pick", "champion": "Galio"}, {"turn": 19, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 20, "side": "red", "action": "pick", "champion": "Nautilus"}], "players": [{"name": "Cube", "role": "Top", "side": "blue", "champion": "Galio", "k": 0, "d": 2, "a": 10}, {"name": "Monki", "role": "Jungle", "side": "blue", "champion": "Vi", "k": 6, "d": 1, "a": 5}, {"name": "Karis", "role": "Mid", "side": "blue", "champion": "Ahri", "k": 4, "d": 0, "a": 9}, {"name": "About", "role": "Bot", "side": "blue", "champion": "Ezreal", "k": 5, "d": 1, "a": 8}, {"name": "Erha", "role": "Support", "side": "blue", "champion": "Seraphine", "k": 2, "d": 1, "a": 14}, {"name": "Xiaoxu", "role": "Top", "side": "red", "champion": "Rumble", "k": 2, "d": 5, "a": 1}, {"name": "JunJia", "role": "Jungle", "side": "red", "champion": "Qiyana", "k": 1, "d": 3, "a": 2}, {"name": "HongQ", "role": "Mid", "side": "red", "champion": "Aurora", "k": 0, "d": 5, "a": 3}, {"name": "GALA", "role": "Bot", "side": "red", "champion": "Jhin", "k": 2, "d": 0, "a": 2}, {"name": "Vampire", "role": "Support", "side": "red", "champion": "Nautilus", "k": 0, "d": 4, "a": 3}]}, {"series": "lpl-2026-regional-finals-round-1-2", "series_time": "2026-09-18T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 2, "patch": "26.17", "blue": "JD Gaming", "red": "Team WE", "blue_win": true, "blue_gd15": 3715, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Orianna"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Lee Sin"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Annie"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Viktor"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Naafiri"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Gnar"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Wukong"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Gwen"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Trundle"}, {"turn": 18, "side": "red", "action": "pick", "champion": "K'Sante"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Ambessa"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Ambessa", "k": 3, "d": 1, "a": 4}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Trundle", "k": 4, "d": 0, "a": 6}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Viktor", "k": 1, "d": 2, "a": 7}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 2, "d": 0, "a": 1}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 4}, {"name": "Cube", "role": "Top", "side": "red", "champion": "K'Sante", "k": 0, "d": 3, "a": 1}, {"name": "Monki", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 3, "d": 4, "a": 0}, {"name": "Karis", "role": "Mid", "side": "red", "champion": "Annie", "k": 0, "d": 1, "a": 3}, {"name": "About", "role": "Bot", "side": "red", "champion": "Lucian", "k": 0, "d": 1, "a": 1}, {"name": "Erha", "role": "Support", "side": "red", "champion": "Milio", "k": 0, "d": 1, "a": 2}]}, {"series": "lpl-2026-regional-finals-round-1-2", "series_time": "2026-09-18T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 3, "patch": "26.17", "blue": "Team WE", "red": "JD Gaming", "blue_win": false, "blue_gd15": -2080, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Neeko"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Orianna"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Wukong"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Kalista"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Nocturne"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ryze"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Jarvan IV"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Twisted Fate"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Sion"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Caitlyn"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Jinx"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Alistar"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Zeri"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Rakan"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Xayah"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Renata Glasc"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Sivir"}], "players": [{"name": "Cube", "role": "Top", "side": "blue", "champion": "Sion", "k": 2, "d": 4, "a": 3}, {"name": "Monki", "role": "Jungle", "side": "blue", "champion": "Jarvan IV", "k": 1, "d": 5, "a": 5}, {"name": "Karis", "role": "Mid", "side": "blue", "champion": "Ryze", "k": 1, "d": 4, "a": 5}, {"name": "About", "role": "Bot", "side": "blue", "champion": "Sivir", "k": 2, "d": 4, "a": 4}, {"name": "Erha", "role": "Support", "side": "blue", "champion": "Rakan", "k": 0, "d": 3, "a": 6}, {"name": "Xiaoxu", "role": "Top", "side": "red", "champion": "Olaf", "k": 7, "d": 1, "a": 5}, {"name": "JunJia", "role": "Jungle", "side": "red", "champion": "Nocturne", "k": 3, "d": 2, "a": 10}, {"name": "HongQ", "role": "Mid", "side": "red", "champion": "Twisted Fate", "k": 4, "d": 1, "a": 11}, {"name": "GALA", "role": "Bot", "side": "red", "champion": "Xayah", "k": 6, "d": 0, "a": 8}, {"name": "Vampire", "role": "Support", "side": "red", "champion": "Renata Glasc", "k": 0, "d": 2, "a": 16}]}, {"series": "lpl-2026-regional-finals-round-1-2", "series_time": "2026-09-18T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 4, "patch": "26.17", "blue": "JD Gaming", "red": "Team WE", "blue_win": true, "blue_gd15": -1804, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Caitlyn"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Orianna"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Neeko"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Syndra"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Akali"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Maokai"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Jinx"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Renekton"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Corki"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Gnar"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Varus"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Thresh"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Ziggs"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Locke"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Sylas"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Ashe"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Braum"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Alistar"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Gnar", "k": 1, "d": 1, "a": 11}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 3, "d": 3, "a": 16}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Sylas", "k": 2, "d": 3, "a": 14}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Jinx", "k": 15, "d": 0, "a": 5}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Alistar", "k": 0, "d": 3, "a": 21}, {"name": "Cube", "role": "Top", "side": "red", "champion": "Renekton", "k": 1, "d": 5, "a": 3}, {"name": "Monki", "role": "Jungle", "side": "red", "champion": "Maokai", "k": 0, "d": 6, "a": 5}, {"name": "Karis", "role": "Mid", "side": "red", "champion": "Corki", "k": 7, "d": 2, "a": 2}, {"name": "About", "role": "Bot", "side": "red", "champion": "Ashe", "k": 1, "d": 4, "a": 9}, {"name": "Erha", "role": "Support", "side": "red", "champion": "Braum", "k": 1, "d": 4, "a": 8}]}, {"series": "lpl-2026-regional-finals-round-2-1", "series_time": "2026-09-19T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "JD Gaming", "red": "Invictus Gaming", "blue_win": false, "blue_gd15": 232, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Vi"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Lee Sin"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Lulu"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Orianna"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Syndra"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Tristana"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Vayne"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Cho'Gath"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Maokai"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Gnar"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Ambessa"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Ambessa", "k": 1, "d": 1, "a": 0}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Cho'Gath", "k": 1, "d": 4, "a": 2}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Orianna", "k": 1, "d": 2, "a": 0}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 0, "d": 1, "a": 1}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Seraphine", "k": 0, "d": 3, "a": 1}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "Gnar", "k": 0, "d": 1, "a": 5}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Maokai", "k": 1, "d": 1, "a": 6}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Syndra", "k": 4, "d": 1, "a": 5}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Tristana", "k": 6, "d": 0, "a": 2}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Lulu", "k": 0, "d": 0, "a": 9}]}, {"series": "lpl-2026-regional-finals-round-2-1", "series_time": "2026-09-19T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 2, "patch": "26.17", "blue": "JD Gaming", "red": "Invictus Gaming", "blue_win": false, "blue_gd15": -4965, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Vi"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Poppy"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Lucian"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Qiyana"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Renata Glasc"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Rumble"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Ezreal"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Karma"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Kalista"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Annie"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Viktor"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Galio"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Trundle"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "K'Sante"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Aurora"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Twisted Fate"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Rumble", "k": 1, "d": 2, "a": 6}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 2, "d": 5, "a": 5}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Twisted Fate", "k": 2, "d": 4, "a": 2}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Kalista", "k": 4, "d": 4, "a": 4}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Renata Glasc", "k": 1, "d": 5, "a": 7}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "K'Sante", "k": 1, "d": 2, "a": 13}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Qiyana", "k": 5, "d": 1, "a": 10}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Aurora", "k": 5, "d": 2, "a": 11}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Ezreal", "k": 9, "d": 4, "a": 5}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Karma", "k": 0, "d": 1, "a": 15}]}, {"series": "lpl-2026-regional-finals-round-2-1", "series_time": "2026-09-19T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 3, "patch": "26.17", "blue": "Invictus Gaming", "red": "JD Gaming", "blue_win": false, "blue_gd15": -423, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Lee Sin"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Lucian"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Trundle"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ryze"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Naafiri"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Jinx"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Thresh"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Jayce"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Olaf"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Caitlyn"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Yorick"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Ziggs"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Jhin"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Renekton"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Viktor"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Nautilus"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Jayce", "k": 2, "d": 8, "a": 4}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Naafiri", "k": 4, "d": 4, "a": 9}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Ryze", "k": 6, "d": 3, "a": 8}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Jhin", "k": 4, "d": 5, "a": 8}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Nautilus", "k": 0, "d": 7, "a": 11}, {"name": "Xiaoxu", "role": "Top", "side": "red", "champion": "Renekton", "k": 3, "d": 6, "a": 6}, {"name": "JunJia", "role": "Jungle", "side": "red", "champion": "Trundle", "k": 11, "d": 1, "a": 11}, {"name": "HongQ", "role": "Mid", "side": "red", "champion": "Viktor", "k": 6, "d": 2, "a": 8}, {"name": "GALA", "role": "Bot", "side": "red", "champion": "Jinx", "k": 6, "d": 3, "a": 9}, {"name": "Vampire", "role": "Support", "side": "red", "champion": "Thresh", "k": 0, "d": 4, "a": 19}]}, {"series": "lpl-2026-regional-finals-round-2-1", "series_time": "2026-09-19T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 4, "patch": "26.17", "blue": "JD Gaming", "red": "Invictus Gaming", "blue_win": false, "blue_gd15": 3731, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Poppy"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Xayah"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Lucian"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Vi"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Pantheon"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Akali"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Alistar"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Ahri"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Jax"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Kennen"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Bard"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Gragas"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Kai'Sa"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Rakan"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Sivir"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Dr. Mundo"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Aphelios"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Jax", "k": 3, "d": 6, "a": 5}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Pantheon", "k": 6, "d": 4, "a": 7}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Akali", "k": 3, "d": 6, "a": 8}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Aphelios", "k": 6, "d": 4, "a": 3}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Rakan", "k": 1, "d": 5, "a": 11}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "Dr. Mundo", "k": 5, "d": 5, "a": 8}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Vi", "k": 6, "d": 3, "a": 12}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Ahri", "k": 6, "d": 2, "a": 12}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Sivir", "k": 7, "d": 6, "a": 12}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Alistar", "k": 1, "d": 4, "a": 17}]}, {"series": "worlds-2026-play-in-round-1-2", "series_time": "2026-10-15T23:00:00+00:00", "event": "worlds-2026-play-in", "n": 1, "patch": "26.20", "blue": "MVK Esports", "red": "FURIA", "blue_win": true, "blue_gd15": -947, "bp": [{"turn": 1, "side": "blue", "action": "ban", "champion": "Ezreal"}, {"turn": 2, "side": "red", "action": "ban", "champion": "Pyke"}, {"turn": 3, "side": "blue", "action": "ban", "champion": "Pantheon"}, {"turn": 4, "side": "red", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "blue", "action": "ban", "champion": "Akali"}, {"turn": 6, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 7, "side": "blue", "action": "pick", "champion": "Olaf"}, {"turn": 8, "side": "red", "action": "pick", "champion": "Yunara"}, {"turn": 9, "side": "red", "action": "pick", "champion": "Lulu"}, {"turn": 10, "side": "blue", "action": "pick", "champion": "Ashe"}, {"turn": 11, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 12, "side": "red", "action": "pick", "champion": "Trundle"}, {"turn": 13, "side": "red", "action": "ban", "champion": "Maokai"}, {"turn": 14, "side": "blue", "action": "ban", "champion": "Sylas"}, {"turn": 15, "side": "red", "action": "ban", "champion": "Lee Sin"}, {"turn": 16, "side": "blue", "action": "ban", "champion": "Locke"}, {"turn": 17, "side": "red", "action": "pick", "champion": "Jax"}, {"turn": 18, "side": "blue", "action": "pick", "champion": "Cassiopeia"}, {"turn": 19, "side": "blue", "action": "pick", "champion": "Vi"}, {"turn": 20, "side": "red", "action": "pick", "champion": "Galio"}], "players": [{"name": "Kratos", "role": "Top", "side": "blue", "champion": "Olaf", "k": 2, "d": 2, "a": 1}, {"name": "Gury", "role": "Jungle", "side": "blue", "champion": "Vi", "k": 2, "d": 2, "a": 7}, {"name": "Chika", "role": "Mid", "side": "blue", "champion": "Cassiopeia", "k": 6, "d": 3, "a": 1}, {"name": "Harky", "role": "Bot", "side": "blue", "champion": "Ashe", "k": 0, "d": 1, "a": 8}, {"name": "SiuLoong", "role": "Support", "side": "blue", "champion": "Seraphine", "k": 1, "d": 2, "a": 6}, {"name": "Guigo", "role": "Top", "side": "red", "champion": "Jax", "k": 4, "d": 4, "a": 2}, {"name": "Tatu", "role": "Jungle", "side": "red", "champion": "Trundle", "k": 3, "d": 1, "a": 3}, {"name": "Tutsz", "role": "Mid", "side": "red", "champion": "Galio", "k": 1, "d": 2, "a": 6}, {"name": "Ayu", "role": "Bot", "side": "red", "champion": "Yunara", "k": 2, "d": 4, "a": 3}, {"name": "JoJo", "role": "Support", "side": "red", "champion": "Lulu", "k": 0, "d": 0, "a": 6}]}], "coverage": {"history_games": 13, "starters": [{"side": "blue", "name": "Chika", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Gury", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Harky", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "Kratos", "games": 1, "same_patch_games": 1}, {"side": "blue", "name": "SiuLoong", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Ayu", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Guigo", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "JoJo", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Tatu", "games": 1, "same_patch_games": 1}, {"side": "red", "name": "Tutsz", "games": 1, "same_patch_games": 1}], "starters_with_history": 10, "coverage_group": "all", "previous_series_games": [1], "missing_previous_series_games": []}}
```

### 5. 模型消息

```
Let me parse the full snapshot with Python for a detailed look.
```

### 6. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 - <<'EOF'
import json
snap = json.load(open('snapshot.json'))
print(\"history games:\", len(snap['history']))
for g in snap['history']:
    print(g['series'], 'n=',g['n'], g['patch'], g['blue'], 'vs', g['red'], 'win=', g.get('blue_win'), 'gd15=', g.get('blue_gd15'))
EOF"
```

### 7. 命令输出

```
history games: 13
lpl-2026-regional-finals-round-1-1 n= 1 26.17 Invictus Gaming vs Top Esports win= True gd15= -38
lpl-2026-regional-finals-round-1-1 n= 2 26.17 Invictus Gaming vs Top Esports win= False gd15= -1351
lpl-2026-regional-finals-round-1-1 n= 3 26.17 Top Esports vs Invictus Gaming win= True gd15= 2775
lpl-2026-regional-finals-round-1-1 n= 4 26.17 Top Esports vs Invictus Gaming win= True gd15= 898
lpl-2026-regional-finals-round-1-2 n= 1 26.17 Team WE vs JD Gaming win= True gd15= -3500
lpl-2026-regional-finals-round-1-2 n= 2 26.17 JD Gaming vs Team WE win= True gd15= 3715
lpl-2026-regional-finals-round-1-2 n= 3 26.17 Team WE vs JD Gaming win= False gd15= -2080
lpl-2026-regional-finals-round-1-2 n= 4 26.17 JD Gaming vs Team WE win= True gd15= -1804
lpl-2026-regional-finals-round-2-1 n= 1 26.17 JD Gaming vs Invictus Gaming win= False gd15= 232
lpl-2026-regional-finals-round-2-1 n= 2 26.17 JD Gaming vs Invictus Gaming win= False gd15= -4965
lpl-2026-regional-finals-round-2-1 n= 3 26.17 Invictus Gaming vs JD Gaming win= False gd15= -423
lpl-2026-regional-finals-round-2-1 n= 4 26.17 JD Gaming vs Invictus Gaming win= False gd15= 3731
worlds-2026-play-in-round-1-2 n= 1 26.20 MVK Esports vs FURIA win= True gd15= -947
```

### 8. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 - <<'EOF'
import json
snap = json.load(open('snapshot.json'))
# game 1 of this series
g1 = [g for g in snap['history'] if g['series']=='worlds-2026-play-in-round-1-2']
print(json.dumps(g1, indent=1))
EOF"
```

### 9. 命令输出

```
[
 {
  "series": "worlds-2026-play-in-round-1-2",
  "series_time": "2026-10-15T23:00:00+00:00",
  "event": "worlds-2026-play-in",
  "n": 1,
  "patch": "26.20",
  "blue": "MVK Esports",
  "red": "FURIA",
  "blue_win": true,
  "blue_gd15": -947,
  "bp": [
   {
    "turn": 1,
    "side": "blue",
    "action": "ban",
    "champion": "Ezreal"
   },
   {
    "turn": 2,
    "side": "red",
    "action": "ban",
    "champion": "Pyke"
   },
   {
    "turn": 3,
    "side": "blue",
    "action": "ban",
    "champion": "Pantheon"
   },
   {
    "turn": 4,
    "side": "red",
    "action": "ban",
    "champion": "Nocturne"
   },
   {
    "turn": 5,
    "side": "blue",
    "action": "ban",
    "champion": "Akali"
   },
   {
    "turn": 6,
    "side": "red",
    "action": "ban",
    "champion": "Jarvan IV"
   },
   {
    "turn": 7,
    "side": "blue",
    "action": "pick",
    "champion": "Olaf"
   },
   {
    "turn": 8,
    "side": "red",
    "action": "pick",
    "champion": "Yunara"
   },
   {
    "turn": 9,
    "side": "red",
    "action": "pick",
    "champion": "Lulu"
   },
   {
    "turn": 10,
    "side": "blue",
    "action": "pick",
    "champion": "Ashe"
   },
   {
    "turn": 11,
    "side": "blue",
    "action": "pick",
    "champion": "Seraphine"
   },
   {
    "turn": 12,
    "side": "red",
    "action": "pick",
    "champion": "Trundle"
   },
   {
    "turn": 13,
    "side": "red",
    "action": "ban",
    "champion": "Maokai"
   },
   {
    "turn": 14,
    "side": "blue",
    "action": "ban",
    "champion": "Sylas"
   },
   {
    "turn": 15,
    "side": "red",
    "action": "ban",
    "champion": "Lee Sin"
   },
   {
    "turn": 16,
    "side": "blue",
    "action": "ban",
    "champion": "Locke"
   },
   {
    "turn": 17,
    "side": "red",
    "action": "pick",
    "champion": "Jax"
   },
   {
    "turn": 18,
    "side": "blue",
    "action": "pick",
    "champion": "Cassiopeia"
   },
   {
    "turn": 19,
    "side": "blue",
    "action": "pick",
    "champion": "Vi"
   },
   {
    "turn": 20,
    "side": "red",
    "action": "pick",
    "champion": "Galio"
   }
  ],
  "players": [
   {
    "name": "Kratos",
    "role": "Top",
    "side": "blue",
    "champion": "Olaf",
    "k": 2,
    "d": 2,
    "a": 1
   },
   {
    "name": "Gury",
    "role": "Jungle",
    "side": "blue",
    "champion": "Vi",
    "k": 2,
    "d": 2,
    "a": 7
   },
   {
    "name": "Chika",
    "role": "Mid",
    "side": "blue",
    "champion": "Cassiopeia",
    "k": 6,
    "d": 3,
    "a": 1
   },
   {
    "name": "Harky",
    "role": "Bot",
    "side": "blue",
    "champion": "Ashe",
    "k": 0,
    "d": 1,
    "a": 8
   },
   {
    "name": "SiuLoong",
    "role": "Support",
    "side": "blue",
    "champion": "Seraphine",
    "k": 1,
    "d": 2,
    "a": 6
   },
   {
    "name": "Guigo",
    "role": "Top",
    "side": "red",
    "champion": "Jax",
    "k": 4,
    "d": 4,
    "a": 2
   },
   {
    "name": "Tatu",
    "role": "Jungle",
    "side": "red",
    "champion": "Trundle",
    "k": 3,
    "d": 1,
    "a": 3
   },
   {
    "name": "Tutsz",
    "role": "Mid",
    "side": "red",
    "champion": "Galio",
    "k": 1,
    "d": 2,
    "a": 6
   },
   {
    "name": "Ayu",
    "role": "Bot",
    "side": "red",
    "champion": "Yunara",
    "k": 2,
    "d": 4,
    "a": 3
   },
   {
    "name": "JoJo",
    "role": "Support",
    "side": "red",
    "champion": "Lulu",
    "k": 0,
    "d": 0,
    "a": 6
   }
  ]
 }
]
```

### 10. 模型消息

```
I've reviewed the data. Now writing the initial forecast.
```

### 11. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 - <<'EOF'
import json
pred = {\"p_blue_win\": 0.60, \"p_blue_ahead_15\": 0.55}
json.dump(pred, open('prediction.json','w'))
print(open('prediction.json').read())
EOF"
```

### 12. 命令输出

```
{"p_blue_win": 0.6, "p_blue_ahead_15": 0.55}
```

### 13. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 - <<'EOF'
import json
snap = json.load(open('snapshot.json'))
hist = snap['history']
blue_wins = sum(g['blue_win'] for g in hist)
print(\"blue win rate:\", blue_wins, \"/\", len(hist), \"=\", round(blue_wins/len(hist),3))
# ahead at 15
ahead = [g['blue_gd15']>0 for g in hist if g.get('blue_gd15') is not None]
print(\"blue ahead15:\", sum(ahead), \"/\", len(ahead), \"=\", round(sum(ahead)/len(ahead),3))
# champion win stats across history (patch 26.17 mostly)
from collections import defaultdict
champ = defaultdict(lambda:[0,0])
for g in hist:
    for p in g.get('players',[]):
        w = (g['blue_win'] and p['side']=='blue') or ((not g['blue_win']) and p['side']=='red')
        champ[p['champion']][1]+=1
        champ[p['champion']][0]+=1 if w else 0
for c in ['Lucian','Milio','Lee Sin','Rumble','Viktor','Xayah','Rakan','Syndra','Wukong','Ornn']:
    w,n = champ[c]
    print(c, f\"{w}/{n}\", round(w/n,3) if n else '-')
EOF"
```

### 14. 命令输出

```
blue win rate: 7 / 13 = 0.538
blue ahead15: 5 / 13 = 0.385
Lucian 0/2 0.0
Milio 0/2 0.0
Lee Sin 1/1 1.0
Rumble 0/3 0.0
Viktor 2/3 0.667
Xayah 1/1 1.0
Rakan 0/2 0.0
Syndra 2/2 1.0
Wukong 0/0 -
Ornn 0/0 -
```

### 15. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 - <<'EOF'
import json
pred = {\"p_blue_win\": 0.58, \"p_blue_ahead_15\": 0.53}
json.dump(pred, open('prediction.json','w'))
print(open('prediction.json').read())
EOF"
```

### 16. 命令输出

```
{"p_blue_win": 0.58, "p_blue_ahead_15": 0.53}
```

### 17. 模型消息

````
Forecast saved to `prediction.json`:

```json
{"p_blue_win": 0.58, "p_blue_ahead_15": 0.53}
```

**Reasoning**
- The only direct evidence is game 1 of this series (same teams, sides, patch): MVK won as blue despite being -947 gold at 15, so I lean MVK but temper the early-lead probability.
- MVK's game 2 draft (`Lucian`/`Milio`, `Lee Sin`, `Rumble`) is early-game oriented, nudging `p_blue_ahead_15` above neutral despite game 1's deficit.
- FURIA's comp (`Xayah`/`Rakan`, `Syndra`, `Wukong`, `Ornn`) scales well, and the loser of game 1 often adjusts, so I keep MVK's edge modest.
````
