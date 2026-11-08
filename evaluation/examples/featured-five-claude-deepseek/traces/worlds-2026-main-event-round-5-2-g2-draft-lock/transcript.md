# LØS vs LYON · G2 · BP 锁定

worlds-2026-main-event · Round 5 · 26.20 · BO3

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/worlds-2026-main-event-round-5-2-g2-draft-lock/trajectory.jsonl) · [stderr](../../jobs/worlds-2026-main-event-round-5-2-g2-draft-lock/stderr.txt) · [交卷文件](../../jobs/worlds-2026-main-event-round-5-2-g2-draft-lock/prediction.json)

## 输入与可查询证据

蓝方首发为 Ackerman, Curse, Duduhh, Feisty, Zest。

红方首发为 Berserker, Dhokla, Inspired, Isles, Saint。

冻结时可查 79 个历史小局，10 名首发有历史出场记录。

本局可见 20 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.5,
    "p_blue_ahead_15": 0.64
  },
  "observed_outcome": {
    "p_blue_win": 0,
    "p_blue_ahead_15": 1
  },
  "brier": {
    "p_blue_win": 0.25,
    "p_blue_ahead_15": 0.1296
  },
  "reward": 0.8102
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 29636,
  "cache_creation_input_tokens": 0,
  "cache_read_input_tokens": 605184,
  "output_tokens": 32385
}
```

## 执行轨迹

### 1. 工具调用 · Read

```
{
  "file_path": "[ephemeral]/app/snapshot.json"
}
```

### 2. 工具结果

```
1	{"phase": "draft-lock", "series_time_utc": "2026-10-31T18:59:00+00:00", "current": {"event": "worlds-2026-main-event", "stage": "Round 5", "series": "worlds-2026-main-event-round-5-2", "n": 2, "patch": "26.20", "bo": 3, "blue": "LØS", "red": "LYON", "starters": {"blue": ["Ackerman", "Curse", "Duduhh", "Feisty", "Zest"], "red": ["Berserker", "Dhokla", "Inspired", "Isles", "Saint"]}, "draft_rule": "Fearless", "bp": [{"turn": 1, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 2, "side": "red", "action": "ban", "champion": "Nocturne"}, {"turn": 3, "side": "blue", "action": "ban", "champion": "Wukong"}, {"turn": 4, "side": "red", "action": "ban", "champion": "Seraphine"}, {"turn": 5, "side": "blue", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "red", "action": "ban", "champion": "Jayce"}, {"turn": 7, "side": "blue", "action": "pick", "champion": "Qiyana"}, {"turn": 8, "side": "red", "action": "pick", "champion": "Yunara"}, {"turn": 9, "side": "red", "action": "pick", "champion": "Lulu"}, {"turn": 10, "side": "blue", "action": "pick", "champion": "Caitlyn"}, {"turn": 11, "side": "blue", "action": "pick", "champion": "Karma"}, {"turn": 12, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 13, "side": "red", "action": "ban", "champion": "Viktor"}, {"turn": 14, "side": "blue", "action": "ban", "champion": "Xin Zhao"}, {"turn": 15, "side": "red", "action": "ban", "champion": "Taliyah"}, {"turn": 16, "side": "blue", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "red", "action": "pick", "champion": "Lee Sin"}, {"turn": 18, "side": "blue", "action": "pick", "champion": "Ambessa"}, {"turn": 19, "side": "blue", "action": "pick", "champion": "LeBlanc"}, {"turn": 20, "side": "red", "action": "pick", "champion": "Gnar"}]}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yorick"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Yorick", "k": 2, "d": 1, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 1, "d": 5, "a": 5}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 3, "d": 1, "a": 7}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 5, "d": 5, "a": 4}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 10}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Jayce", "k": 1, "d": 1, "a": 5}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 1, "d": 6, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Orianna", "k": 7, "d": 0, "a": 1}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Lucian", "k": 2, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Milio", "k": 1, "d": 2, "a": 10}]}, {"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 2, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": false, "blue_gd15": -1351, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Trundle"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ashe"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Ryze"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Lee Sin"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Camille"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Nautilus"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Galio"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Naafiri"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Maokai"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Ezreal"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Karma"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yone"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Camille", "k": 1, "d": 6, "a": 2}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Maokai", "k": 1, "d": 2, "a": 6}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Yone", "k": 1, "d": 2, "a": 4}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Ashe", "k": 4, "d": 3, "a": 1}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Seraphine", "k": 1, "d": 1, "a": 6}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Olaf", "k": 7, "d": 2, "a": 3}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Lee Sin", "k": 3, "d": 3, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Ryze", "k": 2, "d": 0, "a": 6}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Ezreal", "k": 1, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Karma", "k": 1, "d": 1, "a": 8}]}, {"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 3, "patch": "26.17", "blue": "Top Esports", "red": "Invictus Gaming", "blue_win": true, "blue_gd15": 2775, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Ahri"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Vi"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Galio"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Viktor"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Qiyana"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Locke"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Jarvan IV"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Rumble"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Ambessa"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Nautilus"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Poppy"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Alistar"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Jhin"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Rell"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Corki"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Leona"}], "players": [{"name": "ZUIAN", "role": "Top", "side": "blue", "champion": "Ambessa", "k": 8, "d": 5, "a": 8}, {"name": "Tian", "role": "Jungle", "side": "blue", "champion": "Qiyana", "k": 4, "d": 3, "a": 12}, {"name": "Creme", "role": "Mid", "side": "blue", "champion": "Locke", "k": 13, "d": 2, "a": 8}, {"name": "JackeyLove", "role": "Bot", "side": "blue", "champion": "Jhin", "k": 4, "d": 1, "a": 18}, {"name": "Zhuo", "role": "Support", "side": "blue", "champion": "Leona", "k": 0, "d": 2, "a": 17}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "Rumble", "k": 2, "d": 6, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Jarvan IV", "k": 3, "d": 4, "a": 8}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Viktor", "k": 5, "d": 4, "a": 6}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Corki", "k": 2, "d": 7, "a": 4}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Rell", "k": 1, "d": 8, "a": 10}]}, {"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 4, "patch": "26.17", "blue": "Top Esports", "red": "Invictus Gaming", "blue_win": true, "blue_gd15": 898, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Naafiri"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Poppy"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Neeko"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Vi"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Kalista"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Renata Glasc"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Aphelios"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Thresh"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Pantheon"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Taliyah"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Vayne"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Aurora"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Ahri"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Annie"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Gnar"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Galio"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Renekton"}], "players": [{"name": "ZUIAN", "role": "Top", "side": "blue", "champion": "Renekton", "k": 3, "d": 5, "a": 10}, {"name": "Tian", "role": "Jungle", "side": "blue", "champion": "Pantheon", "k": 8, "d": 1, "a": 11}, {"name": "Creme", "role": "Mid", "side": "blue", "champion": "Annie", "k": 5, "d": 3, "a": 13}, {"name": "JackeyLove", "role": "Bot", "side": "blue", "champion": "Kalista", "k": 7, "d": 2, "a": 10}, {"name": "Zhuo", "role": "Support", "side": "blue", "champion": "Renata Glasc", "k": 0, "d": 2, "a": 13}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "Gnar", "k": 3, "d": 2, "a": 4}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Vi", "k": 1, "d": 7, "a": 6}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Galio", "k": 2, "d": 6, "a": 8}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Aphelios", "k": 7, "d": 4, "a": 2}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Thresh", "k": 0, "d": 4, "a": 8}]}, {"series": "lpl-2026-regional-finals-round-1-2", "series_time": "2026-09-18T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Team WE", "red": "JD Gaming", "blue_win": true, "blue_gd15": -3500, "bp": [{"turn": 1, "side": "blue", "action": "ban", "champion": "Orianna"}, {"turn": 2, "side": "red", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "blue", "action": "ban", "champion": "Poppy"}, {"turn": 4, "side": "red", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "blue", "action": "ban", "champion": "Akali"}, {"turn": 6, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 7, "side": "blue", "action": "pick", "champion": "Vi"}, {"turn": 8, "side": "red", "action": "pick", "champion": "Rumble"}, {"turn": 9, "side": "red", "action": "pick", "champion": "Qiyana"}, {"turn": 10, "side": "blue", "action": "pick", "champion": "Ahri"}, {"turn": 11, "side": "blue", "action": "pick", "champion": "Ezreal"}, {"turn": 12, "side": "red", "action": "pick", "champion": "Aurora"}, {"turn": 13, "side": "red", "action": "ban", "champion": "Neeko"}, {"turn": 14, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 15, "side": "red", "action": "ban", "champion": "Bard"}, {"turn": 16, "side": "blue", "action": "ban", "champion": "Alistar"}, {"turn": 17, "side": "red", "action": "pick", "champion": "Jhin"}, {"turn": 18, "side": "blue", "action": "pick", "champion": "Galio"}, {"turn": 19, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 20, "side": "red", "action": "pick", "champion": "Nautilus"}], "players": [{"name": "Cube", "role": "Top", "side": "blue", "champion": "Galio", "k": 0, "d": 2, "a": 10}, {"name": "Monki", "role": "Jungle", "side": "blue", "champion": "Vi", "k": 6, "d": 1, "a": 5}, {"name": "Karis", "role": "Mid", "side": "blue", "champion": "Ahri", "k": 4, "d": 0, "a": 9}, {"name": "About", "role": "Bot", "side": "blue", "champion": "Ezreal", "k": 5, "d": 1, "a": 8}, {"name": "Erha", "role": "Support", "side": "blue", "champion": "Seraphine", "k": 2, "d": 1, "a": 14}, {"name": "Xiaoxu", "role": "Top", "side": "red", "champion": "Rumble", "k": 2, "d": 5, "a": 1}, {"name": "JunJia", "role": "Jungle", "side": "red", "champion": "Qiyana", "k": 1, "d": 3, "a": 2}, {"name": "HongQ", "role": "Mid", "side": "red", "champion": "Aurora", "k": 0, "d": 5, "a": 3}, {"name": "GALA", "role": "Bot", "side": "red", "champion": "Jhin", "k": 2, "d": 0, "a": 2}, {"name": "Vampire", "role": "Support", "side": "red", "champion": "Nautilus", "k": 0, "d": 4, "a": 3}]}, {"series": "lpl-2026-regional-finals-round-1-2", "series_time": "2026-09-18T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 2, "patch": "26.17", "blue": "JD Gaming", "red": "Team WE", "blue_win": true, "blue_gd15": 3715, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Orianna"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Lee Sin"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Annie"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Viktor"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Naafiri"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Gnar"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Wukong"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Gwen"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Trundle"}, {"turn": 18, "side": "red", "action": "pick", "champion": "K'Sante"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Ambessa"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Ambessa", "k": 3, "d": 1, "a": 4}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Trundle", "k": 4, "d": 0, "a": 6}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Viktor", "k": 1, "d": 2, "a": 7}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 2, "d": 0, "a": 1}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 4}, {"name": "Cube", "role": "Top", "side": "red", "champion": "K'Sante", "k": 0, "d": 3, "a": 1}, {"name": "Monki", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 3, "d": 4, "a": 0}, {"name": "Karis", "role": "Mid", "side": "red", "champion": "Annie", "k": 0, "d": 1, "a": 3}, {"name": "About", "role": "Bot", "side": "red", "champion": "Lucian", "k": 0, "d": 1, "a": 1}, {"name": "Erha", "role": "Support", "side": "red", "champion": "Milio", "k": 0, "d": 1, "a": 2}]}, {"series": "lpl-2026-regional-finals-round-1-2", "series_time": "2026-09-18T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 3, "patch": "26.17", "blue": "Team WE", "red": "JD Gaming", "blue_win": false, "blue_gd15": -2080, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Neeko"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Orianna"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Wukong"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Kalista"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Nocturne"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ryze"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Jarvan IV"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Twisted Fate"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Sion"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Caitlyn"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Jinx"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Alistar"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Zeri"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Rakan"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Xayah"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Renata Glasc"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Sivir"}], "players": [{"name": "Cube", "role": "Top", "side": "blue", "champion": "Sion", "k": 2, "d": 4, "a": 3}, {"name": "Monki", "role": "Jungle", "side": "blue", "champion": "Jarvan IV", "k": 1, "d": 5, "a": 5}, {"name": "Karis", "role": "Mid", "side": "blue", "champion": "Ryze", "k": 1, "d": 4, "a": 5}, {"name": "About", "role": "Bot", "side": "blue", "champion": "Sivir", "k": 2, "d": 4, "a": 4}, {"name": "Erha", "role": "Support", "side": "blue", "champion": "Rakan", "k": 0, "d": 3, "a": 6}, {"name": "Xiaoxu", "role": "Top", "side": "red", "champion": "Olaf", "k": 7, "d": 1, "a": 5}, {"name": "JunJia", "role": "Jungle", "side": "red", "champion": "Nocturne", "k": 3, "d": 2, "a": 10}, {"name": "HongQ", "role": "Mid", "side": "red", "champion": "Twisted Fate", "k": 4, "d": 1, "a": 11}, {"name": "GALA", "role": "Bot", "side": "red", "champion": "Xayah", "k": 6, "d": 0, "a": 8}, {"name": "Vampire", "role": "Support", "side": "red", "champion": "Renata Glasc", "k": 0, "d": 2, "a": 16}]}, {"series": "lpl-2026-regional-finals-round-1-2", "series_time": "2026-09-18T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 4, "patch": "26.17", "blue": "JD Gaming", "red": "Team WE", "blue_win": true, "blue_gd15": -1804, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Caitlyn"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Orianna"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Neeko"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Syndra"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Akali"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Maokai"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Jinx"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Renekton"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Corki"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Gnar"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Varus"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Thresh"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Ziggs"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Locke"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Sylas"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Ashe"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Braum"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Alistar"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Gnar", "k": 1, "d": 1, "a": 11}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 3, "d": 3, "a": 16}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Sylas", "k": 2, "d": 3, "a": 14}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Jinx", "k": 15, "d": 0, "a": 5}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Alistar", "k": 0, "d": 3, "a": 21}, {"name": "Cube", "role": "Top", "side": "red", "champion": "Renekton", "k": 1, "d": 5, "a": 3}, {"name": "Monki", "role": "Jungle", "side": "red", "champion": "Maokai", "k": 0, "d": 6, "a": 5}, {"name": "Karis", "role": "Mid", "side": "red", "champion": "Corki", "k": 7, "d": 2, "a": 2}, {"name": "About", "role": "Bot", "side": "red", "champion": "Ashe", "k": 1, "d": 4, "a": 9}, {"name": "Erha", "role": "Support", "side": "red", "champion": "Braum", "k": 1, "d": 4, "a": 8}]}, {"series": "lpl-2026-regional-finals-round-2-1", "series_time": "2026-09-19T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "JD Gaming", "red": "Invictus Gaming", "blue_win": false, "blue_gd15": 232, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Vi"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Lee Sin"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Lulu"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Orianna"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Syndra"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Tristana"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Vayne"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Cho'Gath"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Maokai"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Gnar"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Ambessa"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Ambessa", "k": 1, "d": 1, "a": 0}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Cho'Gath", "k": 1, "d": 4, "a": 2}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Orianna", "k": 1, "d": 2, "a": 0}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 0, "d": 1, "a": 1}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Seraphine", "k": 0, "d": 3, "a": 1}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "Gnar", "k": 0, "d": 1, "a": 5}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Maokai", "k": 1, "d": 1, "a": 6}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Syndra", "k": 4, "d": 1, "a": 5}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Tristana", "k": 6, "d": 0, "a": 2}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Lulu", "k": 0, "d": 0, "a": 9}]}, {"series": "lpl-2026-regional-finals-round-2-1", "series_time": "2026-09-19T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 2, "patch": "26.17", "blue": "JD Gaming", "red": "Invictus Gaming", "blue_win": false, "blue_gd15": -4965, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Vi"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Poppy"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Lucian"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Qiyana"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Renata Glasc"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Rumble"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Ezreal"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Karma"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Kalista"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Annie"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Viktor"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Galio"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Trundle"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "K'Sante"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Aurora"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Twisted Fate"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Rumble", "k": 1, "d": 2, "a": 6}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 2, "d": 5, "a": 5}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Twisted Fate", "k": 2, "d": 4, "a": 2}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Kalista", "k": 4, "d": 4, "a": 4}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Renata Glasc", "k": 1, "d": 5, "a": 7}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "K'Sante", "k": 1, "d": 2, "a": 13}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Qiyana", "k": 5, "d": 1, "a": 10}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Aurora", "k": 5, "d": 2, "a": 11}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Ezreal", "k": 9, "d": 4, "a": 5}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Karma", "k": 0, "d": 1, "a": 15}]}, {"series": "lpl-2026-regional-finals-round-2-1", "series_time": "2026-09-19T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 3, "patch": "26.17", "blue": "Invictus Gaming", "red": "JD Gaming", "blue_win": false, "blue_gd15": -423, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Lee Sin"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Lucian"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Trundle"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ryze"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Naafiri"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Jinx"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Thresh"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Jayce"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Olaf"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Caitlyn"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Yorick"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Ziggs"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Jhin"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Renekton"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Viktor"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Nautilus"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Jayce", "k": 2, "d": 8, "a": 4}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Naafiri", "k": 4, "d": 4, "a": 9}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Ryze", "k": 6, "d": 3, "a": 8}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Jhin", "k": 4, "d": 5, "a": 8}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Nautilus", "k": 0, "d": 7, "a": 11}, {"name": "Xiaoxu", "role": "Top", "side": "red", "champion": "Renekton", "k": 3, "d": 6, "a": 6}, {"name": "JunJia", "role": "Jungle", "side": "red", "champion": "Trundle", "k": 11, "d": 1, "a": 11}, {"name": "HongQ", "role": "Mid", "side": "red", "champion": "Viktor", "k": 6, "d": 2, "a": 8}, {"name": "GALA", "role": "Bot", "side": "red", "champion": "Jinx", "k": 6, "d": 3, "a": 9}, {"name": "Vampire", "role": "Support", "side": "red", "champion": "Thresh", "k": 0, "d": 4, "a": 19}]}, {"series": "lpl-2026-regional-finals-round-2-1", "series_time": "2026-09-19T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 4, "patch": "26.17", "blue": "JD Gaming", "red": "Invictus Gaming", "blue_win": false, "blue_gd15": 3731, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Poppy"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Xayah"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Lucian"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Vi"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Pantheon"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Akali"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Alistar"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Ahri"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Jax"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Kennen"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Bard"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Gragas"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Kai'Sa"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Rakan"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Sivir"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Dr. Mundo"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Aphelios"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Jax", "k": 3, "d": 6, "a": 5}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Pantheon", "k": 6, "d": 4, "a": 7}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Akali", "k": 3, "d": 6, "a": 8}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Aphelios", "k": 6, "d": 4, "a": 3}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Rakan", "k": 1, "d": 5, "a": 11}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "Dr. Mundo", "k": 5, "d": 5, "a": 8}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Vi", "k": 6, "d": 3, "a": 12}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Ahri", "k": 6, "d": 2, "a": 12}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Sivir", "k": 7, "d": 6, "a": 12}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Alistar", "k": 1, "d": 4, "a": 17}]}, {"series": "worlds-2026-play-in-round-1-1", "series_time": "2026-10-15T18:00:00+00:00", "event": "worlds-2026-play-in", "n": 1, "patch": "26.20", "blue": "Karmine Corp", "red": "Cloud9", "blue_win": false, "blue_gd15": -1525, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Seraphine"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Nocturne"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "K'Sante"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Skarner"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Karma"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Rumble"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Lee Sin"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Ezreal"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Gnar"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Nautilus"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Orianna"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Jhin"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Sylas"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Locke"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Xin Zhao"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Miss Fortune"}], "players": [{"name": "Canna", "role": "Top", "side": "blue", "champion": "Rumble", "k": 0, "d": 4, "a": 0}, {"name": "Yike", "role": "Jungle", "side": "blue", "champion": "Lee Sin", "k": 0, "d": 1, "a": 1}, {"name": "Kyeahoo", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 1, "d": 3, "a": 0}, {"name": "Caliste", "role": "Bot", "side": "blue", "champion": "Miss Fortune", "k": 0, "d": 6, "a": 1}, {"name": "Busio", "role": "Support", "side": "blue", "champion": "Nautilus", "k": 0, "d": 6, "a": 1}, {"name": "Thanatos", "role": "Top", "side": "red", "champion": "Gnar", "k": 1, "d": 0, "a": 5}, {"name": "Blaber", "role": "Jungle", "side": "red", "champion": "Xin Zhao", "k": 4, "d": 0, "a": 10}, {"name": "Loki", "role": "Mid", "side": "red", "champion": "Locke", "k": 11, "d": 0, "a": 3}, {"name": "Tactical", "role": "Bot", "side": "red", "champion": "Ezreal", "k": 3, "d": 0, "a": 9}, {"name": "Vulcan", "role": "Support", "side": "red", "champion": "Karma", "k": 1, "d": 1, "a": 16}]}, {"series": "worlds-2026-play-in-round-1-1", "series_time": "2026-10-15T18:00:00+00:00", "event": "worlds-2026-play-in", "n": 2, "patch": "26.20", "blue": "Cloud9", "red": "Karmine Corp", "blue_win": false, "blue_gd15": 395, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Nocturne"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Seraphine"}, {"turn": 3, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Caitlyn"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Lulu"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Qiyana"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Vi"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Kalista"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Renata Glasc"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Cassiopeia"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Akali"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Lucian"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rakan"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Wukong"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Vel'Koz"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Varus"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Camille"}], "players": [{"name": "Thanatos", "role": "Top", "side": "blue", "champion": "Camille", "k": 4, "d": 5, "a": 6}, {"name": "Blaber", "role": "Jungle", "side": "blue", "champion": "Wukong", "k": 1, "d": 4, "a": 9}, {"name": "Loki", "role": "Mid", "side": "blue", "champion": "Akali", "k": 5, "d": 2, "a": 1}, {"name": "Tactical", "role": "Bot", "side": "blue", "champion": "Kalista", "k": 6, "d": 1, "a": 5}, {"name": "Vulcan", "role": "Support", "side": "blue", "champion": "Renata Glasc", "k": 0, "d": 2, "a": 13}, {"name": "Canna", "role": "Top", "side": "red", "champion": "Jayce", "k": 5, "d": 4, "a": 4}, {"name": "Yike", "role": "Jungle", "side": "red", "champion": "Vi", "k": 1, "d": 4, "a": 11}, {"name": "Kyeahoo", "role": "Mid", "side": "red", "champion": "Cassiopeia", "k": 2, "d": 4, "a": 5}, {"name": "Caliste", "role": "Bot", "side": "red", "champion": "Varus", "k": 4, "d": 2, "a": 6}, {"name": "Busio", "role": "Support", "side": "red", "champion": "Vel'Koz", "k": 2, "d": 2, "a": 6}]}, {"series": "worlds-2026-play-in-round-1-1", "series_time": "2026-10-15T18:00:00+00:00", "event": "worlds-2026-play-in", "n": 3, "patch": "26.20", "blue": "Karmine Corp", "red": "Cloud9", "blue_win": false, "blue_gd15": -236, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Seraphine"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Orianna"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Caitlyn"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Lulu"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Viktor"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Qiyana"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Jarvan IV"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lucian"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Nami"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Jhin"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Alistar"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Naafiri"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "K'Sante"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Vayne"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Aurora"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Sylas"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Anivia"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Annie"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Kled"}], "players": [{"name": "Canna", "role": "Top", "side": "blue", "champion": "Kled", "k": 0, "d": 4, "a": 1}, {"name": "Yike", "role": "Jungle", "side": "blue", "champion": "Naafiri", "k": 1, "d": 5, "a": 2}, {"name": "Kyeahoo", "role": "Mid", "side": "blue", "champion": "Anivia", "k": 2, "d": 8, "a": 1}, {"name": "Caliste", "role": "Bot", "side": "blue", "champion": "Lucian", "k": 2, "d": 2, "a": 3}, {"name": "Busio", "role": "Support", "side": "blue", "champion": "Nami", "k": 0, "d": 3, "a": 5}, {"name": "Thanatos", "role": "Top", "side": "red", "champion": "Olaf", "k": 5, "d": 1, "a": 3}, {"name": "Blaber", "role": "Jungle", "side": "red", "champion": "Jarvan IV", "k": 7, "d": 0, "a": 14}, {"name": "Loki", "role": "Mid", "side": "red", "champion": "Annie", "k": 1, "d": 2, "a": 14}, {"name": "Tactical", "role": "Bot", "side": "red", "champion": "Jhin", "k": 7, "d": 1, "a": 7}, {"name": "Vulcan", "role": "Support", "side": "red", "champion": "Alistar", "k": 2, "d": 1, "a": 12}]}, {"series": "worlds-2026-play-in-round-1-1", "series_time": "2026-10-15T18:00:00+00:00", "event": "worlds-2026-play-in", "n": 4, "patch": "26.20", "blue": "Cloud9", "red": "Karmine Corp", "blue_win": false, "blue_gd15": -4476, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Nocturne"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Seraphine"}, {"turn": 3, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Caitlyn"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Pantheon"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Viktor"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Qiyana"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Renekton"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Sylas"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Aphelios"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Vayne"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Draven"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Skarner"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Zaahen"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Xayah"}, {"turn": 19, "side": "red", "acti
```

### 3. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
print('COVERAGE:')
print(json.dumps(d['coverage'], indent=2))
print()
print('current keys:', list(d['current'].keys()))
print('history len:', len(d['history']))
"
```

### 4. 命令结果

```
COVERAGE:
{
  "history_games": 79,
  "starters": [
    {
      "side": "blue",
      "name": "Ackerman",
      "games": 8,
      "same_patch_games": 8
    },
    {
      "side": "blue",
      "name": "Curse",
      "games": 8,
      "same_patch_games": 8
    },
    {
      "side": "blue",
      "name": "Duduhh",
      "games": 8,
      "same_patch_games": 8
    },
    {
      "side": "blue",
      "name": "Feisty",
      "games": 8,
      "same_patch_games": 8
    },
    {
      "side": "blue",
      "name": "Zest",
      "games": 8,
      "same_patch_games": 8
    },
    {
      "side": "red",
      "name": "Berserker",
      "games": 9,
      "same_patch_games": 9
    },
    {
      "side": "red",
      "name": "Dhokla",
      "games": 9,
      "same_patch_games": 9
    },
    {
      "side": "red",
      "name": "Inspired",
      "games": 9,
      "same_patch_games": 9
    },
    {
      "side": "red",
      "name": "Isles",
      "games": 9,
      "same_patch_games": 9
    },
    {
      "side": "red",
      "name": "Saint",
      "games": 9,
      "same_patch_games": 9
    }
  ],
  "starters_with_history": 10,
  "coverage_group": "all",
  "previous_series_games": [
    1
  ],
  "missing_previous_series_games": []
}

current keys: ['event', 'stage', 'series', 'n', 'patch', 'bo', 'blue', 'red', 'starters', 'draft_rule', 'bp']
history len: 79
```

### 5. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
hist=d['history']
# Find games with teams LØS or LYON
for i,g in enumerate(hist):
    if g['blue'] in ('LØS','LYON') or g['red'] in ('LØS','LYON'):
        print(i, g['series'], 'n', g['n'], g['patch'], g['blue'], 'vs', g['red'], 'blue_win', g['blue_win'], 'gd15', g.get('blue_gd15'))
"
```

### 6. 命令结果

```
40 worlds-2026-main-event-round-1-7 n 1 26.20 LØS vs T1 blue_win False gd15 -2368
41 worlds-2026-main-event-round-1-8 n 1 26.20 LYON vs Team Secret Whales blue_win True gd15 -51
44 worlds-2026-main-event-round-2-3 n 1 26.20 LØS vs G2 Esports blue_win False gd15 -753
45 worlds-2026-main-event-round-2-4 n 1 26.20 Karmine Corp vs LYON blue_win False gd15 2170
54 worlds-2026-main-event-round-3-4 n 1 26.20 LYON vs Gen.G blue_win True gd15 -1063
55 worlds-2026-main-event-round-3-4 n 2 26.20 Gen.G vs LYON blue_win True gd15 1623
56 worlds-2026-main-event-round-3-4 n 3 26.20 Gen.G vs LYON blue_win True gd15 -2221
59 worlds-2026-main-event-round-3-7 n 1 26.20 Team Secret Whales vs LØS blue_win False gd15 1421
60 worlds-2026-main-event-round-3-7 n 2 26.20 Team Secret Whales vs LØS blue_win False gd15 -1500
65 worlds-2026-main-event-round-4-2 n 1 26.20 LYON vs Invictus Gaming blue_win False gd15 -1628
66 worlds-2026-main-event-round-4-2 n 2 26.20 Invictus Gaming vs LYON blue_win False gd15 338
67 worlds-2026-main-event-round-4-2 n 3 26.20 LYON vs Invictus Gaming blue_win False gd15 -4021
73 worlds-2026-main-event-round-4-5 n 1 26.20 LØS vs Team Liquid blue_win True gd15 1483
74 worlds-2026-main-event-round-4-5 n 2 26.20 LØS vs Team Liquid blue_win False gd15 -1870
75 worlds-2026-main-event-round-4-5 n 3 26.20 Team Liquid vs LØS blue_win False gd15 -4667
78 worlds-2026-main-event-round-5-2 n 1 26.20 LYON vs LØS blue_win False gd15 -1315
```

### 7. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
g=d['history'][78]
print('series:',g['series'],'n',g['n'])
print('blue',g['blue'],'red',g['red'],'blue_win',g['blue_win'],'gd15',g['blue_gd15'])
print('BP:')
for a in g['bp']:
    print(' ',a['turn'],a['side'],a['action'],a['champion'])
print('Players:')
for p in g['players']:
    print(' ',p['side'],p['role'],p['name'],p['champion'],p['k'],'/',p['d'],'/',p['a'])
"
```

### 8. 命令结果

```
series: worlds-2026-main-event-round-5-2 n 1
blue LYON red LØS blue_win False gd15 -1315
BP:
  1 blue ban Renata Glasc
  2 red ban Qiyana
  3 blue ban Jarvan IV
  4 red ban Nocturne
  5 blue ban Trundle
  6 red ban Olaf
  7 blue pick Syndra
  8 red pick Cassiopeia
  9 red pick Vi
  10 blue pick Ezreal
  11 blue pick Pantheon
  12 red pick Kai'Sa
  13 red ban Karma
  14 blue ban Ambessa
  15 red ban Jayce
  16 blue ban K'Sante
  17 red pick Nautilus
  18 blue pick Alistar
  19 blue pick Rumble
  20 red pick Aurora
Players:
  blue Top Dhokla Rumble 3 / 1 / 2
  blue Jungle Inspired Pantheon 2 / 1 / 4
  blue Mid Saint Syndra 1 / 3 / 1
  blue Bot Berserker Ezreal 2 / 3 / 1
  blue Support Isles Alistar 0 / 3 / 4
  red Top Zest Aurora 1 / 1 / 2
  red Jungle Curse Vi 3 / 2 / 4
  red Mid Feisty Cassiopeia 2 / 3 / 5
  red Bot Duduhh Kai'Sa 4 / 1 / 2
  red Support Ackerman Nautilus 1 / 1 / 4
```

### 9. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
hist=d['history']
targets=('LØS','LYON')
for i,g in enumerate(hist):
    if g['blue'] in targets or g['red'] in targets:
        # compute side for each team and whether they won
        teams={}
        for t in ('LØS','LYON'):
            side = 'blue' if g['blue']==t else 'red'
            win = g['blue_win'] if side=='blue' else (not g['blue_win'])
            gd15 = g.get('blue_gd15')
            teams[t]=(side, win, gd15)
        print(i, g['series'].split('-')[-1], 'n',g['n'])
        for t in ('LØS','LYON'):
            if t in (g['blue'],g['red']):
                side,win,gd15=teams[t]
                print('   ',t,side,'WIN' if win else 'LOSS','gd15(blue-minus-red)=',gd15)
"
```

### 10. 命令结果

```
40 7 n 1
    LØS blue LOSS gd15(blue-minus-red)= -2368
41 8 n 1
    LYON blue WIN gd15(blue-minus-red)= -51
44 3 n 1
    LØS blue LOSS gd15(blue-minus-red)= -753
45 4 n 1
    LYON red WIN gd15(blue-minus-red)= 2170
54 4 n 1
    LYON blue WIN gd15(blue-minus-red)= -1063
55 4 n 2
    LYON red LOSS gd15(blue-minus-red)= 1623
56 4 n 3
    LYON red LOSS gd15(blue-minus-red)= -2221
59 7 n 1
    LØS red WIN gd15(blue-minus-red)= 1421
60 7 n 2
    LØS red WIN gd15(blue-minus-red)= -1500
65 2 n 1
    LYON blue LOSS gd15(blue-minus-red)= -1628
66 2 n 2
    LYON red WIN gd15(blue-minus-red)= 338
67 2 n 3
    LYON blue LOSS gd15(blue-minus-red)= -4021
73 5 n 1
    LØS blue WIN gd15(blue-minus-red)= 1483
74 5 n 2
    LØS blue LOSS gd15(blue-minus-red)= -1870
75 5 n 3
    LØS red WIN gd15(blue-minus-red)= -4667
78 2 n 1
    LØS red WIN gd15(blue-minus-red)= -1315
    LYON blue LOSS gd15(blue-minus-red)= -1315
```

### 11. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
hist=d['history']
targets=('LØS','LYON')
for i,g in enumerate(hist):
    if g['blue'] in targets or g['red'] in targets:
        print('===',i,g['series'].split('-')[-1],'n',g['n'],g['blue'],'vs',g['red'],'blue_win',g['blue_win'],'gd15',g['blue_gd15'])
        for p in g['players']:
            print('   ',p['side'],p['role'],p['name'],p['champion'],str(p['k'])+'/'+str(p['d'])+'/'+str(p['a']))
"
```

### 12. 命令结果

```
=== 40 7 n 1 LØS vs T1 blue_win False gd15 -2368
    blue Top Zest K'Sante 1/5/1
    blue Jungle Curse Pantheon 0/5/2
    blue Mid Feisty Syndra 2/3/1
    blue Bot Duduhh Tristana 0/3/2
    blue Support Ackerman Rakan 0/3/3
    red Top Doran Jayce 4/0/9
    red Jungle Oner Lee Sin 8/0/6
    red Mid Faker LeBlanc 6/0/7
    red Bot Peyz Jhin 1/1/9
    red Support Keria Alistar 0/2/15
=== 41 8 n 1 LYON vs Team Secret Whales blue_win True gd15 -51
    blue Top Dhokla K'Sante 2/1/8
    blue Jungle Inspired Nocturne 2/2/11
    blue Mid Saint Anivia 2/0/11
    blue Bot Berserker Ezreal 13/1/5
    blue Support Isles Alistar 3/2/18
    red Top Pun Rumble 0/5/2
    red Jungle Hizto Lee Sin 0/4/3
    red Mid Dire Ryze 4/2/1
    red Bot Eddie Kai'Sa 2/4/3
    red Support Bie Nautilus 0/7/3
=== 44 3 n 1 LØS vs G2 Esports blue_win False gd15 -753
    blue Top Zest Jayce 3/3/2
    blue Jungle Curse Nocturne 1/5/5
    blue Mid Feisty Orianna 2/4/2
    blue Bot Duduhh Kalista 3/5/3
    blue Support Ackerman Renata Glasc 0/5/7
    red Top BrokenBlade K'Sante 3/1/6
    red Jungle SkewMond Lee Sin 10/1/8
    red Mid Caps Locke 8/5/5
    red Bot Hans Sama Ezreal 1/1/9
    red Support Labrov Karma 0/1/16
=== 45 4 n 1 Karmine Corp vs LYON blue_win False gd15 2170
    blue Top Canna Rumble 4/2/8
    blue Jungle Yike Lee Sin 3/4/4
    blue Mid Kyeahoo Cassiopeia 1/3/9
    blue Bot Caliste Kalista 6/4/8
    blue Support Busio Renata Glasc 1/2/14
    red Top Dhokla Galio 2/1/12
    red Jungle Inspired Wukong 2/3/11
    red Mid Saint Syndra 6/2/6
    red Bot Berserker Yunara 5/4/8
    red Support Isles Lulu 0/5/13
=== 54 4 n 1 LYON vs Gen.G blue_win True gd15 -1063
    blue Top Dhokla Olaf 2/3/2
    blue Jungle Inspired Xin Zhao 1/0/8
    blue Mid Saint Ahri 3/0/6
    blue Bot Berserker Kalista 4/0/4
    blue Support Isles Renata Glasc 0/1/9
    red Top Kiin Rumble 2/1/1
    red Jungle Canyon Qiyana 0/1/3
    red Mid Chovy Anivia 0/3/1
    red Bot Ruler Jhin 1/2/2
    red Support Duro Alistar 1/3/2
=== 55 4 n 2 Gen.G vs LYON blue_win True gd15 1623
    blue Top Kiin Ambessa 5/2/6
    blue Jungle Canyon Nocturne 1/1/12
    blue Mid Chovy Lissandra 2/3/10
    blue Bot Ruler Ashe 7/2/7
    blue Support Duro Seraphine 1/1/12
    red Top Dhokla Shen 1/3/5
    red Jungle Inspired Vi 1/5/6
    red Mid Saint Akali 5/3/3
    red Bot Berserker Yunara 2/3/3
    red Support Isles Lulu 0/2/7
=== 56 4 n 3 Gen.G vs LYON blue_win True gd15 -2221
    blue Top Kiin Camille 3/1/9
    blue Jungle Canyon Jayce 3/1/11
    blue Mid Chovy Galio 4/2/4
    blue Bot Ruler Ezreal 5/2/7
    blue Support Duro Nautilus 0/1/9
    red Top Dhokla K'Sante 1/3/3
    red Jungle Inspired Maokai 0/3/5
    red Mid Saint Tristana 4/2/0
    red Bot Berserker Lucian 1/4/2
    red Support Isles Milio 1/3/6
=== 59 7 n 1 Team Secret Whales vs LØS blue_win False gd15 1421
    blue Top Pun Shen 1/3/5
    blue Jungle Hizto Lee Sin 0/3/3
    blue Mid Dire Akali 5/4/1
    blue Bot Eddie Caitlyn 1/3/4
    blue Support Bie Elise 2/1/3
    red Top Zest Gnar 3/1/6
    red Jungle Curse Wukong 1/2/9
    red Mid Feisty Orianna 4/2/6
    red Bot Duduhh Kalista 6/2/5
    red Support Ackerman Renata Glasc 0/2/12
=== 60 7 n 2 Team Secret Whales vs LØS blue_win False gd15 -1500
    blue Top Pun Jax 0/5/6
    blue Jungle Hizto Vi 2/4/6
    blue Mid Dire Locke 5/3/2
    blue Bot Eddie Miss Fortune 6/4/5
    blue Support Bie Nautilus 0/6/9
    red Top Zest Kennen 9/2/5
    red Jungle Curse Trundle 5/2/14
    red Mid Feisty Galio 2/3/15
    red Bot Duduhh Ashe 5/3/9
    red Support Ackerman Seraphine 1/3/17
=== 65 2 n 1 LYON vs Invictus Gaming blue_win False gd15 -1628
    blue Top Dhokla Rumble 2/3/1
    blue Jungle Inspired Nocturne 1/6/1
    blue Mid Saint Sylas 1/2/2
    blue Bot Berserker Ezreal 0/3/3
    blue Support Isles Karma 0/5/3
    red Top TheShy Ornn 2/0/5
    red Jungle Wei Vi 3/2/11
    red Mid Rookie Aurora 8/1/8
    red Bot JiaQi Yunara 6/1/6
    red Support Meiko Lulu 0/0/16
=== 66 2 n 2 Invictus Gaming vs LYON blue_win False gd15 338
    blue Top TheShy Zaahen 0/4/3
    blue Jungle Wei Lee Sin 3/3/4
    blue Mid Rookie Annie 2/4/4
    blue Bot JiaQi Jhin 3/3/3
    blue Support Meiko Nautilus 0/4/4
    red Top Dhokla Olaf 4/2/3
    red Jungle Inspired Qiyana 4/1/5
    red Mid Saint Taliyah 4/1/7
    red Bot Berserker Corki 6/0/2
    red Support Isles Alistar 0/4/12
=== 67 2 n 3 LYON vs Invictus Gaming blue_win False gd15 -4021
    blue Top Dhokla K'Sante 1/2/0
    blue Jungle Inspired Xin Zhao 2/2/3
    blue Mid Saint LeBlanc 0/1/1
    blue Bot Berserker Lucian 1/2/1
    blue Support Isles Milio 1/0/2
    red Top TheShy Jayce 2/0/2
    red Jungle Wei Trundle 0/0/3
    red Mid Rookie Orianna 0/2/4
    red Bot JiaQi Caitlyn 5/1/2
    red Support Meiko Lux 0/2/7
=== 73 5 n 1 LØS vs Team Liquid blue_win True gd15 1483
    blue Top Zest Jayce 2/2/6
    blue Jungle Curse Trundle 7/0/6
    blue Mid Feisty Syndra 2/2/6
    blue Bot Duduhh Ashe 4/2/3
    blue Support Ackerman Seraphine 0/1/11
    red Top Morgan Ambessa 1/3/2
    red Jungle Josedeodo Nocturne 3/3/2
    red Mid Quid Sylas 2/4/3
    red Bot Yeon Ziggs 1/3/3
    red Support CoreJJ Nautilus 0/2/5
=== 74 5 n 2 LØS vs Team Liquid blue_win False gd15 -1870
    blue Top Zest Rumble 0/1/5
    blue Jungle Curse Jarvan IV 0/5/5
    blue Mid Feisty Galio 1/3/5
    blue Bot Duduhh Ezreal 5/3/2
    blue Support Ackerman Karma 2/3/6
    red Top Morgan Ornn 1/2/8
    red Jungle Josedeodo Xin Zhao 5/1/10
    red Mid Quid Orianna 4/0/6
    red Bot Yeon Lucian 4/4/8
    red Support CoreJJ Nami 1/1/14
=== 75 5 n 3 Team Liquid vs LØS blue_win False gd15 -4667
    blue Top Morgan Gnar 0/4/1
    blue Jungle Josedeodo Sejuani 1/3/5
    blue Mid Quid Viktor 0/5/5
    blue Bot Yeon Yunara 4/3/0
    blue Support CoreJJ Lulu 0/2/4
    red Top Zest Tristana 10/1/3
    red Jungle Curse Pantheon 4/0/7
    red Mid Feisty Taliyah 0/1/12
    red Bot Duduhh Kalista 2/1/7
    red Support Ackerman Renata Glasc 1/2/11
=== 78 2 n 1 LYON vs LØS blue_win False gd15 -1315
    blue Top Dhokla Rumble 3/1/2
    blue Jungle Inspired Pantheon 2/1/4
    blue Mid Saint Syndra 1/3/1
    blue Bot Berserker Ezreal 2/3/1
    blue Support Isles Alistar 0/3/4
    red Top Zest Aurora 1/1/2
    red Jungle Curse Vi 3/2/4
    red Mid Feisty Cassiopeia 2/3/5
    red Bot Duduhh Kai'Sa 4/1/2
    red Support Ackerman Nautilus 1/1/4
```

### 13. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
hist=d['history']
n=len(hist)
bw=sum(1 for g in hist if g['blue_win'])
ba=sum(1 for g in hist if (g.get('blue_gd15') is not None and g['blue_gd15']>0))
withgd=sum(1 for g in hist if g.get('blue_gd15') is not None)
print('total games',n,'blue_win',bw,'blue_win_rate',round(bw/n,3))
print('blue ahead at 15:',ba,'/',withgd,'=',round(ba/withgd,3))
# also check gd15==0
eq=sum(1 for g in hist if g.get('blue_gd15')==0)
print('gd15==0 count',eq)
# correlate: blue ahead -> blue win
both=[g for g in hist if g.get('blue_gd15') is not None]
ahead_win=sum(1 for g in both if g['blue_gd15']>0 and g['blue_win'])
ahead_n=sum(1 for g in both if g['blue_gd15']>0)
print('given blue ahead at 15, blue win:',ahead_win,'/',ahead_n,round(ahead_win/ahead_n,3))
behind_win=sum(1 for g in both if g['blue_gd15']<0 and g['blue_win'])
behind_n=sum(1 for g in both if g['blue_gd15']<0)
print('given blue behind at 15, blue win:',behind_win,'/',behind_n,round(behind_win/behind_n,3))
"
```

### 14. 命令结果

```
total games 79 blue_win 42 blue_win_rate 0.532
blue ahead at 15: 37 / 79 = 0.468
gd15==0 count 0
given blue ahead at 15, blue win: 25 / 37 0.676
given blue behind at 15, blue win: 17 / 42 0.405
```

### 15. 终端命令

```
python3 -c "
import json
# quick sanity: LØS and LYON side records and gd15 from their own perspective
d=json.load(open('snapshot.json'))
hist=d['history']
def teamview(g,t):
    side='blue' if g['blue']==t else 'red'
    win=g['blue_win'] if side=='blue' else (not g['blue_win'])
    gd=g.get('blue_gd15')
    own_gd = gd if side=='blue' else -gd
    return side,win,own_gd
for t in ('LØS','LYON'):
    games=[g for g in hist if g['blue']==t or g['red']==t]
    bw=[g for g in games if g['blue']==t]
    rw=[g for g in games if g['red']==t]
    print(t,'total',len(games),'blue side',len(bw),'red side',len(rw))
    for g in games:
        side,win,og=teamview(g,t)
        print('  ',side,'WIN' if win else 'LOSS','own_gd15',og, 'opp', g['red'] if side=='blue' else g['blue'])
"
```

### 16. 命令结果

```
LØS total 8 blue side 4 red side 4
   blue LOSS own_gd15 -2368 opp T1
   blue LOSS own_gd15 -753 opp G2 Esports
   red WIN own_gd15 -1421 opp Team Secret Whales
   red WIN own_gd15 1500 opp Team Secret Whales
   blue WIN own_gd15 1483 opp Team Liquid
   blue LOSS own_gd15 -1870 opp Team Liquid
   red WIN own_gd15 4667 opp Team Liquid
   red WIN own_gd15 1315 opp LYON
LYON total 9 blue side 5 red side 4
   blue WIN own_gd15 -51 opp Team Secret Whales
   red WIN own_gd15 -2170 opp Karmine Corp
   blue WIN own_gd15 -1063 opp Gen.G
   red LOSS own_gd15 -1623 opp Gen.G
   red LOSS own_gd15 2221 opp Gen.G
   blue LOSS own_gd15 -1628 opp Invictus Gaming
   red WIN own_gd15 -338 opp Invictus Gaming
   blue LOSS own_gd15 -4021 opp Invictus Gaming
   blue LOSS own_gd15 -1315 opp LØS
```

### 17. 工具调用 · Write

```
{
  "file_path": "[ephemeral]/app/prediction.json",
  "content": "{\n  \"p_blue_win\": 0.58,\n  \"p_blue_ahead_15\": 0.65\n}\n"
}
```

### 18. 工具结果

```
File created successfully at: [ephemeral]/app/prediction.json (file state is current in your context — no need to Read it back)
```

### 19. 终端命令

```
python3 -c "
import json,math
d=json.load(open('snapshot.json'))
hist=d['history']
# simple Elo, K=32, start 1500, iterate a few times
teams=set()
for g in hist:
    teams.add(g['blue']); teams.add(g['red'])
elo={t:1500.0 for t in teams}
for _ in range(20):
    for g in hist:
        b,r=g['blue'],g['red']
        eb=1/(1+10**((elo[r]-elo[b])/400))
        w=1.0 if g['blue_win'] else 0.0
        delta=32*(w-eb)
        elo[b]+=delta; elo[r]-=delta
# normalize-ish
print('LØS',round(elo.get('LØS',0),1))
print('LYON',round(elo.get('LYON',0),1))
diff=elo.get('LØS',1500)-elo.get('LYON',1500)
# plus home/blue advantage ~ 30 Elo
adj=diff+30
p=1/(1+10**(-adj/400))
print('diff',round(diff,1),'adj(blue)',round(adj,1),'p_blue_win',round(p,3))
# sort
for t,e in sorted(elo.items(),key=lambda x:-x[1])[:15]:
    print(round(e,0),t)
"
```

### 20. 命令结果

```
LØS 1499.4
LYON 1579.6
diff -80.2 adj(blue) -50.2 p_blue_win 0.428
2023.0 Dplus Kia
1848.0 Gen.G
1843.0 T1
1757.0 Top Esports
1683.0 Hanwha Life Esports
1672.0 Invictus Gaming
1615.0 Bilibili Gaming
1585.0 Karmine Corp
1580.0 LYON
1571.0 Movistar KOI
1499.0 LØS
1483.0 JD Gaming
1409.0 G2 Esports
1377.0 MVK Esports
1317.0 Team Liquid
```

### 21. 终端命令

```
python3 -c "
import json, math, random
d=json.load(open('snapshot.json'))
hist=d['history']
teams=sorted(set([g['blue'] for g in hist]+[g['red'] for g in hist]))
# Bradley-Terry via logistic: P(blue wins)=sigmoid(r_blue - r_red + h)
# gradient ascent
idx={t:i for i,t in enumerate(teams)}
n=len(teams)
r=[0.0]*n
h=0.0
lr=0.1
for it in range(2000):
    gr=[0.0]*n; gh=0.0
    for g in hist:
        rb=r[idx[g['blue']]]; rr=r[idx[g['red']]]
        z=rb-rr+h
        p=1/(1+math.exp(-z))
        y=1.0 if g['blue_win'] else 0.0
        e=y-p
        gr[idx[g['blue']]]+=e; gr[idx[g['red']]]-=e; gh+=e
    for i in range(n): r[i]+=lr*gr[i]
    h+=lr*gh
# print top
rank=sorted([(r[i],teams[i]) for i in range(n)],reverse=True)
for e,t in rank:
    print(round(e,3),t)
rb=r[idx['LØS']]; rr=r[idx['LYON']]
print('h (blue adv)',round(h,3))
p=1/(1+math.exp(-(rb-rr+h)))
print('LØS vs LYON p_blue_win',round(p,3))
print('rating diff (LØS-LYON)',round(rb-rr,3))
"
```

### 22. 命令结果

```
13.778 Dplus Kia
9.366 T1
4.767 Movistar KOI
1.732 Gen.G
1.443 Top Esports
1.028 Bilibili Gaming
0.897 Hanwha Life Esports
0.743 Invictus Gaming
0.065 LYON
-0.247 JD Gaming
-0.929 Karmine Corp
-0.972 G2 Esports
-1.265 LØS
-1.358 Team WE
-2.247 MVK Esports
-2.42 CTBC Flying Oyster
-2.709 Team Liquid
-2.907 Cloud9
-3.155 FURIA
-7.048 Team Secret Whales
-8.561 Anyone's Legend
h (blue adv) -0.231
LØS vs LYON p_blue_win 0.174
rating diff (LØS-LYON) -1.33
```

### 23. 终端命令

```
python3 -c "
import json
d=json.load(open('snapshot.json'))
hist=d['history']
from collections import Counter,defaultdict
champs=set(['Qiyana','Caitlyn','Karma','Ambessa','LeBlanc','Yunara','Lulu','Orianna','Lee Sin','Gnar'])
wins=defaultdict(int); picks=defaultdict(int)
for g in hist:
    for p in g['players']:
        c=p['champion']
        if c in champs:
            picks[c]+=1
            w=(g['blue_win'] if p['side']=='blue' else (not g['blue_win']))
            if w: wins[c]+=1
for c in sorted(champs):
    print(c,picks[c],wins[c],round(wins[c]/picks[c],2) if picks[c] else '-')
"
```

### 24. 命令结果

```
Ambessa 21 11 0.52
Caitlyn 6 2 0.33
Gnar 10 6 0.6
Karma 13 7 0.54
LeBlanc 3 1 0.33
Lee Sin 22 11 0.5
Lulu 19 11 0.58
Orianna 18 11 0.61
Qiyana 19 10 0.53
Yunara 15 8 0.53
```

### 25. 终端命令

```
python3 -c "
import json
from collections import Counter,defaultdict
d=json.load(open('snapshot.json'))
hist=d['history']
rec=defaultdict(lambda:[0,0])
for g in hist:
    for t,side in ((g['blue'],'b'),(g['red'],'r')):
        w=g['blue_win'] if side=='b' else (not g['blue_win'])
        rec[t][0]+=1
        rec[t][1]+=w
for t in ['LØS','LYON','G2 Esports','Team Liquid','Team Secret Whales','Gen.G','Invictus Gaming','T1','Karmine Corp','Dplus Kia','Dplus KIA']:
    if t in rec:
        n,w=rec[t]
        print(t,n,'wins',w,'losses',n-w)
"
```

### 26. 命令结果

```
LØS 8 wins 5 losses 3
LYON 9 wins 4 losses 5
G2 Esports 5 wins 1 losses 4
Team Liquid 7 wins 3 losses 4
Team Secret Whales 4 wins 0 losses 4
Gen.G 5 wins 4 losses 1
Invictus Gaming 14 wins 8 losses 6
T1 5 wins 4 losses 1
Karmine Corp 16 wins 12 losses 4
Dplus Kia 4 wins 4 losses 0
```

### 27. 终端命令

```
python3 -c "
import json, math
d=json.load(open('snapshot.json'))
hist=d['history']
teams=sorted(set([g['blue'] for g in hist]+[g['red'] for g in hist]))
idx={t:i for i,t in enumerate(teams)}
n=len(teams)
# ridge logistic (Bradley-Terry with L2), gradient ascent with penalty
for lam in [0.5,1.0,2.0,5.0,10.0]:
    r=[0.0]*n; h=0.0; lr=0.2
    for it in range(3000):
        gr=[0.0]*n; gh=0.0
        for g in hist:
            z=r[idx[g['blue']]]-r[idx[g['red']]]+h
            p=1/(1+math.exp(-z))
            e=(1.0 if g['blue_win'] else 0.0)-p
            gr[idx[g['blue']]]+=e; gr[idx[g['red']]]-=e; gh+=e
        for i in range(n): gr[i]-=lam*r[i]
        gh-=lam*h*0.1
        for i in range(n): r[i]+=lr*gr[i]
        h+=lr*gh
    rb=r[idx['LØS']]; rr=r[idx['LYON']]
    p=1/(1+math.exp(-(rb-rr+h)))
    print('lambda',lam,'LØS',round(rb,3),'LYON',round(rr,3),'h',round(h,3),'p_blue_win',round(p,3))
"
```

### 28. 命令结果 · 失败

```
Exit code 1
Traceback (most recent call last):
  File "<string>", line 15, in <module>
OverflowError: math range error
lambda 0.5 LØS 0.519 LYON -0.015 h -2.852 p_blue_win 0.09
lambda 1.0 LØS 0.6 LYON -0.221 h -3.051 p_blue_win 0.097
lambda 2.0 LØS 0.42 LYON -0.229 h -2.962 p_blue_win 0.09
lambda 5.0 LØS 0.197 LYON -0.197 h -2.847 p_blue_win 0.079
```

### 29. 工具调用 · Write

```
{
  "file_path": "[ephemeral]/app/prediction.json",
  "content": "{\n  \"p_blue_win\": 0.5,\n  \"p_blue_ahead_15\": 0.64\n}\n"
}
```

### 30. 工具结果

```
The file [ephemeral]/app/prediction.json has been updated successfully. (file state is current in your context — no need to Read it back)
```

### 31. 终端命令

```
python3 -c "
import json
p=json.load(open('prediction.json'))
print(p)
assert set(p)=={'p_blue_win','p_blue_ahead_15'}
for k,v in p.items():
    assert isinstance(v,(int,float)) and 0<=v<=1, (k,v)
print('valid')
"
```

### 32. 命令结果

```
{'p_blue_win': 0.5, 'p_blue_ahead_15': 0.64}
valid
```

### 33. 模型消息

```
I've completed the forecast. Here's my reasoning and final submission:

## Summary

**The matchup:** LØS (blue) vs LYON (red), game 2 of a BO3, patch 26.20, Fearless. LØS won game 1 as red side (+1315 gold at 15).

**Key evidence:**

| Signal | Direction |
|---|---|
| Head-to-head: LØS won game 1 (red side) | LØS |
| Season resume: LYON beat KC (12-4), Gen.G (4-1), IG (8-6); LØS's wins came vs TSW (0-4) and TL (3-4) | LYON |
| Records: LØS 5-3 vs LYON 4-5 (but softer schedule) | ~even |
| Game 2 draft: LYON gets comfort Yunara/Lulu bot + Lulu peel into LØS's dive comp; LØS on 4 unfamiliar picks | LYON |
| Early game: LYON was behind at 15:00 in 8/9 games; LØS drafted a strong early lane (Caitlyn/Karma) | LØS ahead |

**Final estimates:**
- `p_blue_win = 0.50` — Genuinely close. LØS's game-1 win and momentum offset LYON's stronger resume and better game-2 draft.
- `p_blue_ahead_15 = 0.64` — LØS's early-game comp plus LYON's consistent early deficits (behind in 8/9 games, including −1315 vs LØS) make a blue-side gold lead likely, though LØS's unfamiliar picks add variance.

The file is written to `./prediction.json` and validated.
```
