# Movistar KOI vs Bilibili Gaming · G1 · BP 前

worlds-2026-main-event · Round 1 · 26.20 · BO1

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/worlds-2026-main-event-round-1-3-g1-lobby/trajectory.jsonl) · [stderr](../../jobs/worlds-2026-main-event-round-1-3-g1-lobby/stderr.txt) · [交卷文件](../../jobs/worlds-2026-main-event-round-1-3-g1-lobby/prediction.json)

## 输入与可查询证据

蓝方首发为 Alvaro, Elyoya, Jojopyun, Myrwn, Supa。

红方首发为 Bin, Knight, ON, Viper, Xun。

冻结时可查 34 个历史小局，0 名首发有历史出场记录。

本局可见 0 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.15,
    "p_blue_ahead_15": 0.25
  },
  "observed_outcome": {
    "p_blue_win": 1,
    "p_blue_ahead_15": 1
  },
  "brier": {
    "p_blue_win": 0.7224999999999999,
    "p_blue_ahead_15": 0.5625
  },
  "reward": 0.35750000000000004
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 25402,
  "cache_creation_input_tokens": 0,
  "cache_read_input_tokens": 164608,
  "output_tokens": 6353
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
1	{"phase": "lobby", "series_time_utc": "2026-10-23T19:00:00+00:00", "current": {"event": "worlds-2026-main-event", "stage": "Round 1", "series": "worlds-2026-main-event-round-1-3", "n": 1, "patch": "26.20", "bo": 1, "blue": "Movistar KOI", "red": "Bilibili Gaming", "starters": {"blue": ["Alvaro", "Elyoya", "Jojopyun", "Myrwn", "Supa"], "red": ["Bin", "Knight", "ON", "Viper", "Xun"]}, "draft_rule": "Fearless"}, "history": [{"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": true, "blue_gd15": -38, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Renekton"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yorick"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Yorick", "k": 2, "d": 1, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 1, "d": 5, "a": 5}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 3, "d": 1, "a": 7}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 5, "d": 5, "a": 4}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 10}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Jayce", "k": 1, "d": 1, "a": 5}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 1, "d": 6, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Orianna", "k": 7, "d": 0, "a": 1}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Lucian", "k": 2, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Milio", "k": 1, "d": 2, "a": 10}]}, {"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 2, "patch": "26.17", "blue": "Invictus Gaming", "red": "Top Esports", "blue_win": false, "blue_gd15": -1351, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Trundle"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ashe"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Ryze"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Lee Sin"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Camille"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Nautilus"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Galio"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Naafiri"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Maokai"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Ezreal"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Karma"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Yone"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Camille", "k": 1, "d": 6, "a": 2}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Maokai", "k": 1, "d": 2, "a": 6}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Yone", "k": 1, "d": 2, "a": 4}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Ashe", "k": 4, "d": 3, "a": 1}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Seraphine", "k": 1, "d": 1, "a": 6}, {"name": "ZUIAN", "role": "Top", "side": "red", "champion": "Olaf", "k": 7, "d": 2, "a": 3}, {"name": "Tian", "role": "Jungle", "side": "red", "champion": "Lee Sin", "k": 3, "d": 3, "a": 6}, {"name": "Creme", "role": "Mid", "side": "red", "champion": "Ryze", "k": 2, "d": 0, "a": 6}, {"name": "JackeyLove", "role": "Bot", "side": "red", "champion": "Ezreal", "k": 1, "d": 2, "a": 7}, {"name": "Zhuo", "role": "Support", "side": "red", "champion": "Karma", "k": 1, "d": 1, "a": 8}]}, {"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 3, "patch": "26.17", "blue": "Top Esports", "red": "Invictus Gaming", "blue_win": true, "blue_gd15": 2775, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Ahri"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Vi"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Galio"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Viktor"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Qiyana"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Locke"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Jarvan IV"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Rumble"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Ambessa"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Nautilus"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Poppy"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Alistar"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Jhin"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Rell"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Corki"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Leona"}], "players": [{"name": "ZUIAN", "role": "Top", "side": "blue", "champion": "Ambessa", "k": 8, "d": 5, "a": 8}, {"name": "Tian", "role": "Jungle", "side": "blue", "champion": "Qiyana", "k": 4, "d": 3, "a": 12}, {"name": "Creme", "role": "Mid", "side": "blue", "champion": "Locke", "k": 13, "d": 2, "a": 8}, {"name": "JackeyLove", "role": "Bot", "side": "blue", "champion": "Jhin", "k": 4, "d": 1, "a": 18}, {"name": "Zhuo", "role": "Support", "side": "blue", "champion": "Leona", "k": 0, "d": 2, "a": 17}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "Rumble", "k": 2, "d": 6, "a": 6}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Jarvan IV", "k": 3, "d": 4, "a": 8}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Viktor", "k": 5, "d": 4, "a": 6}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Corki", "k": 2, "d": 7, "a": 4}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Rell", "k": 1, "d": 8, "a": 10}]}, {"series": "lpl-2026-regional-finals-round-1-1", "series_time": "2026-09-17T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 4, "patch": "26.17", "blue": "Top Esports", "red": "Invictus Gaming", "blue_win": true, "blue_gd15": 898, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Naafiri"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Poppy"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Neeko"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Vi"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Kalista"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Renata Glasc"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Aphelios"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Thresh"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Pantheon"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Taliyah"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Vayne"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Aurora"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Ahri"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Annie"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Gnar"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Galio"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Renekton"}], "players": [{"name": "ZUIAN", "role": "Top", "side": "blue", "champion": "Renekton", "k": 3, "d": 5, "a": 10}, {"name": "Tian", "role": "Jungle", "side": "blue", "champion": "Pantheon", "k": 8, "d": 1, "a": 11}, {"name": "Creme", "role": "Mid", "side": "blue", "champion": "Annie", "k": 5, "d": 3, "a": 13}, {"name": "JackeyLove", "role": "Bot", "side": "blue", "champion": "Kalista", "k": 7, "d": 2, "a": 10}, {"name": "Zhuo", "role": "Support", "side": "blue", "champion": "Renata Glasc", "k": 0, "d": 2, "a": 13}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "Gnar", "k": 3, "d": 2, "a": 4}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Vi", "k": 1, "d": 7, "a": 6}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Galio", "k": 2, "d": 6, "a": 8}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Aphelios", "k": 7, "d": 4, "a": 2}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Thresh", "k": 0, "d": 4, "a": 8}]}, {"series": "lpl-2026-regional-finals-round-1-2", "series_time": "2026-09-18T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "Team WE", "red": "JD Gaming", "blue_win": true, "blue_gd15": -3500, "bp": [{"turn": 1, "side": "blue", "action": "ban", "champion": "Orianna"}, {"turn": 2, "side": "red", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "blue", "action": "ban", "champion": "Poppy"}, {"turn": 4, "side": "red", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "blue", "action": "ban", "champion": "Akali"}, {"turn": 6, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 7, "side": "blue", "action": "pick", "champion": "Vi"}, {"turn": 8, "side": "red", "action": "pick", "champion": "Rumble"}, {"turn": 9, "side": "red", "action": "pick", "champion": "Qiyana"}, {"turn": 10, "side": "blue", "action": "pick", "champion": "Ahri"}, {"turn": 11, "side": "blue", "action": "pick", "champion": "Ezreal"}, {"turn": 12, "side": "red", "action": "pick", "champion": "Aurora"}, {"turn": 13, "side": "red", "action": "ban", "champion": "Neeko"}, {"turn": 14, "side": "blue", "action": "ban", "champion": "Renata Glasc"}, {"turn": 15, "side": "red", "action": "ban", "champion": "Bard"}, {"turn": 16, "side": "blue", "action": "ban", "champion": "Alistar"}, {"turn": 17, "side": "red", "action": "pick", "champion": "Jhin"}, {"turn": 18, "side": "blue", "action": "pick", "champion": "Galio"}, {"turn": 19, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 20, "side": "red", "action": "pick", "champion": "Nautilus"}], "players": [{"name": "Cube", "role": "Top", "side": "blue", "champion": "Galio", "k": 0, "d": 2, "a": 10}, {"name": "Monki", "role": "Jungle", "side": "blue", "champion": "Vi", "k": 6, "d": 1, "a": 5}, {"name": "Karis", "role": "Mid", "side": "blue", "champion": "Ahri", "k": 4, "d": 0, "a": 9}, {"name": "About", "role": "Bot", "side": "blue", "champion": "Ezreal", "k": 5, "d": 1, "a": 8}, {"name": "Erha", "role": "Support", "side": "blue", "champion": "Seraphine", "k": 2, "d": 1, "a": 14}, {"name": "Xiaoxu", "role": "Top", "side": "red", "champion": "Rumble", "k": 2, "d": 5, "a": 1}, {"name": "JunJia", "role": "Jungle", "side": "red", "champion": "Qiyana", "k": 1, "d": 3, "a": 2}, {"name": "HongQ", "role": "Mid", "side": "red", "champion": "Aurora", "k": 0, "d": 5, "a": 3}, {"name": "GALA", "role": "Bot", "side": "red", "champion": "Jhin", "k": 2, "d": 0, "a": 2}, {"name": "Vampire", "role": "Support", "side": "red", "champion": "Nautilus", "k": 0, "d": 4, "a": 3}]}, {"series": "lpl-2026-regional-finals-round-1-2", "series_time": "2026-09-18T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 2, "patch": "26.17", "blue": "JD Gaming", "red": "Team WE", "blue_win": true, "blue_gd15": 3715, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Orianna"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Lee Sin"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Annie"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Lucian"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Milio"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Viktor"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Naafiri"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Gnar"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Wukong"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Gwen"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Trundle"}, {"turn": 18, "side": "red", "action": "pick", "champion": "K'Sante"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Cho'Gath"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Ambessa"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Ambessa", "k": 3, "d": 1, "a": 4}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Trundle", "k": 4, "d": 0, "a": 6}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Viktor", "k": 1, "d": 2, "a": 7}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 2, "d": 0, "a": 1}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Lulu", "k": 0, "d": 0, "a": 4}, {"name": "Cube", "role": "Top", "side": "red", "champion": "K'Sante", "k": 0, "d": 3, "a": 1}, {"name": "Monki", "role": "Jungle", "side": "red", "champion": "Cho'Gath", "k": 3, "d": 4, "a": 0}, {"name": "Karis", "role": "Mid", "side": "red", "champion": "Annie", "k": 0, "d": 1, "a": 3}, {"name": "About", "role": "Bot", "side": "red", "champion": "Lucian", "k": 0, "d": 1, "a": 1}, {"name": "Erha", "role": "Support", "side": "red", "champion": "Milio", "k": 0, "d": 1, "a": 2}]}, {"series": "lpl-2026-regional-finals-round-1-2", "series_time": "2026-09-18T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 3, "patch": "26.17", "blue": "Team WE", "red": "JD Gaming", "blue_win": false, "blue_gd15": -2080, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Neeko"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Orianna"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Wukong"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Kalista"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Nocturne"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ryze"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Jarvan IV"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Twisted Fate"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Sion"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Caitlyn"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Jinx"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Alistar"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Zeri"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Rakan"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Xayah"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Renata Glasc"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Sivir"}], "players": [{"name": "Cube", "role": "Top", "side": "blue", "champion": "Sion", "k": 2, "d": 4, "a": 3}, {"name": "Monki", "role": "Jungle", "side": "blue", "champion": "Jarvan IV", "k": 1, "d": 5, "a": 5}, {"name": "Karis", "role": "Mid", "side": "blue", "champion": "Ryze", "k": 1, "d": 4, "a": 5}, {"name": "About", "role": "Bot", "side": "blue", "champion": "Sivir", "k": 2, "d": 4, "a": 4}, {"name": "Erha", "role": "Support", "side": "blue", "champion": "Rakan", "k": 0, "d": 3, "a": 6}, {"name": "Xiaoxu", "role": "Top", "side": "red", "champion": "Olaf", "k": 7, "d": 1, "a": 5}, {"name": "JunJia", "role": "Jungle", "side": "red", "champion": "Nocturne", "k": 3, "d": 2, "a": 10}, {"name": "HongQ", "role": "Mid", "side": "red", "champion": "Twisted Fate", "k": 4, "d": 1, "a": 11}, {"name": "GALA", "role": "Bot", "side": "red", "champion": "Xayah", "k": 6, "d": 0, "a": 8}, {"name": "Vampire", "role": "Support", "side": "red", "champion": "Renata Glasc", "k": 0, "d": 2, "a": 16}]}, {"series": "lpl-2026-regional-finals-round-1-2", "series_time": "2026-09-18T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 4, "patch": "26.17", "blue": "JD Gaming", "red": "Team WE", "blue_win": true, "blue_gd15": -1804, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Caitlyn"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Orianna"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Neeko"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Syndra"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Akali"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Maokai"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Jinx"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Renekton"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Corki"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Gnar"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Varus"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Thresh"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Ziggs"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Locke"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Sylas"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Ashe"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Braum"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Alistar"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Gnar", "k": 1, "d": 1, "a": 11}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 3, "d": 3, "a": 16}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Sylas", "k": 2, "d": 3, "a": 14}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Jinx", "k": 15, "d": 0, "a": 5}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Alistar", "k": 0, "d": 3, "a": 21}, {"name": "Cube", "role": "Top", "side": "red", "champion": "Renekton", "k": 1, "d": 5, "a": 3}, {"name": "Monki", "role": "Jungle", "side": "red", "champion": "Maokai", "k": 0, "d": 6, "a": 5}, {"name": "Karis", "role": "Mid", "side": "red", "champion": "Corki", "k": 7, "d": 2, "a": 2}, {"name": "About", "role": "Bot", "side": "red", "champion": "Ashe", "k": 1, "d": 4, "a": 9}, {"name": "Erha", "role": "Support", "side": "red", "champion": "Braum", "k": 1, "d": 4, "a": 8}]}, {"series": "lpl-2026-regional-finals-round-2-1", "series_time": "2026-09-19T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 1, "patch": "26.17", "blue": "JD Gaming", "red": "Invictus Gaming", "blue_win": false, "blue_gd15": 232, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Vi"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Lee Sin"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Lulu"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Orianna"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Syndra"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Tristana"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Seraphine"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Trundle"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rumble"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Vayne"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Cho'Gath"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Maokai"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Gnar"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Ambessa"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Ambessa", "k": 1, "d": 1, "a": 0}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Cho'Gath", "k": 1, "d": 4, "a": 2}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Orianna", "k": 1, "d": 2, "a": 0}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 0, "d": 1, "a": 1}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Seraphine", "k": 0, "d": 3, "a": 1}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "Gnar", "k": 0, "d": 1, "a": 5}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Maokai", "k": 1, "d": 1, "a": 6}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Syndra", "k": 4, "d": 1, "a": 5}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Tristana", "k": 6, "d": 0, "a": 2}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Lulu", "k": 0, "d": 0, "a": 9}]}, {"series": "lpl-2026-regional-finals-round-2-1", "series_time": "2026-09-19T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 2, "patch": "26.17", "blue": "JD Gaming", "red": "Invictus Gaming", "blue_win": false, "blue_gd15": -4965, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Vi"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Poppy"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Lucian"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Qiyana"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Renata Glasc"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Rumble"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Ezreal"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Karma"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Kalista"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Annie"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Viktor"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Galio"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Trundle"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Skarner"}, {"turn": 18, "side": "red", "action": "pick", "champion": "K'Sante"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Aurora"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Twisted Fate"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Rumble", "k": 1, "d": 2, "a": 6}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Skarner", "k": 2, "d": 5, "a": 5}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Twisted Fate", "k": 2, "d": 4, "a": 2}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Kalista", "k": 4, "d": 4, "a": 4}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Renata Glasc", "k": 1, "d": 5, "a": 7}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "K'Sante", "k": 1, "d": 2, "a": 13}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Qiyana", "k": 5, "d": 1, "a": 10}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Aurora", "k": 5, "d": 2, "a": 11}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Ezreal", "k": 9, "d": 4, "a": 5}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Karma", "k": 0, "d": 1, "a": 15}]}, {"series": "lpl-2026-regional-finals-round-2-1", "series_time": "2026-09-19T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 3, "patch": "26.17", "blue": "Invictus Gaming", "red": "JD Gaming", "blue_win": false, "blue_gd15": -423, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Lee Sin"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Lucian"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Trundle"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Ryze"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Naafiri"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Jinx"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Thresh"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Jayce"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Olaf"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Caitlyn"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Yorick"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Ziggs"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Jhin"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Renekton"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Viktor"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Nautilus"}], "players": [{"name": "TheShy", "role": "Top", "side": "blue", "champion": "Jayce", "k": 2, "d": 8, "a": 4}, {"name": "Wei", "role": "Jungle", "side": "blue", "champion": "Naafiri", "k": 4, "d": 4, "a": 9}, {"name": "Rookie", "role": "Mid", "side": "blue", "champion": "Ryze", "k": 6, "d": 3, "a": 8}, {"name": "JiaQi", "role": "Bot", "side": "blue", "champion": "Jhin", "k": 4, "d": 5, "a": 8}, {"name": "Meiko", "role": "Support", "side": "blue", "champion": "Nautilus", "k": 0, "d": 7, "a": 11}, {"name": "Xiaoxu", "role": "Top", "side": "red", "champion": "Renekton", "k": 3, "d": 6, "a": 6}, {"name": "JunJia", "role": "Jungle", "side": "red", "champion": "Trundle", "k": 11, "d": 1, "a": 11}, {"name": "HongQ", "role": "Mid", "side": "red", "champion": "Viktor", "k": 6, "d": 2, "a": 8}, {"name": "GALA", "role": "Bot", "side": "red", "champion": "Jinx", "k": 6, "d": 3, "a": 9}, {"name": "Vampire", "role": "Support", "side": "red", "champion": "Thresh", "k": 0, "d": 4, "a": 19}]}, {"series": "lpl-2026-regional-finals-round-2-1", "series_time": "2026-09-19T09:00:00+00:00", "event": "lpl-2026-regional-finals", "n": 4, "patch": "26.17", "blue": "JD Gaming", "red": "Invictus Gaming", "blue_win": false, "blue_gd15": 3731, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Cassiopeia"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Poppy"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Xayah"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Lucian"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Vi"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Pantheon"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Akali"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Alistar"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Ahri"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Jax"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Kennen"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Bard"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Gragas"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Kai'Sa"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Rakan"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Sivir"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Dr. Mundo"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Aphelios"}], "players": [{"name": "Xiaoxu", "role": "Top", "side": "blue", "champion": "Jax", "k": 3, "d": 6, "a": 5}, {"name": "JunJia", "role": "Jungle", "side": "blue", "champion": "Pantheon", "k": 6, "d": 4, "a": 7}, {"name": "HongQ", "role": "Mid", "side": "blue", "champion": "Akali", "k": 3, "d": 6, "a": 8}, {"name": "GALA", "role": "Bot", "side": "blue", "champion": "Aphelios", "k": 6, "d": 4, "a": 3}, {"name": "Vampire", "role": "Support", "side": "blue", "champion": "Rakan", "k": 1, "d": 5, "a": 11}, {"name": "TheShy", "role": "Top", "side": "red", "champion": "Dr. Mundo", "k": 5, "d": 5, "a": 8}, {"name": "Wei", "role": "Jungle", "side": "red", "champion": "Vi", "k": 6, "d": 3, "a": 12}, {"name": "Rookie", "role": "Mid", "side": "red", "champion": "Ahri", "k": 6, "d": 2, "a": 12}, {"name": "JiaQi", "role": "Bot", "side": "red", "champion": "Sivir", "k": 7, "d": 6, "a": 12}, {"name": "Meiko", "role": "Support", "side": "red", "champion": "Alistar", "k": 1, "d": 4, "a": 17}]}, {"series": "worlds-2026-play-in-round-1-1", "series_time": "2026-10-15T18:00:00+00:00", "event": "worlds-2026-play-in", "n": 1, "patch": "26.20", "blue": "Karmine Corp", "red": "Cloud9", "blue_win": false, "blue_gd15": -1525, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Seraphine"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Nocturne"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "K'Sante"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Qiyana"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Skarner"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Karma"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Rumble"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Lee Sin"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Ezreal"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Gnar"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Nautilus"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Orianna"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Jhin"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Sylas"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Syndra"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Locke"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Xin Zhao"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Miss Fortune"}], "players": [{"name": "Canna", "role": "Top", "side": "blue", "champion": "Rumble", "k": 0, "d": 4, "a": 0}, {"name": "Yike", "role": "Jungle", "side": "blue", "champion": "Lee Sin", "k": 0, "d": 1, "a": 1}, {"name": "Kyeahoo", "role": "Mid", "side": "blue", "champion": "Syndra", "k": 1, "d": 3, "a": 0}, {"name": "Caliste", "role": "Bot", "side": "blue", "champion": "Miss Fortune", "k": 0, "d": 6, "a": 1}, {"name": "Busio", "role": "Support", "side": "blue", "champion": "Nautilus", "k": 0, "d": 6, "a": 1}, {"name": "Thanatos", "role": "Top", "side": "red", "champion": "Gnar", "k": 1, "d": 0, "a": 5}, {"name": "Blaber", "role": "Jungle", "side": "red", "champion": "Xin Zhao", "k": 4, "d": 0, "a": 10}, {"name": "Loki", "role": "Mid", "side": "red", "champion": "Locke", "k": 11, "d": 0, "a": 3}, {"name": "Tactical", "role": "Bot", "side": "red", "champion": "Ezreal", "k": 3, "d": 0, "a": 9}, {"name": "Vulcan", "role": "Support", "side": "red", "champion": "Karma", "k": 1, "d": 1, "a": 16}]}, {"series": "worlds-2026-play-in-round-1-1", "series_time": "2026-10-15T18:00:00+00:00", "event": "worlds-2026-play-in", "n": 2, "patch": "26.20", "blue": "Cloud9", "red": "Karmine Corp", "blue_win": false, "blue_gd15": 395, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Nocturne"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Seraphine"}, {"turn": 3, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Caitlyn"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Lulu"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Qiyana"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Vi"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Kalista"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Renata Glasc"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Cassiopeia"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Jayce"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Akali"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Lucian"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Olaf"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Rakan"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Jarvan IV"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Wukong"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Vel'Koz"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Varus"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Camille"}], "players": [{"name": "Thanatos", "role": "Top", "side": "blue", "champion": "Camille", "k": 4, "d": 5, "a": 6}, {"name": "Blaber", "role": "Jungle", "side": "blue", "champion": "Wukong", "k": 1, "d": 4, "a": 9}, {"name": "Loki", "role": "Mid", "side": "blue", "champion": "Akali", "k": 5, "d": 2, "a": 1}, {"name": "Tactical", "role": "Bot", "side": "blue", "champion": "Kalista", "k": 6, "d": 1, "a": 5}, {"name": "Vulcan", "role": "Support", "side": "blue", "champion": "Renata Glasc", "k": 0, "d": 2, "a": 13}, {"name": "Canna", "role": "Top", "side": "red", "champion": "Jayce", "k": 5, "d": 4, "a": 4}, {"name": "Yike", "role": "Jungle", "side": "red", "champion": "Vi", "k": 1, "d": 4, "a": 11}, {"name": "Kyeahoo", "role": "Mid", "side": "red", "champion": "Cassiopeia", "k": 2, "d": 4, "a": 5}, {"name": "Caliste", "role": "Bot", "side": "red", "champion": "Varus", "k": 4, "d": 2, "a": 6}, {"name": "Busio", "role": "Support", "side": "red", "champion": "Vel'Koz", "k": 2, "d": 2, "a": 6}]}, {"series": "worlds-2026-play-in-round-1-1", "series_time": "2026-10-15T18:00:00+00:00", "event": "worlds-2026-play-in", "n": 3, "patch": "26.20", "blue": "Karmine Corp", "red": "Cloud9", "blue_win": false, "blue_gd15": -236, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Seraphine"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Orianna"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Caitlyn"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Lulu"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Viktor"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Qiyana"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Jarvan IV"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Lucian"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Nami"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Jhin"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Alistar"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Naafiri"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "K'Sante"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Vayne"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Aurora"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Sylas"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Anivia"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Annie"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Kled"}], "players": [{"name": "Canna", "role": "Top", "side": "blue", "champion": "Kled", "k": 0, "d": 4, "a": 1}, {"name": "Yike", "role": "Jungle", "side": "blue", "champion": "Naafiri", "k": 1, "d": 5, "a": 2}, {"name": "Kyeahoo", "role": "Mid", "side": "blue", "champion": "Anivia", "k": 2, "d": 8, "a": 1}, {"name": "Caliste", "role": "Bot", "side": "blue", "champion": "Lucian", "k": 2, "d": 2, "a": 3}, {"name": "Busio", "role": "Support", "side": "blue", "champion": "Nami", "k": 0, "d": 3, "a": 5}, {"name": "Thanatos", "role": "Top", "side": "red", "champion": "Olaf", "k": 5, "d": 1, "a": 3}, {"name": "Blaber", "role": "Jungle", "side": "red", "champion": "Jarvan IV", "k": 7, "d": 0, "a": 14}, {"name": "Loki", "role": "Mid", "side": "red", "champion": "Annie", "k": 1, "d": 2, "a": 14}, {"name": "Tactical", "role": "Bot", "side": "red", "champion": "Jhin", "k": 7, "d": 1, "a": 7}, {"name": "Vulcan", "role": "Support", "side": "red", "champion": "Alistar", "k": 2, "d": 1, "a": 12}]}, {"series": "worlds-2026-play-in-round-1-1", "series_time": "2026-10-15T18:00:00+00:00", "event": "worlds-2026-play-in", "n": 4, "patch": "26.20", "blue": "Cloud9", "red": "Karmine Corp", "blue_win": false, "blue_gd15": -4476, "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Nocturne"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Seraphine"}, {"turn": 3, "side": "red", "action": "ban", "champion": "K'Sante"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Caitlyn"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Pantheon"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Viktor"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Qiyana"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Yunara"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Lulu"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Orianna"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Renekton"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Sylas"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Aphelios"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Vayne"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Draven"}, {"turn": 16, "side": "red", "action": "ban", "champion": "Skarner"}, {"turn": 17, "side": "blue", "action": "pick", "champion": "Zaahen"}, {"turn": 18, "side": "red", "action": "pick", "champion": "Xayah"}, {"turn": 19, "side": "red", "action": "pick", "champion": "Rakan"}, {"turn": 20, "side": "blue", "action": "pick", "champion": "Sejuani"}], "players": [{"name": "Thanatos", "role": "Top", "side": "blue", "champion": "Zaahen", "k": 2, "d": 1, "a": 1}, {"name": "Blaber", "role": "Jungle", "side": "blue", "champion": "Sejuani", "k": 0, "d": 2, "a": 6}, {"name": "Loki", "role": "Mid", "side": "blue", "champion": "Sylas", "k": 0, "d": 5, "a": 4}, {"name": "Tactical", "role": "Bot", "side": "blue", "champion": "Yunara", "k": 3, "d": 4, "a": 2}, {"name": "Vulcan", "role": "Support", "side": "blue", "champion": "Lulu", "k": 1, "d": 3, "a": 4}, {"name": "Canna", "role": "Top", "side": "red", "champion": "Renekton", "k": 1, "d": 0, "a": 8}, {"name": "Yike", "role": "Jungle", "side": "red", "champion": "Qiyana", "k": 1, "d": 2, "a": 6}, {"name": "Kyeahoo", "role": "Mid", "side": "red", "champion": "Orianna", "k": 2, "d": 2, "a": 5}, {"name": "Caliste", "role": "Bot", "side": "red", "champion": "Xayah", "k": 11, "d": 1, "a": 3}, {"name": "Busio", "role": "Support", "side": "red", "champion": "Rakan", "k": 0, "d": 1, "a": 9}]}, {"series": "worlds-2026-play-in-round-1-1", "series_time": "2026-10-15T18:00:00+00:00", "event": "worlds-2026-play-in", "n": 5, "patch": "26.20", "blue": "Karmine Corp", "red": "Cloud9", "blue_win": true, "blue_gd15": 622, "bp": [{"turn": 1, "side": "blue", "action": "ban", "champion": "Nocturn
```

### 3. 终端命令

```
python3 -c "
import json
d = json.load(open('snapshot.json'))
print('CURRENT:', json.dumps(d['current'], indent=2))
print('COVERAGE:', json.dumps(d.get('coverage', {}), indent=2))
print('num history:', len(d['history']))
"
```

### 4. 命令结果

```
CURRENT: {
  "event": "worlds-2026-main-event",
  "stage": "Round 1",
  "series": "worlds-2026-main-event-round-1-3",
  "n": 1,
  "patch": "26.20",
  "bo": 1,
  "blue": "Movistar KOI",
  "red": "Bilibili Gaming",
  "starters": {
    "blue": [
      "Alvaro",
      "Elyoya",
      "Jojopyun",
      "Myrwn",
      "Supa"
    ],
    "red": [
      "Bin",
      "Knight",
      "ON",
      "Viper",
      "Xun"
    ]
  },
  "draft_rule": "Fearless"
}
COVERAGE: {
  "history_games": 34,
  "starters": [
    {
      "side": "blue",
      "name": "Alvaro",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "blue",
      "name": "Elyoya",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "blue",
      "name": "Jojopyun",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "blue",
      "name": "Myrwn",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "blue",
      "name": "Supa",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "red",
      "name": "Bin",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "red",
      "name": "Knight",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "red",
      "name": "ON",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "red",
      "name": "Viper",
      "games": 0,
      "same_patch_games": 0
    },
    {
      "side": "red",
      "name": "Xun",
      "games": 0,
      "same_patch_games": 0
    }
  ],
  "starters_with_history": 0,
  "coverage_group": "none",
  "previous_series_games": [],
  "missing_previous_series_games": []
}
num history: 34
```

### 5. 终端命令

```
python3 -c "
import json
d = json.load(open('snapshot.json'))
h = d['history']
blue_win = sum(1 for g in h if g.get('blue_win') is True)
blue_win_n = sum(1 for g in h if 'blue_win' in g)
gd = [g['blue_gd15'] for g in h if g.get('blue_gd15') is not None]
ahead = sum(1 for x in gd if x > 0)
print('total games', len(h))
print('blue_win recorded', blue_win_n, 'blue_win', blue_win, 'rate', blue_win/blue_win_n if blue_win_n else None)
print('blue_gd15 recorded', len(gd), 'ahead(>0)', ahead, 'rate', ahead/len(gd) if gd else None)
print('mean gd15', sum(gd)/len(gd) if gd else None)
# by patch
for p in sorted(set(g['patch'] for g in h)):
    hs = [g for g in h if g['patch']==p]
    bw = sum(1 for g in hs if g.get('blue_win') is True)
    bwn = sum(1 for g in hs if 'blue_win' in g)
    gd = [g['blue_gd15'] for g in hs if g.get('blue_gd15') is not None]
    ah = sum(1 for x in gd if x>0)
    print(p, 'n', len(hs), 'blue_win', bw, '/', bwn, '=', round(bw/bwn,3) if bwn else None, 'ahead', ah, '/', len(gd), '=', round(ah/len(gd),3) if gd else None, 'meangd', round(sum(gd)/len(gd)) if gd else None)
"
```

### 6. 命令结果

```
total games 34
blue_win recorded 34 blue_win 19 rate 0.5588235294117647
blue_gd15 recorded 34 ahead(>0) 16 rate 0.47058823529411764
mean gd15 268.29411764705884
26.17 n 12 blue_win 6 / 12 = 0.5 ahead 5 / 12 = 0.417 meangd -234
26.20 n 22 blue_win 13 / 22 = 0.591 ahead 11 / 22 = 0.5 meangd 542
```

### 7. 终端命令

```
python3 -c "
import json
d = json.load(open('snapshot.json'))
h = d['history']
for g in h:
    print(g['event'], g['series'], 'n', g['n'], g['patch'], g['blue'], 'vs', g['red'], 'blue_win', g.get('blue_win'), 'gd15', g.get('blue_gd15'))
"
```

### 8. 命令结果

```
lpl-2026-regional-finals lpl-2026-regional-finals-round-1-1 n 1 26.17 Invictus Gaming vs Top Esports blue_win True gd15 -38
lpl-2026-regional-finals lpl-2026-regional-finals-round-1-1 n 2 26.17 Invictus Gaming vs Top Esports blue_win False gd15 -1351
lpl-2026-regional-finals lpl-2026-regional-finals-round-1-1 n 3 26.17 Top Esports vs Invictus Gaming blue_win True gd15 2775
lpl-2026-regional-finals lpl-2026-regional-finals-round-1-1 n 4 26.17 Top Esports vs Invictus Gaming blue_win True gd15 898
lpl-2026-regional-finals lpl-2026-regional-finals-round-1-2 n 1 26.17 Team WE vs JD Gaming blue_win True gd15 -3500
lpl-2026-regional-finals lpl-2026-regional-finals-round-1-2 n 2 26.17 JD Gaming vs Team WE blue_win True gd15 3715
lpl-2026-regional-finals lpl-2026-regional-finals-round-1-2 n 3 26.17 Team WE vs JD Gaming blue_win False gd15 -2080
lpl-2026-regional-finals lpl-2026-regional-finals-round-1-2 n 4 26.17 JD Gaming vs Team WE blue_win True gd15 -1804
lpl-2026-regional-finals lpl-2026-regional-finals-round-2-1 n 1 26.17 JD Gaming vs Invictus Gaming blue_win False gd15 232
lpl-2026-regional-finals lpl-2026-regional-finals-round-2-1 n 2 26.17 JD Gaming vs Invictus Gaming blue_win False gd15 -4965
lpl-2026-regional-finals lpl-2026-regional-finals-round-2-1 n 3 26.17 Invictus Gaming vs JD Gaming blue_win False gd15 -423
lpl-2026-regional-finals lpl-2026-regional-finals-round-2-1 n 4 26.17 JD Gaming vs Invictus Gaming blue_win False gd15 3731
worlds-2026-play-in worlds-2026-play-in-round-1-1 n 1 26.20 Karmine Corp vs Cloud9 blue_win False gd15 -1525
worlds-2026-play-in worlds-2026-play-in-round-1-1 n 2 26.20 Cloud9 vs Karmine Corp blue_win False gd15 395
worlds-2026-play-in worlds-2026-play-in-round-1-1 n 3 26.20 Karmine Corp vs Cloud9 blue_win False gd15 -236
worlds-2026-play-in worlds-2026-play-in-round-1-1 n 4 26.20 Cloud9 vs Karmine Corp blue_win False gd15 -4476
worlds-2026-play-in worlds-2026-play-in-round-1-1 n 5 26.20 Karmine Corp vs Cloud9 blue_win True gd15 622
worlds-2026-play-in worlds-2026-play-in-round-1-2 n 1 26.20 MVK Esports vs FURIA blue_win True gd15 -947
worlds-2026-play-in worlds-2026-play-in-round-1-2 n 2 26.20 MVK Esports vs FURIA blue_win True gd15 2286
worlds-2026-play-in worlds-2026-play-in-round-1-2 n 3 26.20 MVK Esports vs FURIA blue_win True gd15 5303
worlds-2026-play-in worlds-2026-play-in-round-2-1 n 1 26.20 Karmine Corp vs MVK Esports blue_win True gd15 3377
worlds-2026-play-in worlds-2026-play-in-round-2-1 n 2 26.20 Karmine Corp vs MVK Esports blue_win True gd15 -3003
worlds-2026-play-in worlds-2026-play-in-round-2-1 n 3 26.20 MVK Esports vs Karmine Corp blue_win False gd15 -2837
worlds-2026-play-in worlds-2026-play-in-round-1-3 n 1 26.20 FURIA vs Cloud9 blue_win False gd15 -1173
worlds-2026-play-in worlds-2026-play-in-round-1-3 n 2 26.20 Cloud9 vs FURIA blue_win False gd15 1875
worlds-2026-play-in worlds-2026-play-in-round-1-3 n 3 26.20 FURIA vs Cloud9 blue_win True gd15 -432
worlds-2026-play-in worlds-2026-play-in-round-1-3 n 4 26.20 FURIA vs Cloud9 blue_win True gd15 -678
worlds-2026-play-in worlds-2026-play-in-round-2-2 n 1 26.20 MVK Esports vs FURIA blue_win True gd15 3139
worlds-2026-play-in worlds-2026-play-in-round-2-2 n 2 26.20 MVK Esports vs FURIA blue_win True gd15 1704
worlds-2026-play-in worlds-2026-play-in-round-2-2 n 3 26.20 MVK Esports vs FURIA blue_win False gd15 -2091
worlds-2026-play-in worlds-2026-play-in-round-2-2 n 4 26.20 MVK Esports vs FURIA blue_win True gd15 3077
worlds-2026-play-in worlds-2026-play-in-round-3-1 n 1 26.20 Karmine Corp vs MVK Esports blue_win True gd15 3288
worlds-2026-play-in worlds-2026-play-in-round-3-1 n 2 26.20 Karmine Corp vs MVK Esports blue_win True gd15 6558
worlds-2026-play-in worlds-2026-play-in-round-3-1 n 3 26.20 MVK Esports vs Karmine Corp blue_win False gd15 -2294
```

### 9. 工具调用 · Write

```
{
  "file_path": "[ephemeral]/app/prediction.json",
  "content": "{\"p_blue_win\": 0.15, \"p_blue_ahead_15\": 0.25}\n"
}
```

### 10. 工具结果

```
File created successfully at: [ephemeral]/app/prediction.json (file state is current in your context — no need to Read it back)
```

### 11. 终端命令

```
python3 -c "
import json
d = json.load(open('snapshot.json'))
h = [g for g in d['history'] if g['patch']=='26.20']
# blue_win vs blue ahead
both = [(g.get('blue_win'), g.get('blue_gd15')) for g in h if 'blue_win' in g and g.get('blue_gd15') is not None]
print('26.20 games with both:', len(both))
for bw,gd in both:
    print(bw, gd, 'ahead' if gd>0 else 'behind/even')
win_and_ahead = sum(1 for bw,gd in both if bw and gd>0)
win_and_behind = sum(1 for bw,gd in both if bw and gd<=0)
lose_and_ahead = sum(1 for bw,gd in both if not bw and gd>0)
lose_and_behind = sum(1 for bw,gd in both if not bw and gd<=0)
print('win&ahead',win_and_ahead,'win&behind',win_and_behind,'lose&ahead',lose_and_ahead,'lose&behind',lose_and_behind)
"
```

### 12. 命令结果

```
26.20 games with both: 22
False -1525 behind/even
False 395 ahead
False -236 behind/even
False -4476 behind/even
True 622 ahead
True -947 behind/even
True 2286 ahead
True 5303 ahead
True 3377 ahead
True -3003 behind/even
False -2837 behind/even
False -1173 behind/even
False 1875 ahead
True -432 behind/even
True -678 behind/even
True 3139 ahead
True 1704 ahead
False -2091 behind/even
True 3077 ahead
True 3288 ahead
True 6558 ahead
False -2294 behind/even
win&ahead 9 win&behind 4 lose&ahead 2 lose&behind 7
```

### 13. 模型消息

```
I've analyzed the snapshot and written the prediction. Here's my reasoning:

## Key findings

**Coverage: none.** Every one of the 10 starters (both KOI and BLG) has 0 recorded appearances in the 34-game history. The history only contains LPL regional finals (IG/TES/JDG/WE on patch 26.17) and Worlds play-in games (KC/C9/MVK/FURIA on patch 26.20). So there's no direct player-level evidence — I must rely on roster-strength priors.

**The matchup is heavily lopsided.** BLG fields a superteam (Bin, Knight, Viper, Xun, ON — multiple world-class players), while Movistar KOI's roster (Myrwn, Elyoya, Jojopyun, Supa, Alvaro) is a mid-table LEC lineup. Blue-side draft advantage and Bo1 variance help KOI somewhat, but not much.

**Base rates from the data** (for calibration context):
- Blue win rate overall: 19/34 = 56%
- Blue ahead at 15: 16/34 = 47%
- On the current patch (26.20), wins come from being ahead at 15 in ~69% of cases, so early leads matter but don't always convert.

**Forecast:**
- `p_blue_win = 0.15` — KOI winning a Bo1 against this BLG roster is roughly a 1-in-7 proposition, slightly above a pure talent read because of blue side and Bo1 upset potential.
- `p_blue_ahead_15 = 0.25` — KOI being ahead in early gold is more likely than winning (early skirmish variance), since they'd often fail to convert an early lead into a win against BLG's superior macro.
```

### 14. 终端命令

```
cat [ephemeral]/app/prediction.json
```

### 15. 命令结果

```
{"p_blue_win": 0.15, "p_blue_ahead_15": 0.25}
```

### 16. 模型消息

````
The prediction is saved to `./prediction.json`:

```json
{"p_blue_win": 0.15, "p_blue_ahead_15": 0.25}
```

Both values are finite and between 0 and 1. Forecast summary: Bilibili Gaming is the clear favorite on red side given their elite roster versus a mid-tier LEC Movistar KOI, with blue side and Bo1 variance giving KOI roughly a 15% win chance and a 25% chance of leading gold at 15 minutes.
````
