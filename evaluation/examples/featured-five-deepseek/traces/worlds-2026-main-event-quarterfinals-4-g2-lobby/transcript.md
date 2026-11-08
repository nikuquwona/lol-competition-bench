# Karmine Corp vs T1 · G2 · BP 前

worlds-2026-main-event · Quarterfinals · 26.20 · BO5

[实际题面](instruction.md) · [可查询的完整快照](snapshot.json) · [原始事件 JSONL](../../jobs/worlds-2026-main-event-quarterfinals-4-g2-lobby/trajectory.jsonl) · [stderr](../../jobs/worlds-2026-main-event-quarterfinals-4-g2-lobby/stderr.txt) · [交卷文件](../../jobs/worlds-2026-main-event-quarterfinals-4-g2-lobby/prediction.json)

## 输入与可查询证据

蓝方首发为 Busio, Caliste, Canna, Kyeahoo, Yike。

红方首发为 Doran, Faker, Keria, Oner, Peyz。

冻结时可查 96 个历史小局，10 名首发有历史出场记录。

本局可见 0 手禁选。

## 预测与赛后结算

```
{
  "status": "scored",
  "prediction": {
    "p_blue_win": 0.44,
    "p_blue_ahead_15": 0.6
  },
  "observed_outcome": {
    "p_blue_win": 0,
    "p_blue_ahead_15": 0
  },
  "brier": {
    "p_blue_win": 0.1936,
    "p_blue_ahead_15": 0.36
  },
  "reward": 0.7232000000000001
}
```

## CLI 报告的 token 用量

```
{
  "input_tokens": 252719,
  "cached_input_tokens": 246016,
  "cache_write_input_tokens": 0,
  "output_tokens": 15858,
  "reasoning_output_tokens": 11170
}
```

## 执行轨迹

### 1. CLI 诊断

```
Model metadata for `deepseek-v4-pro` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.
```

### 2. 模型消息

```
I'll start by inspecting the snapshot to understand its structure and relevant data.
```

### 3. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json
with open('snapshot.json') as f:
    d=json.load(f)
print('TOP KEYS:', list(d.keys()))
print()
print(json.dumps(d.get('current'), indent=2)[:3000])
\""
```

### 4. 命令输出

```
TOP KEYS: ['phase', 'series_time_utc', 'current', 'history', 'coverage']

{
  "event": "worlds-2026-main-event",
  "stage": "Quarterfinals",
  "series": "worlds-2026-main-event-quarterfinals-4",
  "n": 2,
  "patch": "26.20",
  "bo": 5,
  "blue": "Karmine Corp",
  "red": "T1",
  "starters": {
    "blue": [
      "Busio",
      "Caliste",
      "Canna",
      "Kyeahoo",
      "Yike"
    ],
    "red": [
      "Doran",
      "Faker",
      "Keria",
      "Oner",
      "Peyz"
    ]
  },
  "draft_rule": "Fearless"
}
```

### 5. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json
with open('snapshot.json') as f:
    d=json.load(f)
print('HISTORY LEN:', len(d['history']))
print('COVERAGE:', json.dumps(d['coverage'], indent=2))
print()
print('FIRST RECORD KEYS:', list(d['history'][0].keys()))
print(json.dumps(d['history'][0], indent=2)[:2000])
\""
```

### 6. 命令输出

```
HISTORY LEN: 96
COVERAGE: {
  "history_games": 96,
  "starters": [
    {
      "side": "blue",
      "name": "Busio",
      "games": 19,
      "same_patch_games": 19
    },
    {
      "side": "blue",
      "name": "Caliste",
      "games": 19,
      "same_patch_games": 19
    },
    {
      "side": "blue",
      "name": "Canna",
      "games": 19,
      "same_patch_games": 19
    },
    {
      "side": "blue",
      "name": "Kyeahoo",
      "games": 19,
      "same_patch_games": 19
    },
    {
      "side": "blue",
      "name": "Yike",
      "games": 19,
      "same_patch_games": 19
    },
    {
      "side": "red",
      "name": "Doran",
      "games": 6,
      "same_patch_games": 6
    },
    {
      "side": "red",
      "name": "Faker",
      "games": 6,
      "same_patch_games": 6
    },
    {
      "side": "red",
      "name": "Keria",
      "games": 6,
      "same_patch_games": 6
    },
    {
      "side": "red",
      "name": "Oner",
      "games": 6,
      "same_patch_games": 6
    },
    {
      "side": "red",
      "name": "Peyz",
      "games": 6,
      "same_patch_games": 6
    }
  ],
  "starters_with_history": 10,
  "coverage_group": "all",
  "previous_series_games": [
    1
  ],
  "missing_previous_series_games": []
}

FIRST RECORD KEYS: ['series', 'series_time', 'event', 'n', 'patch', 'blue', 'red', 'blue_win', 'blue_gd15', 'bp', 'players']
{
  "series": "lpl-2026-regional-finals-round-1-1",
  "series_time": "2026-09-17T09:00:00+00:00",
  "event": "lpl-2026-regional-finals",
  "n": 1,
  "patch": "26.17",
  "blue": "Invictus Gaming",
  "red": "Top Esports",
  "blue_win": true,
  "blue_gd15": -38,
  "bp": [
    {
      "turn": 1,
      "side": "red",
      "action": "ban",
      "champion": "Qiyana"
    },
    {
      "turn": 2,
      "side": "blue",
      "action": "ban",
      "champion": "Cassiopeia"
    },
    {
      "turn": 3,
      "side": "red",
      "action": "ban",
      "champion": "Olaf"
    },
    {
      "turn": 4,
      "side": "blue",
      "action": "ban",
      "champion": "Vi"
    },
    {
      "turn": 5,
      "side": "red",
      "action": "ban",
      "champion": "Jarvan IV"
    },
    {
      "turn": 6,
      "side": "blue",
      "action": "ban",
      "champion": "Nocturne"
    },
    {
      "turn": 7,
      "side": "red",
      "action": "pick",
      "champion": "Orianna"
    },
    {
      "turn": 8,
      "side": "blue",
      "action": "pick",
      "champion": "Lulu"
    },
    {
      "turn": 9,
      "side": "blue",
      "action": "pick",
      "champion": "Yunara"
    },
    {
      "turn": 10,
      "side": "red",
      "action": "pick",
      "champion": "Lucian"
    },
    {
      "turn": 11,
      "side": "red",
      "action": "pick",
      "champion": "Milio"
    },
    {
      "turn": 12,
      "side": "blue",
      "action": "pick",
      "champion": "Syndra"
    },
    {
      "turn": 13,
      "side": "blue",
      "action": "ban",
      "champion": "Trundle"
    },
    {
      "turn": 14,
      "side": "red",
      "action": "ban",
      "champion": "K'Sante"
    },
    {
      "turn": 15,
      "side": "blue",
      "action": "ban",
      "champion": "Rumble"
    },
    {
      "turn": 16,
      "side": "red",
      "action": "ban",
      "champion": "Renekton"
    },
    {
      "turn": 17,
      "side": "blue",
      "action": "pick",
      "champion":
```

### 7. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json
with open('snapshot.json') as f:
    d=json.load(f)
h=d['history']
# Find games involving KC or T1
kc=[g for g in h if g['blue']=='Karmine Corp' or g['red']=='Karmine Corp']
t1=[g for g in h if g['blue']=='T1' or g['red']=='T1']
print('KC games:', len(kc))
print('T1 games:', len(t1))
print()
# The current series game 1
s='worlds-2026-main-event-quarterfinals-4'
for g in h:
    if g['series']==s:
        print('SERIES GAME:', json.dumps(g, indent=2)[:2500])
\""
```

### 8. 命令输出

```
KC games: 19
T1 games: 6

SERIES GAME: {
  "series": "worlds-2026-main-event-quarterfinals-4",
  "series_time": "2026-11-06T22:00:00+00:00",
  "event": "worlds-2026-main-event",
  "n": 1,
  "patch": "26.20",
  "blue": "T1",
  "red": "Karmine Corp",
  "blue_win": true,
  "blue_gd15": -660,
  "bp": [
    {
      "turn": 1,
      "side": "red",
      "action": "ban",
      "champion": "Nocturne"
    },
    {
      "turn": 2,
      "side": "blue",
      "action": "ban",
      "champion": "Cassiopeia"
    },
    {
      "turn": 3,
      "side": "red",
      "action": "ban",
      "champion": "Renata Glasc"
    },
    {
      "turn": 4,
      "side": "blue",
      "action": "ban",
      "champion": "Vi"
    },
    {
      "turn": 5,
      "side": "red",
      "action": "ban",
      "champion": "Galio"
    },
    {
      "turn": 6,
      "side": "blue",
      "action": "ban",
      "champion": "Qiyana"
    },
    {
      "turn": 7,
      "side": "red",
      "action": "pick",
      "champion": "Rumble"
    },
    {
      "turn": 8,
      "side": "blue",
      "action": "pick",
      "champion": "Lulu"
    },
    {
      "turn": 9,
      "side": "blue",
      "action": "pick",
      "champion": "Jarvan IV"
    },
    {
      "turn": 10,
      "side": "red",
      "action": "pick",
      "champion": "Ezreal"
    },
    {
      "turn": 11,
      "side": "red",
      "action": "pick",
      "champion": "Leona"
    },
    {
      "turn": 12,
      "side": "blue",
      "action": "pick",
      "champion": "Yunara"
    },
    {
      "turn": 13,
      "side": "blue",
      "action": "ban",
      "champion": "Wukong"
    },
    {
      "turn": 14,
      "side": "red",
      "action": "ban",
      "champion": "Locke"
    },
    {
      "turn": 15,
      "side": "blue",
      "action": "ban",
      "champion": "Pantheon"
    },
    {
      "turn": 16,
      "side": "red",
      "action": "ban",
      "champion": "Orianna"
    },
    {
      "turn": 17,
      "side": "blue",
      "action": "pick",
      "champion": "Ornn"
    },
    {
      "turn": 18,
      "side": "red",
      "action": "pick",
      "champion": "Syndra"
    },
    {
      "turn": 19,
      "side": "red",
      "action": "pick",
      "champion": "Lee Sin"
    },
    {
      "turn": 20,
      "side": "blue",
      "action": "pick",
      "champion": "Viktor"
    }
  ],
  "players": [
    {
      "name": "Doran",
      "role": "Top",
      "side": "blue",
      "champion": "Ornn",
      "k": 1,
      "d": 3,
      "a": 13
    },
    {
      "n
```

### 9. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json
with open('snapshot.json') as f:
    d=json.load(f)
h=d['history']
def summarize(team):
    gs=[g for g in h if g['blue']==team or g['red']==team]
    wins=0; n=len(gs); ahead=0; gd_vals=[]
    print(f'=== {team}: {n} games ===')
    for g in gs:
        side='blue' if g['blue']==team else 'red'
        win = (g['blue_win'] if side=='blue' else not g['blue_win'])
        if win: wins+=1
        b_gd=g.get('blue_gd15')
        if b_gd is not None:
            gd = b_gd if side=='blue' else -b_gd
            gd_vals.append(gd)
            if gd>0: ahead+=1
        opp = g['red'] if side=='blue' else g['blue']
        print(f\\\"  n={g['n']} patch={g['patch']} side={side} vs {opp:20s} win={win} gd15={gd if b_gd is not None else None}\\\")
    print(f'  wins={wins}/{n}, ahead15={ahead}/{len(gd_vals)}, mean_gd15={sum(gd_vals)/len(gd_vals) if gd_vals else None}')
    print()
summarize('Karmine Corp')
summarize('T1')
\""
```

### 10. 命令输出

```
=== Karmine Corp: 19 games ===
  n=1 patch=26.20 side=blue vs Cloud9               win=False gd15=-1525
  n=2 patch=26.20 side=red vs Cloud9               win=True gd15=-395
  n=3 patch=26.20 side=blue vs Cloud9               win=False gd15=-236
  n=4 patch=26.20 side=red vs Cloud9               win=True gd15=4476
  n=5 patch=26.20 side=blue vs Cloud9               win=True gd15=622
  n=1 patch=26.20 side=blue vs MVK Esports          win=True gd15=3377
  n=2 patch=26.20 side=blue vs MVK Esports          win=True gd15=-3003
  n=3 patch=26.20 side=red vs MVK Esports          win=True gd15=2837
  n=1 patch=26.20 side=blue vs MVK Esports          win=True gd15=3288
  n=2 patch=26.20 side=blue vs MVK Esports          win=True gd15=6558
  n=3 patch=26.20 side=red vs MVK Esports          win=True gd15=2294
  n=1 patch=26.20 side=blue vs Anyone's Legend      win=True gd15=-461
  n=1 patch=26.20 side=blue vs LYON                 win=False gd15=2170
  n=1 patch=26.20 side=red vs Bilibili Gaming      win=False gd15=-1055
  n=1 patch=26.20 side=blue vs CTBC Flying Oyster   win=True gd15=1279
  n=2 patch=26.20 side=red vs CTBC Flying Oyster   win=True gd15=-3870
  n=1 patch=26.20 side=blue vs Movistar KOI         win=True gd15=1380
  n=2 patch=26.20 side=blue vs Movistar KOI         win=True gd15=4093
  n=1 patch=26.20 side=red vs T1                   win=False gd15=660
  wins=14/19, ahead15=12/19, mean_gd15=1183.6315789473683

=== T1: 6 games ===
  n=1 patch=26.20 side=red vs LØS                  win=True gd15=2368
  n=1 patch=26.20 side=red vs Dplus Kia            win=False gd15=3024
  n=1 patch=26.20 side=blue vs CTBC Flying Oyster   win=True gd15=-1582
  n=1 patch=26.20 side=blue vs Movistar KOI         win=True gd15=-138
  n=2 patch=26.20 side=blue vs Movistar KOI         win=True gd15=3510
  n=1 patch=26.20 side=blue vs Karmine Corp         win=True gd15=-660
  wins=5/6, ahead15=3/6, mean_gd15=1087.0
```

### 11. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json
with open('snapshot.json') as f:
    d=json.load(f)
h=d['history']
# overall blue win & blue ahead
bw=sum(1 for g in h if g['blue_win']); ba=sum(1 for g in h if g.get('blue_gd15') is not None and g['blue_gd15']>0)
n=len(h); ng=sum(1 for g in h if g.get('blue_gd15') is not None)
print(f'ALL {n} games: blue_win={bw/n:.3f}, blue_ahead15={ba}/{ng}={ba/ng:.3f}')
# patch 26.20
p=[g for g in h if g['patch']=='26.20']
bw=sum(1 for g in p if g['blue_win']); ba=sum(1 for g in p if g.get('blue_gd15') is not None and g['blue_gd15']>0)
ng=sum(1 for g in p if g.get('blue_gd15') is not None)
print(f'PATCH 26.20 {len(p)} games: blue_win={bw/len(p):.3f}, blue_ahead15={ba}/{ng}={ba/ng:.3f}')
# Worlds games only
w=[g for g in h if g['event']=='worlds-2026-main-event']
bw=sum(1 for g in w if g['blue_win']); ba=sum(1 for g in w if g.get('blue_gd15') is not None and g['blue_gd15']>0)
ng=sum(1 for g in w if g.get('blue_gd15') is not None)
print(f'WORLDS {len(w)} games: blue_win={bw/len(w):.3f}, blue_ahead15={ba}/{ng}={ba/ng:.3f}')
# KC side splits
kc=[g for g in h if g['blue']=='Karmine Corp' or g['red']=='Karmine Corp']
for side in ['blue','red']:
    gs=[g for g in kc if (g['blue'] if side=='blue' else g['red'])=='Karmine Corp']
    wins=sum(1 for g in gs if (g['blue_win'] if side=='blue' else not g['blue_win']))
    ahead=sum(1 for g in gs if g.get('blue_gd15') is not None and (g['blue_gd15'] if side=='blue' else -g['blue_gd15'])>0)
    ng=sum(1 for g in gs if g.get('blue_gd15') is not None)
    print(f'KC as {side}: {len(gs)} games, win={wins}/{len(gs)}, ahead15={ahead}/{ng}')
# T1 side splits
t1=[g for g in h if g['blue']=='T1' or g['red']=='T1']
for side in ['blue','red']:
    gs=[g for g in t1 if (g['blue'] if side=='blue' else g['red'])=='T1']
    wins=sum(1 for g in gs if (g['blue_win'] if side=='blue' else not g['blue_win']))
    ahead=sum(1 for g in gs if g.get('blue_gd15') is not None and (g['blue_gd15'] if side=='blue' else -g['blue_gd15'])>0)
    ng=sum(1 for g in gs if g.get('blue_gd15') is not None)
    print(f'T1 as {side}: {len(gs)} games, win={wins}/{len(gs)}, ahead15={ahead}/{ng}')
\""
```

### 12. 命令输出

```
ALL 96 games: blue_win=0.562, blue_ahead15=50/96=0.521
PATCH 26.20 84 games: blue_win=0.571, blue_ahead15=45/84=0.536
WORLDS 62 games: blue_win=0.565, blue_ahead15=34/62=0.548
KC as blue: 12 games, win=9/12, ahead15=8/12
KC as red: 7 games, win=5/7, ahead15=4/7
T1 as blue: 4 games, win=4/4, ahead15=1/4
T1 as red: 2 games, win=1/2, ahead15=2/2
```

### 13. 模型消息

```
Let me fit a quick strength model to ground the estimate before writing the file.
```

### 14. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json, math
with open('snapshot.json') as f:
    d=json.load(f)
h=d['history']
# Bradley-Terry with blue advantage via logistic
from collections import defaultdict
# iterative maximum likelihood (MM algorithm)
teams=set()
for g in h:
    teams.add(g['blue']); teams.add(g['red'])
teams=sorted(teams)
r={t:0.0 for t in teams}
b=0.0
def predict(bteam,rteam):
    return 1/(1+math.exp(-(b+r[bteam]-r[rteam])))
for it in range(200):
    # gradient ascent
    lr=0.1
    grad={t:0.0 for t in teams}
    gb=0.0
    for g in h:
        p=predict(g['blue'],g['red'])
        y=1 if g['blue_win'] else 0
        e=y-p
        gb+=e
        grad[g['blue']]+=e
        grad[g['red']]-=e
    for t in teams:
        r[t]+=lr*grad[t]
    b+=lr*gb
# center ratings
m=sum(r.values())/len(r)
for t in r: r[t]-=m
print('blue adv:', round(b,4))
for t in sorted(r, key=lambda x:-r[x])[:10]:
    print(f'{t:22s} {r[t]:+.3f}')
print()
print('KC rating', round(r.get('Karmine Corp',0),3), 'T1 rating', round(r.get('T1',0),3))
pb=predict('Karmine Corp','T1')
print('model p_blue_win (KC vs T1):', round(pb,3))
\""
```

### 15. 命令输出

```
blue adv: 0.0598
Gen.G                  +3.442
Bilibili Gaming        +2.418
Top Esports            +2.199
Invictus Gaming        +2.172
T1                     +1.862
Dplus Kia              +1.611
Hanwha Life Esports    +1.413
LYON                   +1.391
JD Gaming              +0.984
Karmine Corp           +0.731

KC rating 0.731 T1 rating 1.862
model p_blue_win (KC vs T1): 0.255
```

### 16. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json, math
with open('snapshot.json') as f:
    d=json.load(f)
h=d['history']
teams=set()
for g in h:
    teams.add(g['blue']); teams.add(g['red'])
teams=sorted(teams)
for lam in [0.0,1.0,2.0,5.0,10.0]:
    r={t:0.0 for t in teams}; b=0.0
    def predict(bt,rt): return 1/(1+math.exp(-(b+r[bt]-r[rt])))
    for it in range(500):
        lr=0.05
        gb=0.0; grad={t:0.0 for t in teams}
        for g in h:
            p=predict(g['blue'],g['red']); y=1 if g['blue_win'] else 0
            e=y-p; gb+=e; grad[g['blue']]+=e; grad[g['red']]-=e
        for t in teams:
            r[t]+=lr*(grad[t]-lam*r[t])
        b+=lr*gb
    m=sum(r.values())/len(r)
    for t in r: r[t]-=m
    p=predict('Karmine Corp','T1')
    print(f'lambda={lam}: KC={r[\\\"Karmine Corp\\\"]:+.3f} T1={r[\\\"T1\\\"]:+.3f} p_blue_win={p:.3f} blue_adv={b:.3f}')
\""
```

### 17. 命令输出

```
lambda=0.0: KC=+0.753 T1=+1.885 p_blue_win=0.255 blue_adv=0.060
lambda=1.0: KC=+0.667 T1=+0.791 p_blue_win=0.499 blue_adv=0.119
lambda=2.0: KC=+0.579 T1=+0.546 p_blue_win=0.545 blue_adv=0.149
lambda=5.0: KC=+0.407 T1=+0.290 p_blue_win=0.576 blue_adv=0.188
lambda=10.0: KC=+0.273 T1=+0.164 p_blue_win=0.580 blue_adv=0.212
```

### 18. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json, math
with open('snapshot.json') as f:
    d=json.load(f)
h=d['history']
teams=set()
for g in h:
    teams.add(g['blue']); teams.add(g['red'])
teams=sorted(teams)
idx={t:i for i,t in enumerate(teams)}
# proper logistic regression with L2, gradient ascent to max penalized log-lik
# model logit = b + r[blue]-r[red]
def fit(trainset, lam, iters=2000):
    r={t:0.0 for t in teams}; b=0.0
    for it in range(iters):
        lr=0.05
        gb=0.0; gr={t:0.0 for t in teams}
        for g in trainset:
            z=b+r[g['blue']]-r[g['red']]
            p=1/(1+math.exp(-z)); y=1 if g['blue_win'] else 0
            e=y-p
            gb+=e; gr[g['blue']]+=e; gr[g['red']]-=e
        b+=lr*gb
        for t in teams:
            r[t]+=lr*(gr[t]-lam*r[t])
    m=sum(r.values())/len(r)
    for t in r: r[t]-=m
    return r,b
for lam in [0.0,0.5,1.0,2.0,3.0,5.0,8.0,12.0,20.0]:
    # LOO
    ll=0.0
    for i,g in enumerate(h):
        tr=[x for j,x in enumerate(h) if j"'!=i]
        r,b=fit(tr,lam,iters=400)
        z=b+r[g['"'blue']]-r[g['red']]
        p=1/(1+math.exp(-z)); y=1 if g['blue_win'] else 0
        ll+= y*math.log(p+1e-9)+(1-y)*math.log(1-p+1e-9)
    print(f'lam={lam}: LOO loglik={ll:.2f}')
\""
```

### 19. 命令输出

```
lam=0.0: LOO loglik=-85.36
lam=0.5: LOO loglik=-65.71
lam=1.0: LOO loglik=-65.01
lam=2.0: LOO loglik=-65.06
lam=3.0: LOO loglik=-65.25
lam=5.0: LOO loglik=-65.56
lam=8.0: LOO loglik=-65.84
lam=12.0: LOO loglik=-66.05
lam=20.0: LOO loglik=-66.28
```

### 20. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json, math
with open('snapshot.json') as f:
    d=json.load(f)
h=d['history']
teams=set()
for g in h:
    teams.add(g['blue']); teams.add(g['red'])
teams=sorted(teams)
def fit(trainset, lam, iters=5000):
    r={t:0.0 for t in teams}; b=0.0
    for it in range(iters):
        lr=0.05
        gb=0.0; gr={t:0.0 for t in teams}
        for g in trainset:
            z=b+r[g['blue']]-r[g['red']]
            p=1/(1+math.exp(-z)); y=1 if g['blue_win'] else 0
            e=y-p
            gb+=e; gr[g['blue']]+=e; gr[g['red']]-=e
        b+=lr*gb
        for t in teams:
            r[t]+=lr*(gr[t]-lam*r[t])
    m=sum(r.values())/len(r)
    for t in r: r[t]-=m
    return r,b
for lam in [0.3,0.5,0.7,1.0,1.5,2.0]:
    r,b=fit(h,lam)
    z=b+r['Karmine Corp']-r['T1']
    p=1/(1+math.exp(-z))
    print(f'lam={lam}: blue_adv={b:.3f} KC={r[\\\"Karmine Corp\\\"]:+.3f} T1={r[\\\"T1\\\"]:+.3f} diff={r[\\\"Karmine Corp\\\"]-r[\\\"T1\\\"]:+.3f} p_blue_win={p:.3f}')
\""
```

### 21. 命令输出

```
lam=0.3: blue_adv=0.080 KC=+0.708 T1=+1.219 diff=-0.511 p_blue_win=0.394
lam=0.5: blue_adv=0.094 KC=+0.705 T1=+1.045 diff=-0.340 p_blue_win=0.439
lam=0.7: blue_adv=0.105 KC=+0.693 T1=+0.923 diff=-0.230 p_blue_win=0.469
lam=1.0: blue_adv=0.119 KC=+0.667 T1=+0.791 diff=-0.124 p_blue_win=0.499
lam=1.5: blue_adv=0.136 KC=+0.621 T1=+0.644 diff=-0.023 p_blue_win=0.528
lam=2.0: blue_adv=0.149 KC=+0.579 T1=+0.546 diff=+0.033 p_blue_win=0.545
```

### 22. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json, math
with open('snapshot.json') as f:
    d=json.load(f)
h=d['history']
# only games with gd15
gds=[g for g in h if g.get('blue_gd15') is not None]
teams=set()
for g in gds:
    teams.add(g['blue']); teams.add(g['red'])
teams=sorted(teams)
def fit(trainset, lam, iters=5000):
    r={t:0.0 for t in teams}; b=0.0
    for it in range(iters):
        lr=0.05
        gb=0.0; gr={t:0.0 for t in teams}
        for g in trainset:
            z=b+r[g['blue']]-r[g['red']]
            p=1/(1+math.exp(-z)); y=1 if g['blue_gd15']>0 else 0
            e=y-p
            gb+=e; gr[g['blue']]+=e; gr[g['red']]-=e
        b+=lr*gb
        for t in teams:
            r[t]+=lr*(gr[t]-lam*r[t])
    m=sum(r.values())/len(r)
    for t in r: r[t]-=m
    return r,b
for lam in [0.0,0.5,1.0,2.0]:
    r,b=fit(gds,lam)
    z=b+r['Karmine Corp']-r['T1']
    p=1/(1+math.exp(-z))
    print(f'lam={lam}: blue_adv={b:.3f} KC={r[\\\"Karmine Corp\\\"]:+.3f} T1={r[\\\"T1\\\"]:+.3f} diff={r[\\\"Karmine Corp\\\"]-r[\\\"T1\\\"]:+.3f} p_blue_ahead15={p:.3f}')
# also unregularized top teams
r,b=fit(gds,0.0)
print('top early teams:')
for t in sorted(r,key=lambda x:-r[x])[:8]:
    print(f'  {t:22s} {r[t]:+.3f}')
\""
```

### 23. 命令输出

```
lam=0.0: blue_adv=-0.103 KC=+0.149 T1=-0.046 diff=+0.195 p_blue_ahead15=0.523
lam=0.5: blue_adv=-0.033 KC=+0.451 T1=+0.016 diff=+0.435 p_blue_ahead15=0.599
lam=1.0: blue_adv=-0.014 KC=+0.436 T1=+0.007 diff=+0.429 p_blue_ahead15=0.602
lam=2.0: blue_adv=0.007 KC=+0.376 T1=+0.001 diff=+0.375 p_blue_ahead15=0.594
top early teams:
  JD Gaming              +2.037
  G2 Esports             +1.399
  Team WE                +0.936
  Invictus Gaming        +0.885
  Team Liquid            +0.702
  Cloud9                 +0.639
  Dplus Kia              +0.632
  Bilibili Gaming        +0.454
```

### 24. 模型消息

```
Now I'll write the forecast based on the team strength model, side effects, and early-game evidence.
```

### 25. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json
pred={'p_blue_win':0.44,'p_blue_ahead_15':0.60}
with open('prediction.json','w') as f:
    json.dump(pred,f)
print(open('prediction.json').read())
\""
```

### 26. 命令输出

```
{"p_blue_win": 0.44, "p_blue_ahead_15": 0.6}
```

### 27. 模型消息

```
I've saved the forecast. Quick verification of the final file:
```

### 28. 终端命令 · 退出码 0

```
/bin/zsh -lc "python3 -c \"
import json
d=json.load(open('prediction.json'))
assert set(d)=={'p_blue_win','p_blue_ahead_15'}
assert all(isinstance(v,(int,float)) and 0<=v<=1 for v in d.values())
print('valid:', d)
\""
```

### 29. 命令输出

```
valid: {'p_blue_win': 0.44, 'p_blue_ahead_15': 0.6}
```

### 30. 模型消息

````
Forecast saved to `prediction.json`:

```json
{"p_blue_win": 0.44, "p_blue_ahead_15": 0.6}
```

**Reasoning**
- `p_blue_win` (KC on blue): KC went 14-5 overall and 9-3 on blue side, while T1 went 5-1 and won the head-to-head game 1. Regularized team-strength modeling put the matchup near even after blue-side advantage, but T1's cleaner schedule and the game-1 result keep T1 slightly favored, landing KC around 44%.
- `p_blue_ahead_15`: KC was ahead at 15:00 in 12 of 19 games (67% on blue), and led at 15 in game 1. T1 was behind at 15 in three of four blue-side games, suggesting a weak early game despite strong late game, supporting ~60% for a KC early gold lead.
````
