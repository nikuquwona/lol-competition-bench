# Codex CLI × DeepSeek · draft-lock

下列为原生 CLI 逐步事件。较长的命令输出仅预览，完整值见 trajectory.jsonl。

## error

Model metadata for `deepseek-v4-pro` not found. Defaulting to fallback metadata; this can degrade performance and cause issues.

## 终端命令

~~~~sh
/bin/zsh -c "cat snapshot.json; echo '---'; ls -la; echo '---'; find . -maxdepth 2 -type f | head -100"
~~~~

退出码 0

~~~~
{"phase": "draft-lock", "series_time_utc": "2026-11-06T22:00:00+00:00", "current": {"event": "worlds-2026-main-event", "stage": "Quarterfinals", "series": "worlds-2026-main-event-quarterfinals-4", "n": 2, "patch": "26.20", "bo": 5, "blue": "Karmine Corp", "red": "T1", "starters": {"blue": ["Busio", "Caliste", "Canna", "Kyeahoo", "Yike"], "red": ["Doran", "Faker", "Keria", "Oner", "Peyz"]}, "draft_rule": "Fearless", "bp": [{"turn": 1, "side": "red", "action": "ban", "champion": "Locke"}, {"turn": 2, "side": "blue", "action": "ban", "champion": "Vi"}, {"turn": 3, "side": "red", "action": "ban", "champion": "Akali"}, {"turn": 4, "side": "blue", "action": "ban", "champion": "Qiyana"}, {"turn": 5, "side": "red", "action": "ban", "champion": "Renata Glasc"}, {"turn": 6, "side": "blue", "action": "ban", "champion": "Nocturne"}, {"turn": 7, "side": "red", "action": "pick", "champion": "Cassiopeia"}, {"turn": 8, "side": "blue", "action": "pick", "champion": "Orianna"}, {"turn": 9, "side": "blue", "action": "pick", "champion": "Pantheon"}, {"turn": 10, "side": "red", "action": "pick", "champion": "Olaf"}, {"turn": 11, "side": "red", "action": "pick", "champion": "Nautilus"}, {"turn": 12, "side": "blue", "action": "pick", "champion": "Ambessa"}, {"turn": 13, "side": "blue", "action": "ban", "champion": "Xin Zhao"}, {"turn": 14, "side": "red", "action": "ban", "champion": "Alistar"}, {"turn": 15, "side": "blue", "action": "ban", "champion": "Wukong"}, {"turn": 16, "side": "red", "action"
[…] {"name": "Busio", "role": "Support", "side": "red", "champion": "Leona", "k": 0, "d": 6, "a": 4}]}]}---
total 496
drwxr-xr-x@ 3 [user]  wheel      96 Nov  8 19:05 .
drwx------@ 8 [user]  wheel     256 Nov  8 19:05 ..
-rw-r--r--@ 1 [user]  wheel  252293 Nov  8 19:05 snapshot.json
---
./snapshot.json

~~~~

## 终端命令

~~~~sh
/bin/zsh -c "python3 - <<'PY'
import json, collections
snap=json.load(open('snapshot.json'))
hist=snap['history']
print('num history', len(hist))
# teams
teams=collections.Counter()
for g in hist:
    teams[g['blue']]+=1; teams[g['red']]+=1
print('num teams', len(teams))
# games involving T1 or Karmine Corp
for name in ['T1','Karmine Corp']:
    gs=[g for g in hist if g['blue']==name or g['red']==name]
    print(name, 'games', len(gs))
    wins=0; gd15s=[]
    for g in gs:
        blue_side = g['blue']==name
        win = g['blue_win'] if blue_side else not g['blue_win']
        wins+=win
        gd = g['blue_gd15'] if blue_side else -g['blue_gd15']
        gd15s.append((g['series_time'][:10], g['series'], g['n'], 'W' if win else 'L', gd, g['blue'], g['red']))
    print('  wins', wins, 'of', len(gs), 'winrate', wins/len(gs))
    for r in gd15s[-25:]:
        print('   ', r)
PY"
~~~~

退出码 0

~~~~
num history 96
num teams 21
T1 games 6
  wins 5 of 6 winrate 0.8333333333333334
    ('2026-10-23', 'worlds-2026-main-event-round-1-7', 1, 'W', 2368, 'LØS', 'T1')
    ('2026-10-24', 'worlds-2026-main-event-round-2-7', 1, 'L', 3024, 'Dplus Kia', 'T1')
    ('2026-10-26', 'worlds-2026-main-event-round-3-5', 1, 'W', -1582, 'T1', 'CTBC Flying Oyster')
    ('2026-10-28', 'worlds-2026-main-event-round-4-1', 1, 'W', -138, 'T1', 'Movistar KOI')
    ('2026-10-28', 'worlds-2026-main-event-round-4-1', 2, 'W', 3510, 'T1', 'Movistar KOI')
    ('2026-11-06', 'worlds-2026-main-event-quarterfinals-4', 1, 'W', -660, 'T1', 'Karmine Corp')
Karmine Corp games 19
  wins 14 of 19 winrate 0.7368421052631579
    ('2026-10-15', 'worlds-2026-play-in-round-1-1', 1, 'L', -1525, 'Karmine Corp', 'Cloud9')
    ('2026-10-15', 'worlds-2026-play-in-round-1-1', 2, 'W', -395, 'Cloud9', 'Karmine Corp')
    ('2026-10-15', 'worlds-2026-play-in-round-1-1', 3, 'L', -236, 'Karmine Corp', 'Cloud9')
    ('2026-10-15', 'worlds-2026-play-in-round-1-1', 4, 'W', 4476, 'Cloud9', 'Karmine Corp')
    ('2026-10-15', 'worlds-2026-play-in-round-1-1', 5, 'W', 622, 'Karmine Corp', 'Cloud9')
    ('2026-10-16', 'worlds-2026-play-in-round-2-1', 1, 'W', 3377, 'Karmine Corp', 'MVK Esports')
    ('2026-10-16', 'worlds-2026-play-in-round-2-1', 2, 'W', -3003, 'Karmine Corp', 'MVK Esports')
    ('2026-10-16', 'worlds-2026-play-in-round-2-1', 3, 'W', 2837, 'MVK Esports', 'Karmine Corp')
    ('2026-10-18', 'worlds-2026-play-in-round-3-1', 1, '
[…] )
    ('2026-10-31', 'worlds-2026-main-event-round-5-1', 1, 'W', 1380, 'Karmine Corp', 'Movistar KOI')
    ('2026-10-31', 'worlds-2026-main-event-round-5-1', 2, 'W', 4093, 'Karmine Corp', 'Movistar KOI')
    ('2026-11-06', 'worlds-2026-main-event-quarterfinals-4', 1, 'L', 660, 'T1', 'Karmine Corp')

~~~~

## 终端命令

~~~~sh
/bin/zsh -c "python3 - <<'PY'
import json, collections, statistics
snap=json.load(open('snapshot.json'))
hist=snap['history']
def team_gd(g,name):
    blue_side=g['blue']==name
    gd=g['blue_gd15']
    return gd if blue_side else -gd
for name in ['T1','Karmine Corp']:
    gs=[g for g in hist if g['blue']==name or g['red']==name]
    gds=[team_gd(g,name) for g in gs]
    ahead=sum(1 for x in gds if x>0)
    print(name,'n',len(gs),'winrate',sum(1 for g in gs if (g['blue']==name)==g['blue_win'])/len(gs))
    print('  gd15 mean',statistics.mean(gds),'median',statistics.median(gds),'ahead%',ahead/len(gds),'list',gds)
    # by side
    for side in ['blue','red']:
        sg=[g for g in gs if (g['blue']==name)==(side=='blue')]
        if sg:
            wins=sum(1 for g in sg if g['blue_win']==(side=='blue'))
            gds=[team_gd(g,name) for g in sg]
            print('  side',side,'n',len(sg),'winrate',wins/len(sg),'gd15mean',statistics.mean(gds),'ahead%',sum(1 for x in gds if x>0)/len(gds))
# main event only
for name in ['T1','Karmine Corp']:
    gs=[g for g in hist if (g['blue']==name or g['red']==name) and g['event']=='worlds-2026-main-event']
    wins=sum(1 for g in gs if (g['blue']==name)==g['blue_win'])
    gds=[team_gd(g,name) for g in gs]
    print(name,'main event',len(gs),'wins',wins,'winrate',wins/len(gs),'gd15mean',statistics.mean(gds),'ahead%',sum(1 for x in gds if x>0)/len(gds))
# opponents strength rough: average opponent winrate
print('--- opp winrate')
def opp_winrate(name):
    gs=[g for g in hist if g['blue']==name or g['red']==name]
    opps=[]
    for g in gs:
        opp = g['red'] if g['blue']==name else g['blue']
        og=[gg for gg in hist if gg['blue']==opp or gg['red']==opp]
        w=sum(1 for gg in og if (gg['blue']==opp)==gg['blue_win'])
        opps.append(w/len(og) if og else 0)
    return statistics.mean(opps)
for name in ['T1','Karmine Corp','Bilibili Gaming','Cloud9']:
    print(name, round(opp_winrate(name),3))
# game1 detail players
g1=[g for g in hist if g['series']=='worlds-2026-main-event-quarterfinals-4' and g['n']==1][0]
for p in g1['players']:
    print(p['side'],p['name'],p['role'],p['champion'],p['k'],p['d'],p['a'])
PY"
~~~~

退出码 0

~~~~
T1 n 6 winrate 0.8333333333333334
  gd15 mean 1087 median 1115.0 ahead% 0.5 list [2368, 3024, -1582, -138, 3510, -660]
  side blue n 4 winrate 1.0 gd15mean 282.5 ahead% 0.25
  side red n 2 winrate 0.5 gd15mean 2696 ahead% 1.0
Karmine Corp n 19 winrate 0.7368421052631579
  gd15 mean 1183.6315789473683 median 1279 ahead% 0.631578947368421 list [-1525, -395, -236, 4476, 622, 3377, -3003, 2837, 3288, 6558, 2294, -461, 2170, -1055, 1279, -3870, 1380, 4093, 660]
  side blue n 12 winrate 0.75 gd15mean 1461.8333333333333 ahead% 0.6666666666666666
  side red n 7 winrate 0.7142857142857143 gd15mean 706.7142857142857 ahead% 0.5714285714285714
T1 main event 6 wins 5 winrate 0.8333333333333334 gd15mean 1087 ahead% 0.5
Karmine Corp main event 8 wins 5 winrate 0.625 gd15mean 524.5 ahead% 0.625
--- opp winrate
T1 0.418
Karmine Corp 0.386
Bilibili Gaming 0.518
Cloud9 0.571
blue Doran Top Ornn 1 3 13
blue Oner Jungle Jarvan IV 4 1 18
blue Faker Mid Viktor 7 0 5
blue Peyz Bot Yunara 11 1 6
blue Keria Support Lulu 0 2 15
red Canna Top Rumble 2 4 3
red Yike Jungle Lee Sin 2 5 2
red Kyeahoo Mid Syndra 2 5 2
red Caliste Bot Ezreal 1 3 2
red Busio Support Leona 0 6 4

~~~~

## 终端命令

~~~~sh
/bin/zsh -c "python3 - <<'PY'
import json, math, statistics
snap=json.load(open('snapshot.json'))
hist=snap['history']
# chronological order
hist=sorted(hist, key=lambda g:g['series_time'])

# overall blue winrate and blue ahead rate
bw=sum(1 for g in hist if g['blue_win'])
ba=sum(1 for g in hist if g['blue_gd15']>0)
print('overall blue winrate', bw/len(hist), 'blue ahead15 rate', ba/len(hist), 'n', len(hist))

# Bradley-Terry with blue advantage via gradient ascent
teams=sorted(set([g['blue'] for g in hist]+[g['red'] for g in hist]))
r={t:0.0 for t in teams}
# gradient ascent for win model
for it in range(2000):
    grad={t:0.0 for t in teams}; grad_h=0.0
    for g in hist:
        rb=r[g['blue']]; rr=r[g['red']]
        z=rb-rr+home
        p=1/(1+math.exp(-z))
        y=1 if g['blue_win'] else 0
        grad[g['blue']]+=y-p
        grad[g['red']]-=(y-p)
        grad_h+=y-p
    for t in teams: r[t]+=0.05*grad[t]/len(hist)
    home+=0.05*grad_h/len(hist)
# not properly normalized; standardize
mean_r=statistics.mean(r.values())
r={t:v-mean_r for t,v in r.items()}
print('home adv', home)
for t in ['T1','Karmine Corp','Bilibili Gaming','Cloud9','Dplus Kia']:
    print(t, round(r[t],3))
rb=r['Karmine Corp']; rr=r['T1']
z=rb-rr+home
p_win=1/(1+math.exp(-z))
print('BT pred KC beats T1 (KC blue, T1 red):', p_win, 'z', z)

# gd15 ahead logistic using same rating diff: fit a*zdiff + b
# use zdiff = r_blue-r_red (no home)
import random
def logistic(z): return 1/(1+math.exp(-z))
a=1.0; b=0.0
for it in range(2000):
    ga=0; gb=0
    for g in hist:
        z=a*(r[g['blue']]-r[g['red']])+b
        p=logistic(z)
        y=1 if g['blue_gd15']>0 else 0
        ga+=(y-p)*(r[g['blue']]-r[g['red']])
        gb+=(y-p)
    a+=0.01*ga/len(hist)
    b+=0.01*gb/len(hist)
print('gd15 model a,b', a, b)
z15=a*(rb-rr)+b
p_ahead=logistic(z15)
print('pred KC ahead15 vs T1 (KC blue):', p_ahead, 'z15', z15)

# also simple Elo recency
elo={t:1500 for t in teams}
K=32
for g in hist:
    eb=1/(1+10**((elo[g['red']]-elo[g['blue']])/400))
    er=1-eb
    yb=1 if g['blue_win'] else 0
    elo[g['blue']]+=K*(yb-eb); elo[g['red']]+=K*(1-yb-er)
print('Elo', elo['Karmine Corp'], elo['T1'], 'diff', elo['Karmine Corp']-elo['T1'])
eb=1/(1+10**((elo['T1']-elo['Karmine Corp'])/400))
print('Elo pred KC', eb)

# recent main event form for these two
for name in ['T1','Karmine Corp']:
    gs=[g for g in hist if (g['blue']==name or g['red']==name) and g['event']=='worlds-2026-main-event']
    gds=[ (g['blue_gd15'] if g['blue']==name else -g['blue_gd15']) for g in gs]
    wins=sum(1 for g in gs if (g['blue']==name)==g['blue_win'])
    print(name,'main',len(gs),'w',wins,'gd15mean',round(statistics.mean(gds),1),'ahead%',round(sum(1 for x in gds if x>0)/len(gds),3))
PY"
~~~~

退出码 1

~~~~
Traceback (most recent call last):
  File "<stdin>", line 20, in <module>
overall blue winrate 0.5625 blue ahead15 rate 0.5208333333333334 n 96
NameError: name 'home' is not defined

~~~~

## 终端命令

~~~~sh
/bin/zsh -c "python3 - <<'PY'
import json, math, statistics
snap=json.load(open('snapshot.json'))
hist=sorted(snap['history'], key=lambda g:g['series_time'])
teams=sorted(set([g['blue'] for g in hist]+[g['red'] for g in hist]))

# Bradley-Terry win model with blue-side home advantage
r={t:0.0 for t in teams}; home=0.0
for it in range(3000):
    grad={t:0.0 for t in teams}; gh=0.0
    for g in hist:
        z=r[g['blue']]-r[g['red']]+home
        p=1/(1+math.exp(-z)); y=1 if g['blue_win'] else 0
        d=y-p
        grad[g['blue']]+=d; grad[g['red']]-=d; gh+=d
    lr=0.02
    for t in teams: r[t]+=lr*grad[t]/len(hist)
    home+=lr*gh/len(hist)
mean_r=statistics.mean(r.values())
r={t:v-mean_r for t,v in r.items()}
print('BT home', round(home,4))
for t in ['T1','Karmine Corp','Bilibili Gaming','Dplus Kia','Cloud9']:
    print(' ',t,round(r[t],3))

# logistic for ahead15 using rating diff
a=1.0; b=0.0
for it in range(3000):
    ga=gb=0.0
    for g in hist:
        z=a*(r[g['blue']]-r[g['red']])+b
        p=1/(1+math.exp(-z)); y=1 if g['blue_gd15']>0 else 0
        d=y-p
        ga+=d*(r[g['blue']]-r[g['red']]); gb+=d
    a+=0.005*ga/len(hist); b+=0.005*gb/len(hist)
print('ahead model a,b', round(a,4), round(b,4))

zd=r['Karmine Corp']-r['T1']+home
pw=1/(1+math.exp(-zd))
za=a*(r['Karmine Corp']-r['T1'])+b
pa=1/(1+math.exp(-za))
print('zdiff KC-T1', round(r['Karmine Corp']-r['T1'],4))
print('BT p_win', round(pw,4), 'p_ahead15', round(pa,4))

# Elo recency
elo={t:1500 for t in teams}
for g in hist:
    eb=1/(1+10**((elo[g['red']]-elo[g['blue']])/400))
    er=1-eb
    yb=1 if g['blue_win'] else 0
    elo[g['blue']]+=32*(yb-eb); elo[g['red']]+=32*(1-yb-er)
eb=1/(1+10**((elo['T1']-elo['Karmine Corp'])/400))
print('Elo KC,T1', round(elo['Karmine Corp'],1), round(elo['T1'],1), 'Elo p_KC', round(eb,4))

# side and opponent-adj rough
for name in ['T1','Karmine Corp']:
    gs=[g for g in hist if (g['blue']==name or g['red']==name)]
    print(name, 'all', len(gs), 'win', sum(1 for g in gs if (g['blue']==name)==g['blue_win']))
    for side in ['blue','red']:
        sg=[g for g in gs if (g['blue']==name)==(side=='blue')]
        if sg:
            print('  ',side,len(sg),'win',sum(1 for g in sg if g['blue_win']==(side=='blue')),'ahead15',sum(1 for g in sg if (g['blue_gd15'] if g['blue']==name else -g['blue_gd15'])>0))
PY"
~~~~

退出码 0

~~~~
BT home 0.1166
  T1 0.778
  Karmine Corp 0.801
  Bilibili Gaming 0.881
  Dplus Kia 0.267
  Cloud9 -0.346
ahead model a,b 0.5415 -0.0142
zdiff KC-T1 0.0227
BT p_win 0.5348 p_ahead15 0.4995
Elo KC,T1 1598.2 1564.5 Elo p_KC 0.5483
T1 all 6 win 5
   blue 4 win 4 ahead15 1
   red 2 win 1 ahead15 2
Karmine Corp all 19 win 14
   blue 12 win 9 ahead15 8
   red 7 win 5 ahead15 4

~~~~

## 终端命令

~~~~sh
/bin/zsh -c "python3 - <<'PY'
import json, math, statistics
snap=json.load(open('snapshot.json'))
hist=sorted(snap['history'], key=lambda g:g['series_time'])
teams=sorted(set([g['blue'] for g in hist]+[g['red'] for g in hist]))

def bt(games, prior_scale=0.0, iters=3000):
    r={t:0.0 for t in teams}; home=0.0
    for it in range(iters):
        grad={t:0.0 for t in teams}; gh=0.0
        for g in games:
            z=r[g['blue']]-r[g['red']]+home
            p=1/(1+math.exp(-z)); y=1 if g['blue_win'] else 0
            d=y-p
            grad[g['blue']]+=d; grad[g['red']]-=d; gh+=d
        lr=0.02
        for t in teams: r[t]+=lr*grad[t]/len(games)
        home+=lr*gh/len(games)
    mean_r=statistics.mean(r.values())
    r={t:v-mean_r for t,v in r.items()}
    return r, home

r_all, home_all = bt(hist)
main=[g for g in hist if g['event']=='worlds-2026-main-event']
r_main, home_main = bt(main)
print('ALL home', round(home_all,4), 'n', len(hist))
print('  T1', round(r_all['T1'],3), 'KC', round(r_all['Karmine Corp'],3), 'BLG', round(r_all['Bilibili Gaming'],3), 'DK', round(r_all['Dplus Kia'],3))
print('MAIN home', round(home_main,4), 'n', len(main))
for t in ['T1','Karmine Corp','Bilibili Gaming','Dplus Kia','LYON','Movistar KOI','CTBC Flying Oyster']:
    if t in r_main:
        print('  ',t, round(r_main[t],3))

zd_all=r_all['Karmine Corp']-r_all['T1']+home_all
zd_main=r_main['Karmine Corp']-r_main['T1']+home_main
print('p_win allBT', round(1/(1+math.exp(-zd_all)),4), 'mainBT', round(1/(1+math.exp(-zd_main)),4))

# write chosen prediction
pred={'p_blue_win':0.26,'p_blue_ahead_15':0.48}
json.dump(pred, open('prediction.json','w'))
print('wrote', pred)
PY
cat prediction.json"
~~~~

退出码 0

~~~~
ALL home 0.1166 n 96
  T1 0.778 KC 0.801 BLG 0.881 DK 0.267
MAIN home 0.0713 n 62
   T1 0.909
   Karmine Corp 0.273
   Bilibili Gaming 0.943
   Dplus Kia 0.353
   LYON 0.26
   Movistar KOI -0.642
   CTBC Flying Oyster -0.791
p_win allBT 0.5348 mainBT 0.3625
wrote {'p_blue_win': 0.26, 'p_blue_ahead_15': 0.48}
{"p_blue_win": 0.26, "p_blue_ahead_15": 0.48}
~~~~

## 终端命令

~~~~sh
/bin/zsh -c "python3 - <<'PY'
import json
pred={'p_blue_win':0.32,'p_blue_ahead_15':0.44}
json.dump(pred, open('prediction.json','w'))
print(open('prediction.json').read())
PY"
~~~~

退出码 0

~~~~
{"p_blue_win": 0.32, "p_blue_ahead_15": 0.44}

~~~~

## agent_message

Wrote `prediction.json`:

```json
{"p_blue_win": 0.32, "p_blue_ahead_15": 0.44}
```

Basis: T1 is favored (main-event rating ~0.91 vs Karmine Corp ~0.27, and T1 won game 1 decisively), but KC gets blue side and had early gold leads in game 1, keeping `p_blue_ahead_15` near even.
