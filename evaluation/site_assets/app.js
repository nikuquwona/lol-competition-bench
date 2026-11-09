"use strict";
const main = document.querySelector("main");
const fmt = new Intl.NumberFormat("zh-CN");
const labels = {
  live: "实时推理",
  "openrouter-free": "OpenRouter 免费模型",
  controlled: "受控模型",
  baseline: "历史基线",
  fixture: "固定响应",
  vendor: "厂商通道",
  boundary: "防穿越验收",
  full: "全量",
  subset: "子集",
  completed: "已完成",
  scored: "已评分",
  failed: "失败",
  started: "已启动",
  partial: "部分完成",
  unfinished: "未完成",
  interrupted: "已中断",
  passed: "通过",
  unverified: "待核验",
  ineligible: "超出窗口",
  lobby: "BP 前",
  "draft-lock": "BP 后",
  macos: "macOS",
  harbor: "Harbor",
  local: "本地",
  docker: "Docker",
  release_labels: "标签已核验",
  report_consistency: "报告自洽检查",
};
const display = (v) =>
  Object.hasOwn(labels, v) ? labels[v] : String(v ?? "—");
const nfmt = (n) => (Number.isFinite(n) ? fmt.format(n) : "—");
const fixed = (n) => (Number.isFinite(n) ? n.toFixed(4) : "—");
const pct = (n) => (Number.isFinite(n) ? (n * 100).toFixed(1) + "%" : "—");
const enc = encodeURIComponent;
const runPath = (id) => "#/runs/" + enc(id);
const taskPath = (id, key) => runPath(id) + "/trials/" + enc(key);
const baseApi = (id) => "/api/runs/" + enc(id);
const phase = (t) =>
  t.phase ||
  (t.task?.endsWith("-draft-lock")
    ? "draft-lock"
    : t.task?.endsWith("-lobby")
      ? "lobby"
      : null);
const trialKey = (t) =>
  t.scope && t.harness ? t.harness + "--" + t.task : t.task;
const modelTitles = {
  "deepseek-v4-pro": "DeepSeek V4 Pro",
  "nvidia/nemotron-3.5-lightning:free": "Nemotron 3.5 Lightning",
};
const humanModel = (id) =>
  Object.hasOwn(modelTitles, id) ? modelTitles[id] : id;
const modelName = (r) =>
  humanModel(r.model) ||
  (r.mode === "baseline"
    ? "选手历史基线"
    : r.mode === "boundary"
      ? "隔离验收"
      : r.name || r.id);
let active;
function node(tag, cls, ...children) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  for (const c of children.flat(Infinity))
    if (c !== null && c !== undefined && c !== false) e.append(c);
  return e;
}
const div = (cls, ...children) => node("div", cls, ...children);
const span = (cls, ...children) => node("span", cls, ...children);
const empty = (text) => node("p", "notice", text);
function link(text, href, cls) {
  const a = node("a", cls, text);
  a.href = href;
  return a;
}
function action(text, fn) {
  const b = node("button", "btn", text);
  b.type = "button";
  b.addEventListener("click", fn);
  return b;
}
function badge(key) {
  const color = ["completed", "scored", "passed", "controlled"].includes(key)
    ? " ok"
    : ["failed", "interrupted", "partial", "ineligible"].includes(key)
      ? " warn"
      : "";
  return span("badge" + color, display(key));
}
function dateText(value) {
  const t = new Date(value);
  return value && Number.isFinite(t.valueOf())
    ? new Intl.DateTimeFormat("zh-CN", {
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      }).format(t)
    : "—";
}
async function json(url, signal) {
  const r = await fetch(url, {
    signal,
    headers: { Accept: "application/json" },
  });
  if (!r.ok) throw Error("请求失败（HTTP " + r.status + "）");
  return r.json();
}
function apiFile(value) {
  if (typeof value !== "string") return null;
  try {
    const u = new URL(value, location.origin);
    return u.origin === location.origin &&
      !u.username &&
      !u.password &&
      u.pathname.startsWith("/api/")
      ? u.href
      : null;
  } catch {
    return null;
  }
}
function heading(title, desc, metrics = [], context = null) {
  return node(
    "header",
    "hero",
    div(
      "",
      context && div("eyebrow", context),
      node("h1", "", title),
      desc && node("p", "sub", desc),
    ),
    (metrics.length &&
      div(
        "metrics",
        metrics.map(([label, value]) =>
          div("metric", node("strong", "", value), span("", label)),
        ),
      )) ||
      null,
  );
}
function box(title, content, extra = null, cls = "") {
  return node(
    "section",
    "panel " + cls,
    div("panel-head", node("h2", "", title), extra),
    content,
  );
}
function table(headers, rows, caption) {
  const t = node("table", "");
  if (caption) t.setAttribute("aria-label", caption);
  t.append(
    node(
      "thead",
      "",
      node(
        "tr",
        "",
        headers.map((h) => {
          const c = node("th", h[1] || "", h[0]);
          c.scope = "col";
          return c;
        }),
      ),
    ),
    node(
      "tbody",
      "",
      rows.map((r) =>
        node(
          "tr",
          "",
          r.map((v, i) => {
            const cell = node("td", headers[i]?.[1] || "", v);
            cell.dataset.label = headers[i]?.[0] || "";
            return cell;
          }),
        ),
      ),
    ),
  );
  const wrap = div("table-wrap", t);
  wrap.tabIndex = 0;
  wrap.setAttribute("role", "region");
  wrap.setAttribute("aria-label", caption || "数据表");
  return wrap;
}
function choice(title, opts, value, onChange, wide = false) {
  const s = node("select", wide ? "wide-select" : "");
  s.setAttribute("aria-label", title);
  for (const [val, name] of opts) {
    const o = node("option", "", name);
    o.value = val;
    s.append(o);
  }
  s.value = value;
  s.addEventListener("change", () => onChange(s.value));
  return node("label", "", title, s);
}
const field = (k, v) =>
  div("data-field", span("", k), node("strong", "", v ?? "—"));
const crumb = (...parts) =>
  node(
    "nav",
    "crumbs",
    parts.flatMap((x, i) => (i ? [span("", "/"), x] : [x])),
  );
const harnessNames = {
  codex: "Codex",
  claude: "Claude Code",
  cursor: "Cursor",
  pi: "Pi",
  kimi: "Kimi Code",
};
const isForecast = (r) =>
  ["live", "openrouter-free", "vendor"].includes(r.mode);
const harnessName = (h) => harnessNames[h] || h || "—";
function pageHeading(title, description, actions = null) {
  return node(
    "header",
    "report-heading",
    div("", node("h1", "", title), description && node("p", "", description)),
    actions,
  );
}
function gameNumber(task) {
  const match = String(task || "").match(/-g(\d+)-(lobby|draft-lock)$/);
  return match ? Number(match[1]) : null;
}
function asGames(report, fixtures) {
  const byId = new Map((report.trials || []).map((t) => [t.task, t]));
  if (fixtures?.length) {
    return fixtures.map((f) => {
      const pair = {};
      for (const ph of ["lobby", "draft-lock"]) {
        const id = f.tasks?.[ph] || f.tasks?.[ph.replace("-", "_")];
        if (id)
          pair[ph] = byId.get(id) || {
            task: id,
            status: "unattempted",
            phase: ph,
          };
      }
      return { ...f, pair };
    });
  }
  const games = new Map();
  for (const id of report.planned?.length ? report.planned : byId.keys()) {
    const t = byId.get(id) || { task: id, status: "unattempted" },
      ph = phase(t),
      base = id.replace(/-(lobby|draft-lock)$/, "");
    if (!ph) continue;
    const m = t.match || {};
    if (!games.has(base))
      games.set(base, {
        series: base.replace(/-g\d+$/, ""),
        game: m.n || gameNumber(id),
        pair: {},
      });
    const g = games.get(base);
    Object.assign(
      g,
      Object.fromEntries(
        Object.entries({
          blue: m.blue,
          red: m.red,
          blue_logo: m.blue_logo,
          red_logo: m.red_logo,
          patch: t.patch,
          stage: m.stage,
          bo: m.bo,
        }).filter(([, v]) => v != null),
      ),
    );
    g.pair[ph] = t;
  }
  return [...games.values()];
}
function gameResult(g) {
  return (
    g.pair.lobby?.observed_outcome ||
    g.pair["draft-lock"]?.observed_outcome ||
    g.observed_outcome ||
    {}
  );
}
function gameLabel(g) {
  const event = g.series?.startsWith("lpl-")
    ? "LPL 区域资格赛"
    : g.series?.includes("-play-in-")
      ? "世界赛入围赛"
      : g.series?.startsWith("worlds-")
        ? "世界赛"
        : g.series || "赛事";
  const round = /^Round (\d+)$/i.exec(g.stage || "");
  const stage = round
    ? "第 " + round[1] + " 轮"
    : { Quarterfinals: "八强赛", Semifinals: "半决赛", Finals: "决赛" }[
        g.stage
      ] || g.stage;
  const label = div(
    "game-id",
    span("game-event", event),
    span(
      "game-stage",
      [stage, g.game && "G" + g.game].filter(Boolean).join(" · "),
    ),
  );
  label.title = [
    event,
    stage,
    g.game && "第 " + g.game + " 局",
    g.bo && "BO" + g.bo,
    g.patch && "Patch " + g.patch,
  ]
    .filter(Boolean)
    .join(" · ");
  return label;
}
function teamLine(g, side) {
  const wrap = div("game-club " + side + "-team"),
    name = g[side] || (side === "blue" ? "蓝方" : "红方"),
    src = g[side + "_logo"];
  if (typeof src === "string" && /^\/teams\/[a-zA-Z0-9_-]+\.png$/.test(src)) {
    const img = node("img", "team-logo");
    img.src = src;
    img.alt = "";
    img.width = 25;
    img.height = 25;
    img.addEventListener("error", () => img.remove(), { once: true });
    wrap.append(img);
  }
  wrap.append(span("", name));
  return wrap;
}
function phaseCells(runId, t, ph, failedLoad = false) {
  let title = "—",
    url = null;
  if (failedLoad) title = "读取失败";
  else if (!t) title = "—";
  else if (t.status === "scored") {
    const a = link(
      pct(t.prediction?.p_blue_win),
      taskPath(runId, trialKey(t)),
      "forecast-link",
    );
    a.setAttribute(
      "aria-label",
      display(ph) +
        "蓝方胜率 " +
        pct(t.prediction?.p_blue_win) +
        "，查看逐题轨迹",
    );
    return [a, pct(t.prediction?.p_blue_ahead_15), fixed(t.reward)];
  } else if (!["unattempted", "unstarted", "not_run"].includes(t.status)) {
    const limited =
      t.failure_kind === "rate_limit" ||
      t.runtime?.upstream?.at(-1)?.status === 429 ||
      /(?:HTTP statuses?\s*\[[\d,\s]*\b429\s*\]|HTTP 429|rate.limit)/i.test(
        String(t.error || ""),
      );
    title = ["started", "pending"].includes(t.status)
      ? "进行中"
      : limited
        ? "限流"
        : display(t.status);
    if (t.runtime || !["started", "pending"].includes(t.status))
      url = taskPath(runId, trialKey(t));
  }
  return [
    url ? link(title, url, "trial-state failed") : span("trial-state", title),
    "—",
    "—",
  ];
}
function winDelta(pair) {
  const before = pair.lobby?.prediction?.p_blue_win,
    after = pair["draft-lock"]?.prediction?.p_blue_win;
  if (!Number.isFinite(before) || !Number.isFinite(after)) return "—";
  const delta = (after - before) * 100;
  return (delta > 0 ? "+" : "") + delta.toFixed(1);
}
function headerCell(label, scope, rows = 1, columns = 1, cls = "") {
  const th = node("th", cls, label);
  th.scope = scope;
  if (rows !== 1) th.rowSpan = rows;
  if (columns !== 1) th.colSpan = columns;
  return th;
}
function dataCell(value, cls = "", rows = 1) {
  const td = node("td", cls, value);
  if (rows !== 1) td.rowSpan = rows;
  return td;
}
// Each game is one table row group. Teams and outcomes span its model/CLI entries.
function resultsGrid(games, combinations, compare) {
  if (!games.length) return empty("此题单没有已登记的对局。");
  if (!combinations.length) return empty("没有匹配的模型运行。");
  const grid = node("table", "game-grid" + (compare ? " comparison-grid" : ""));
  grid.setAttribute("aria-label", "逐场预测、真实赛果与 BP 前后评分");
  const widths = {
    event: compare ? 10 : 13,
    blue: compare ? 9 : 12,
    red: compare ? 9 : 12,
    model: 9,
    cli: 7,
    win: compare ? 6 : 7.5,
    ahead: compare ? 6 : 7.5,
    reward: compare ? 6 : 7.5,
    delta: 6,
    winner: compare ? 8 : 8,
    aheadResult: compare ? 6 : 6,
  };
  const group = (keys) => {
    const cg = node("colgroup", "");
    for (const key of keys) {
      const col = node("col", "");
      col.style.width = widths[key] + "%";
      cg.append(col);
    }
    grid.append(cg);
  };
  group(["event"]);
  group(["blue", "red"]);
  if (compare) group(["model", "cli"]);
  group(["win", "ahead", "reward"]);
  group(["win", "ahead", "reward"]);
  group(["delta"]);
  group(["winner", "aheadResult"]);
  const top = node(
    "tr",
    "metric-groups",
    headerCell("赛事 / 局次", "col", 2),
    headerCell("对阵", "colgroup", 1, 2),
  );
  if (compare) top.append(headerCell("参赛组合", "colgroup", 1, 2));
  const change = headerCell("胜率变化", "col", 2, 1, "group-start");
  change.append(span("unit", "百分点"));
  change.title = "BP 后蓝方胜率减 BP 前蓝方胜率";
  top.append(
    headerCell("BP 前预测", "colgroup", 1, 3, "group-start pre-header"),
    headerCell("BP 后预测", "colgroup", 1, 3, "group-start post-header"),
    change,
    headerCell("真实赛果", "colgroup", 1, 2, "group-start"),
  );
  const sub = node(
    "tr",
    "metric-headings",
    headerCell("蓝方", "col", 1, 1, "blue-label"),
    headerCell("红方", "col", 1, 1, "red-label"),
  );
  if (compare) sub.append(headerCell("模型", "col"), headerCell("CLI", "col"));
  for (let i = 0; i < 2; i++)
    sub.append(
      headerCell("蓝方胜率", "col", 1, 1, "group-start numeric"),
      headerCell("15′ 蓝方领先", "col", 1, 1, "numeric"),
      headerCell("得分", "col", 1, 1, "numeric"),
    );
  sub.append(
    headerCell("胜方", "col", 1, 1, "group-start"),
    headerCell("蓝方领先@15", "col"),
  );
  grid.append(node("thead", "", top, sub));
  for (const g of games) {
    const body = node("tbody", "fixture-group");
    const rows = combinations.filter(
      (combo) =>
        combo.failedLoad ||
        Object.values(combo.games.get(gameKey(g))?.pair || {}).some(
          (t) =>
            t &&
            ![
              "unattempted",
              "unstarted",
              "not_started",
              "not_run",
              "environment_error",
            ].includes(t.status),
        ),
    );
    const spanRows = Math.max(1, rows.length);
    const result = gameResult({ ...g, pair: g.pair || {} });
    const winner =
      result.p_blue_win === 1 ? "blue" : result.p_blue_win === 0 ? "red" : null;
    const gold =
      result.p_blue_ahead_15 === 1
        ? "是"
        : result.p_blue_ahead_15 === 0
          ? "否"
          : "—";
    for (let i = 0; i < spanRows; i++) {
      const combo = rows[i];
      const tr = node("tr", ""),
        game = combo?.games.get(gameKey(g)),
        pair = game?.pair || {};
      if (i === 0)
        tr.append(
          headerCell(gameLabel(g), "rowgroup", spanRows, 1, "game-key"),
          dataCell(teamLine(g, "blue"), "club-data", spanRows),
          dataCell(teamLine(g, "red"), "club-data", spanRows),
        );
      if (!combo) {
        const vacant = dataCell("该场无运行记录", "no-trial");
        vacant.colSpan = compare ? 9 : 7;
        tr.append(vacant);
      } else {
        if (compare) {
          const model = link(
            humanModel(combo.model),
            runPath(combo.id),
            "entry-model",
          );
          model.title = combo.model;
          tr.append(
            headerCell(model, "row", 1, 1, "entrant-key"),
            dataCell(harnessName(combo.harness), "cli-data"),
          );
        }
        for (const ph of ["lobby", "draft-lock"]) {
          const value = phaseCells(combo.id, pair[ph], ph, combo.failedLoad);
          tr.append(
            dataCell(value[0], "numeric group-start win-data"),
            dataCell(value[1], "numeric"),
            dataCell(value[2], "numeric reward-data"),
          );
        }
        tr.append(dataCell(winDelta(pair), "numeric group-start delta-data"));
      }
      if (i === 0)
        tr.append(
          dataCell(
            winner
              ? span(
                  "outcome-" + winner,
                  g[winner] || (winner === "blue" ? "蓝方" : "红方"),
                )
              : "—",
            "group-start winner-data",
            spanRows,
          ),
          dataCell(gold, "result-gold", spanRows),
        );
      body.append(tr);
    }
    grid.append(body);
  }
  const wrap = div("game-grid-scroll matches-table", grid);
  wrap.tabIndex = 0;
  wrap.setAttribute("role", "region");
  wrap.setAttribute("aria-label", "逐场预测明细，可横向滚动");
  return wrap;
}
const gameKey = (g) => String(g.series) + "#" + String(g.game ?? g.n);
function matchTable(games, runId) {
  return resultsGrid(
    games,
    [{ id: runId, games: new Map(games.map((g) => [gameKey(g), g])) }],
    false,
  );
}
function seasonVisual() {
  const img = node("img", "season-art");
  img.src = "/media/worlds-2026.webp";
  img.alt = "2026 全球总决赛官方主视觉，亚索越过蓝紫色城市上空";
  img.width = 1440;
  img.height = 605;
  img.fetchPriority = "high";
  const credit = link(
    "全球总决赛",
    "https://lolesports.com/en-GB/news/worlds-2026-primer",
    "season-title",
  );
  credit.title = "Riot Games / LoL Esports 官方主视觉与赛事资料";
  return node(
    "figure",
    "event-visual",
    img,
    node("figcaption", "", span("season-year", "2026"), credit),
  );
}
function quarterfinalWalkout() {
  const figure = node("figure", "walkout");
  const photos = [
    [
      "Karmine Corp",
      "/media/kc-walkout.webp",
      "https://www.flickr.com/photos/lolesports/55637131328/",
    ],
    [
      "T1",
      "/media/t1-walkout.webp",
      "https://www.flickr.com/photos/lolesports/55637131263/",
    ],
  ];
  for (const [team, src, source] of photos) {
    const img = node("img", "walkout-photo");
    img.src = src;
    img.alt = team + " 在 2026 世界赛八强系列赛入场";
    img.width = 900;
    img.height = 601;
    const a = link("", source, "walkout-image");
    a.title = team + " · Riot Games 原片";
    a.append(img, span("", team));
    figure.append(a);
  }
  figure.append(
    node(
      "figcaption",
      "",
      node("strong", "", "世界赛八强 · 系列赛入场"),
      span("", "2026.11.06"),
      span("", "摄影　Yicun Liu / Riot Games"),
    ),
  );
  return figure;
}
function isQuarterfinal(series) {
  return series === "worlds-2026-main-event-quarterfinals-4";
}
function fixtureHead(title, controls) {
  return div(
    "fixture-head",
    div("", node("h2", "", "逐场预测"), title && span("selected-pair", title)),
    controls,
  );
}
function rankingTable(entries) {
  const groups = new Set(
    entries.map((e) =>
      [e.backend, e.track, e.protocol || "suite-v1"].join("/"),
    ),
  );
  const showScope = groups.size > 1;
  const headers = [
    ["排名"],
    ["模型"],
    ["Harness"],
    ...(showScope ? [["比较组"]] : []),
    ["交卷", "right"],
    ["BP 前均分", "right"],
    ["BP 后均分", "right"],
    ["综合得分", "right"],
  ];
  const rows = entries.map((e) => {
    const score = (ph) => {
      const stats = e.by_phase?.[ph] || {};
      const value =
        stats.mean_scored_reward ??
        (stats.scored === stats.selected ? stats.mean_reward : null);
      const label = span("phase-mean", fixed(value));
      label.title =
        "该阶段已交 " +
        nfmt(stats.scored) +
        " / " +
        nfmt(stats.selected) +
        " 题";
      return label;
    };
    const coverage = span(
      "coverage-value",
      nfmt(e.scored) + " / " + nfmt(e.selected),
    );
    coverage.title =
      "已交 " + nfmt(e.scored) + " 题，已启动 " + nfmt(e.attempted) + " 题";
    const ranking = span(e.rank ? "rank-position" : "unplayed", e.rank ?? "—");
    if (!e.rank)
      ranking.title = e.scored !== e.selected ? "未交齐题单" : "不列入受控排名";
    const model = link(humanModel(e.model), runPath(e.run_id), "model-name");
    model.title = e.model;
    return [
      ranking,
      model,
      harnessName(e.harness),
      ...(showScope
        ? [
            [
              display(e.backend),
              display(e.track),
              e.protocol !== "suite-v1" && e.protocol?.slice(0, 8),
            ]
              .filter(Boolean)
              .join(" · "),
          ]
        : []),
      coverage,
      score("lobby"),
      score("draft-lock"),
      span(
        "overall-score",
        fixed(e.scored === e.selected ? e.mean_reward : null),
      ),
    ];
  });
  const wrap = table(headers, rows, "当前题单的模型与 CLI 综合排名");
  wrap.classList.add("overall-ranking");
  const body = wrap.querySelector("tbody");
  const missing = entries.findIndex((e) => !e.rank);
  if (missing !== -1) {
    const divider = node("td", "", "未排名");
    divider.colSpan = headers.length;
    body.insertBefore(
      node("tr", "ranking-divider", divider),
      body.rows[missing],
    );
  }
  return wrap;
}
async function leaderboard(root, signal) {
  const board = await json("/api/leaderboard", signal),
    featured = board.featured;
  const desk = div(
    "scoring-desk",
    div(
      "desk-head",
      div(
        "",
        span("desk-context", featured?.display_title || ""),
        node("h1", "", "模型与 Harness 综合排名"),
      ),
    ),
  );
  root.replaceChildren(node("section", "event-spread", seasonVisual(), desk));
  if (!featured?.games?.length) {
    desk.append(empty("暂无有效题单。"));
    return;
  }
  const entries = [...(featured.entries || [])].sort(
    (a, b) =>
      (a.rank ?? Infinity) - (b.rank ?? Infinity) ||
      b.scored - a.scored ||
      String(a.model).localeCompare(String(b.model)) ||
      String(a.harness).localeCompare(String(b.harness)),
  );
  const tasks = featured.games.reduce(
    (n, g) => n + Object.keys(g.tasks || {}).length,
    0,
  );
  const totals = span(
    "desk-scope",
    nfmt(featured.games.length) + " 场 · " + nfmt(tasks) + " 题",
  );
  desk.append(totals);
  if (!entries.length) {
    desk.append(empty("该题单尚无真实模型运行。"));
    return;
  }
  desk.append(
    rankingTable(entries),
    span("score-rule", "BP 前后分别取已交题的平均分。综合排名要求交齐十题。"),
  );
  const results = await Promise.allSettled(
    entries.map((e) => json(baseApi(e.run_id), signal)),
  );
  if (signal.aborted) return;
  const combos = entries.map((e, i) => {
    const result = results[i],
      report = result.status === "fulfilled" ? result.value.report : null;
    const games = asGames(report || { trials: [] }, featured.games);
    return {
      ...e,
      id: e.run_id,
      games: new Map(games.map((g) => [gameKey(g), g])),
      failedLoad: !report,
    };
  });
  const panel = div("fixture-deck"),
    holder = div("");
  let selectedModel = "",
    selectedCLI = "";
  const choices = (key, format) => [
    ["", "全部"],
    ...[...new Set(entries.map((e) => e[key]))].map((v) => [v, format(v)]),
  ];
  const filters = div(
    "game-filters",
    choice("模型", choices("model", humanModel), "", (v) => {
      selectedModel = v;
      render();
    }),
    choice("Harness", choices("harness", harnessName), "", (v) => {
      selectedCLI = v;
      render();
    }),
  );
  panel.append(fixtureHead("", filters), holder);
  root.append(panel);
  function render() {
    const shown = combos.filter(
      (c) =>
        (!selectedModel || c.model === selectedModel) &&
        (!selectedCLI || c.harness === selectedCLI),
    );
    holder.replaceChildren(resultsGrid(featured.games, shown, true));
  }
  render();
}
async function listRuns(root, signal, technical = false, model = null) {
  const { runs: source = [] } = await json(
    "/api/runs" + (technical ? "?view=diagnostics" : ""),
    signal,
  );
  const runs = (technical ? source : source.filter(isForecast)).filter(
    (r) => !model || r.model === model,
  );
  root.replaceChildren(
    pageHeading(
      humanModel(model) || (technical ? "技术记录" : "预测运行"),
      nfmt(runs.length) +
        " 次运行 · " +
        new Set(runs.map((r) => r.harness)).size +
        " 种 CLI",
      model
        ? link("全部预测运行 →", "#/runs", "sub-link")
        : technical
          ? link("返回预测运行", "#/runs", "sub-link")
          : link("技术记录 →", "#/diagnostics", "sub-link"),
    ),
  );
  let query = "",
    filter = "",
    page = 0;
  const holder = div("");
  function render() {
    const filtered = runs.filter(
      (r) =>
        (!filter || r.harness === filter) &&
        [r.model, r.harness, r.name, r.edition, r.display_title, r.id]
          .join(" ")
          .toLowerCase()
          .includes(query),
    );
    const pages = Math.max(1, Math.ceil(filtered.length / 30));
    page = Math.min(page, pages - 1);
    const rows = filtered
      .slice(page * 30, (page + 1) * 30)
      .map((r) => [
        link(modelName(r), runPath(r.id), "primary"),
        harnessName(r.harness),
        div(
          "",
          r.short_title || r.release,
          span("secondary", r.edition || display(r.mode)),
        ),
        span("number", nfmt(r.scored) + " / " + nfmt(r.selected)),
        span("number score-num", fixed(r.mean_reward)),
        display(r.status),
        span("secondary nowrap", dateText(r.created_at)),
      ]);
    holder.replaceChildren(
      rows.length
        ? table(
            [
              ["模型 / 运行"],
              ["CLI"],
              ["题集"],
              ["交卷", "right"],
              ["均分", "right"],
              ["状态"],
              ["记录时间"],
            ],
            rows,
            "运行记录",
          )
        : empty("没有匹配的运行。"),
      pager(filtered.length, page, pages, (v) => {
        page = v;
        render();
      }),
    );
  }
  const input = node("input", "");
  input.type = "search";
  input.placeholder = "搜索模型或运行名称";
  input.setAttribute("aria-label", "搜索模型或运行名称");
  input.addEventListener("input", () => {
    query = input.value.trim().toLowerCase();
    page = 0;
    render();
  });
  const cliOpts = [
    ["", "全部"],
    ...[...new Set(runs.map((r) => r.harness).filter(Boolean))]
      .sort()
      .map((h) => [h, harnessName(h)]),
  ];
  root.append(
    div(
      "compact-table",
      div(
        "board-toolbar",
        input,
        choice("CLI", cliOpts, "", (v) => {
          filter = v;
          page = 0;
          render();
        }),
      ),
      holder,
    ),
  );
  render();
}
function pager(total, page, pages, go) {
  const prev = action("上一页", () => go(page - 1)),
    next = action("下一页", () => go(page + 1));
  prev.disabled = page === 0;
  next.disabled = page + 1 >= pages;
  return div(
    "panel-foot",
    span(
      "meta",
      "共 " +
        nfmt(total) +
        " 条" +
        (pages > 1 ? " · 第 " + (page + 1) + " / " + pages + " 页" : ""),
    ),
    pages > 1 && div("button-row", prev, next),
  );
}
async function rules(root, signal) {
  const { featured } = await json("/api/leaderboard", signal);
  const games = featured?.game_count || 0;
  root.replaceChildren(
    pageHeading("评测规则", games ? games + " 场比赛 · 每场两次独立预测" : ""),
    div("grid",
      box("预测窗口", table(
        [["时点"], ["模型可见的证据"]],
        [
          ["BP 前", "版本、赛制、选边、首发和当时可查的历史。"],
          ["BP 后", "上述证据与本局完整的禁选顺序。"],
        ],
        "模型在两个预测窗口可见的证据",
      )),
      box("得分与名次", div("panel-body rule-body",
        node("p", "", "每次提交两项概率：蓝方获胜、蓝方在 15 分钟经济领先。赛后按真实结果计算 Brier 误差，两项等权。单题得分为 1 减去平均误差。"),
        node("p", "", "同一题单、受控后端与评测协议内，交齐全部题目后按平均得分排名，同分并列。同一组合有多轮完整记录时显示最近一轮。"),
        node("p", "", "部分完成的组合显示交卷数，阶段均分只统计已交题。"),
      )),
    ),
  );
}
async function runDetail(root, id, signal) {
  const { run: r, report } = await json(baseApi(id), signal);
  if (!r) throw Error("找不到运行记录");
  const tech = !isForecast(r),
    boundary = r.mode === "boundary",
    trials = report.trials || [];
  const meta = [
    r.model && humanModel(r.model) !== r.model && r.model,
    harnessName(r.harness),
    r.display_title || r.short_title || r.release,
    r.edition,
    display(r.backend),
    r.billing_source,
    dateText(r.created_at),
  ].filter(Boolean);
  root.replaceChildren(
    crumb(
      link(tech ? "技术记录" : "预测运行", tech ? "#/diagnostics" : "#/runs"),
      r.name || id,
    ),
    pageHeading(modelName(r), meta.join(" · ")),
  );
  if (boundary) {
    root.append(
      box(
        "逐题验收",
        table(
          [["题目"], ["CLI"], ["阶段"], ["验收范围"], ["结果"]],
          trials.map((t) => [
            link(t.task, taskPath(id, trialKey(t))),
            harnessName(t.harness),
            display(phase(t)),
            t.scope,
            display(t.status),
          ]),
          "逐题验收",
        ),
      ),
    );
    return;
  }
  const games = asGames(report),
    summary = report.summary || {};
  root.append(
    div(
      "run-facts",
      field("平均得分", fixed(r.mean_reward)),
      field("成功交卷", nfmt(r.scored) + " / " + nfmt(r.selected)),
      field("胜负 Brier", fixed(summary.brier_on_scored?.p_blue_win)),
      field("15′ 领先 Brier", fixed(summary.brier_on_scored?.p_blue_ahead_15)),
    ),
  );
  let page = 0;
  const holder = div("");
  function draw() {
    const pages = Math.max(1, Math.ceil(games.length / 20));
    holder.replaceChildren(
      matchTable(games.slice(page * 20, (page + 1) * 20), id),
      pager(games.length, page, pages, (v) => {
        page = v;
        draw();
      }),
    );
  }
  root.append(holder);
  draw();
  if (games.length && games.every((g) => isQuarterfinal(g.series)))
    root.append(quarterfinalWalkout());
}
function displayText(x) {
  return typeof x === "string" ? x : (JSON.stringify(x, null, 2) ?? "");
}
function coverageCard(c) {
  if (!c || !Array.isArray(c.starters))
    return empty("此报告没有逐位选手的覆盖数据。");
  return div(
    "",
    div(
      "panel-body details-row",
      field("可见历史小局", nfmt(c.history_games)),
      field(
        "有历史的首发",
        nfmt(c.starters.filter((p) => p.games > 0).length) +
          " / " +
          nfmt(c.starters.length),
      ),
    ),
    table(
      [["首发"], ["方位"], ["历史出场", "right"], ["同版本", "right"]],
      c.starters.map((p) => [
        span("strong", p.name),
        p.side === "blue" ? "蓝方" : "红方",
        span("number", nfmt(p.games)),
        span("number", nfmt(p.same_patch_games)),
      ]),
      "选手历史覆盖",
    ),
  );
}
async function trialDetail(root, id, key, signal) {
  const {
    run,
    trial: t,
    artifacts = {},
  } = await json(baseApi(id) + "/trials/" + enc(key), signal);
  const files = {};
  for (const [name, path] of Object.entries(artifacts)) {
    const url = apiFile(path);
    if (url) files[name] = url;
  }
  const ph = display(phase(t)),
    game = t.task?.match(/-g(\d+)-(?:draft-lock|lobby)$/)?.[1],
    match = t.match || {};
  const title =
    match.blue && match.red
      ? match.blue + " vs " + match.red
      : t.scope
        ? (t.harness || "") + " · 隔离验收"
        : "单局预测";
  const boundary = Boolean(t.scope);
  const tr = t.trajectory || {},
    p = t.prediction || {};
  root.replaceChildren(
    crumb(
      link("运行记录", "#/runs"),
      link("运行详情", runPath(id)),
      "逐题记录",
    ),
    heading(
      title,
      [
        humanModel(run.model),
        harnessName(t.harness || run.harness),
        run.billing_source,
      ]
        .filter(Boolean)
        .join(" · "),
      [
        ...(boundary
          ? [["状态", display(t.status)]]
          : [
              ["蓝方胜率", pct(p.p_blue_win)],
              ["15′ 蓝方领先", pct(p.p_blue_ahead_15)],
              ["reward", fixed(t.reward)],
            ]),
      ],
      [game && "GAME " + game, ph, t.patch && "PATCH " + t.patch]
        .filter(Boolean)
        .join(" / "),
    ),
  );
  if (!boundary && t.draft)
    root.append(window.LoLDraft.render(t.draft, t.match));
  const details = div(
    "panel-body details-row",
    field("状态", display(t.status)),
    field("时点", ph),
    field("Harness", t.runtime?.cli || t.harness),
    field("版本", t.patch || t.runtime?.version),
    boundary && field("验收范围", t.scope),
  );
  if (
    !boundary &&
    isQuarterfinal(
      match.series || t.task?.replace(/-g\d+-(lobby|draft-lock)$/, ""),
    )
  ) {
    const hero = root.querySelector(".hero");
    hero.classList.add("quarterfinal-hero");
    hero.append(quarterfinalWalkout());
  }
  if (t.error) details.append(field("运行错误", displayText(t.error)));
  if (!boundary) {
    const y = t.observed_outcome || {};
    details.append(
      field(
        "实际胜方",
        y.p_blue_win === 1 ? "蓝方" : y.p_blue_win === 0 ? "红方" : "—",
      ),
      field(
        "15′ 蓝方领先",
        y.p_blue_ahead_15 === 1 ? "是" : y.p_blue_ahead_15 === 0 ? "否" : "—",
      ),
      field("Brier · 胜负", fixed(t.brier?.p_blue_win)),
      field("Brier · 15′", fixed(t.brier?.p_blue_ahead_15)),
    );
  }
  const left = div(
    "stack",
    box(boundary ? "验收信息" : "预测与赛后结果", details),
  );
  if (boundary && t.observation)
    left.append(
      box(
        "隔离环境观察",
        div("panel-body", node("pre", "code", displayText(t.observation))),
      ),
    );
  if (t.differences && Object.keys(t.differences).length)
    left.append(
      box(
        "验收差异",
        div("panel-body", node("pre", "code", displayText(t.differences))),
      ),
    );
  root.append(
    box(
      "模型上下文",
      trialTimeline(
        t,
        files,
        baseApi(id) + "/trials/" + enc(key) + "/timeline",
        signal,
      ),
    ),
  );
  const right = div("stack");
  if (!boundary)
    right.append(
      box(
        "选手历史覆盖",
        coverageCard(t.coverage),
        files.snapshot ? link("冻结快照", files.snapshot) : null,
      ),
    );
  const usage = tr.token_usage || {};
  if (Object.keys(usage).length)
    right.append(
      box(
        "CLI 用量",
        div(
          "panel-body details-row",
          Object.entries(usage).map(([k, v]) => field(k, nfmt(v))),
        ),
      ),
    );
  const supporting = node(
    "details",
    "tx-support",
    node("summary", "", "评分与证据覆盖"),
    div("workspace", left, right),
  );
  root.append(supporting);
}
async function route() {
  active?.abort();
  active = new AbortController();
  const { signal } = active;
  let parts;
  try {
    parts = location.hash
      .split("?", 1)[0]
      .replace(/^#\/?/, "")
      .split("/")
      .filter(Boolean)
      .map(decodeURIComponent);
  } catch {
    parts = ["invalid"];
  }
  const tab = parts[0] || "leaderboard",
    root = div("page");
  main.replaceChildren(root);
  for (const a of document.querySelectorAll("[data-nav]")) {
    if (
      a.dataset.nav ===
      (tab === "models" || tab === "diagnostics" ? "runs" : tab)
    )
      a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  }
  const titles = {
    leaderboard: "模型成绩",
    runs: "预测运行",
    rules: "评测规则",
    diagnostics: "技术记录",
  };
  document.title =
    (parts.length > 2
      ? "逐题记录"
      : parts.length > 1
        ? "运行详情"
        : titles[tab] || "页面") + " · LoL Competition Bench";
  const loading = empty("正在读取本地评测数据…");
  loading.setAttribute("role", "status");
  root.append(loading);
  try {
    if (tab === "leaderboard" && parts.length <= 1)
      await leaderboard(root, signal);
    else if (tab === "runs" && parts.length === 1) await listRuns(root, signal);
    else if (tab === "diagnostics" && parts.length === 1)
      await listRuns(root, signal, true);
    else if (tab === "models" && parts.length === 2)
      await listRuns(root, signal, false, parts[1]);
    else if (tab === "runs" && parts.length === 2)
      await runDetail(root, parts[1], signal);
    else if (tab === "runs" && parts.length === 4 && parts[2] === "trials")
      await trialDetail(root, parts[1], parts[3], signal);
    else if (tab === "rules" && parts.length === 1) await rules(root, signal);
    else throw Error("页面路径无效。");
  } catch (e) {
    if (!signal.aborted)
      root.replaceChildren(
        box(
          "无法显示页面",
          div(
            "panel-body",
            node("p", "", e.message),
            div(
              "button-row section",
              action("重新读取", route),
              link("返回排行榜", "#/leaderboard", "btn"),
            ),
          ),
        ),
      );
  }
}
window.addEventListener("hashchange", () => {
  window.scrollTo(0, 0);
  main.focus({ preventScroll: true });
  route();
});
document.querySelector(".skip").addEventListener("click", (event) => {
  event.preventDefault();
  main.focus();
});
route();
