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
const fileLabels = {
  prompt: "实际题面",
  snapshot: "冻结快照",
  transcript: "逐步轨迹",
  events: "原生事件",
  stderr: "错误输出",
  prediction: "交卷文件",
  boundary: "边界检查",
  runtime: "运行信息",
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
function modelLink(id, href) {
  const a = link(humanModel(id), href, "model-name");
  a.title = id;
  return a;
}
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
function link(text, href, cls, download = false) {
  const a = node("a", cls, text);
  a.href = href;
  if (download) a.download = "";
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
function groupLabel(g) {
  const single = g.games?.length === 1 ? g.games[0] : null;
  const scope = g.is_featured
    ? g.sampling
      ? "五场对照"
      : "五场 · 全题单均分"
    : g.scope === "full"
      ? "完整题集"
      : single?.blue && single?.red
        ? single.blue + " vs " + single.red + " G" + single.game
        : Number.isInteger(g.game_count)
          ? nfmt(g.game_count) + " 场"
          : "自选题单";
  return [
    scope,
    nfmt(g.selected) + " 题",
    g.edition || g.short_title || g.release,
    g.backend && display(g.backend),
    g.track === "vendor" ? "厂商通道" : null,
  ]
    .filter(Boolean)
    .join(" · ");
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
        }).filter(([, v]) => v != null),
      ),
    );
    g.pair[ph] = t;
  }
  return [...games.values()];
}
function actual(g) {
  const label =
    g.pair.lobby?.observed_outcome ||
    g.pair["draft-lock"]?.observed_outcome ||
    g.observed_outcome ||
    {};
  const winner =
    label.p_blue_win === 1
      ? g.blue || "蓝方"
      : label.p_blue_win === 0
        ? g.red || "红方"
        : null;
  const ahead =
    label.p_blue_ahead_15 === 1
      ? "蓝方领先"
      : label.p_blue_ahead_15 === 0
        ? "蓝方未领先"
        : "—";
  return div(
    "actual",
    span("strong", winner || "—"),
    span("secondary", "15′ " + ahead),
  );
}
function matchName(g) {
  if (!g.blue || !g.red)
    return div(
      "",
      span("strong", g.series || "比赛"),
      span("secondary", g.game ? "第 " + g.game + " 局" : "—"),
    );
  function team(side) {
    const row = span(side + "-team", g[side]),
      src = g[side + "_logo"];
    if (typeof src === "string" && /^\/teams\/[a-zA-Z0-9_-]+\.png$/.test(src)) {
      const img = node("img", "team-logo");
      img.alt = "";
      img.width = 22;
      img.height = 22;
      img.addEventListener(
        "error",
        () => {
          img.remove();
          row.classList.remove("with-logo");
        },
        { once: true },
      );
      row.classList.add("with-logo");
      row.prepend(img);
      img.src = src;
    }
    return row;
  }
  return div(
    "match-name",
    team("blue"),
    team("red"),
    span(
      "secondary",
      ["G" + g.game, g.stage, g.patch && "Patch " + g.patch]
        .filter(Boolean)
        .join(" · "),
    ),
  );
}
function phaseResult(runId, t) {
  if (!t) return span("unplayed", "未选此阶段");
  if (t.status === "unattempted") return span("unplayed", "未测");
  if (t.status !== "scored") {
    const lastResponse = t.runtime?.upstream?.at(-1)?.status;
    const limitReached =
      t.failure_kind === "rate_limit" ||
      lastResponse === 429 ||
      /(?:HTTP statuses?\s*\[[\d,\s]*\b429\s*\]|HTTP 429|rate.limit)/i.test(
        String(t.error || ""),
      );
    const title = ["started", "pending"].includes(t.status)
      ? "等待交卷"
      : limitReached
        ? "限流"
        : display(t.status);
    return t.status === "started" && !t.runtime
      ? span("unplayed", title)
      : link(title, taskPath(runId, trialKey(t)), "problem-link");
  }
  const a = link("", taskPath(runId, trialKey(t)), "forecast-link");
  a.append(
    span(
      "forecast-numbers",
      pct(t.prediction?.p_blue_win),
      " / ",
      pct(t.prediction?.p_blue_ahead_15),
    ),
    span("secondary", "得分 " + fixed(t.reward) + " ↗"),
  );
  a.setAttribute("aria-label", display(phase(t)) + " 预测及轨迹：" + t.task);
  return a;
}
function bpChange(pair) {
  const before = pair.lobby?.prediction?.p_blue_win,
    after = pair["draft-lock"]?.prediction?.p_blue_win;
  if (!Number.isFinite(before) || !Number.isFinite(after))
    return span("unplayed", "—");
  const diff = (after - before) * 100,
    label = (diff > 0 ? "+" : "") + diff.toFixed(1) + " pp";
  const chart = span(
    "pair-plot",
    span("pair-line"),
    span("before-dot"),
    span("after-dot"),
  );
  chart.style.setProperty("--before", 100 * before + "%");
  chart.style.setProperty("--after", 100 * after + "%");
  chart.style.setProperty("--left", 100 * Math.min(before, after) + "%");
  chart.style.setProperty("--width", Math.abs(diff) + "%");
  chart.setAttribute("aria-hidden", "true");
  const result = div("delta-cell", span("number", label), chart);
  result.title = "BP 使蓝方胜率从 " + pct(before) + " 变为 " + pct(after);
  return result;
}
function matchTable(games, runId) {
  if (!games.length) return empty("这轮运行尚无可展示的对局。");
  const box = table(
    [
      ["对局 · 蓝 / 红"],
      ["实际胜方"],
      ["BP 前 · 蓝胜率 / 15′ 领先"],
      ["BP 后 · 蓝胜率 / 15′ 领先"],
      ["胜率变化"],
    ],
    games.map((g) => [
      matchName(g),
      actual(g),
      phaseResult(runId, g.pair.lobby),
      phaseResult(runId, g.pair["draft-lock"]),
      bpChange(g.pair),
    ]),
    "逐场预测",
  );
  box.classList.add("matches-table");
  return box;
}
function reportExports(id) {
  return div(
    "button-row",
    link("完整记录 ZIP", baseApi(id) + "/bundle.zip", "btn", true),
    link("报告 JSON", baseApi(id) + "/report.json", "btn", true),
    link("逐题 CSV", baseApi(id) + "/trials.csv", "btn", true),
  );
}
function predictionGroups(board) {
  const verified = (board.groups || []).filter((g) =>
    ["controlled", "vendor"].includes(g.track),
  );
  const featured = board.featured;
  if (!featured?.games?.length) return verified;
  const byBackend = new Map();
  const bestFirst = [...(featured.entries || [])].sort(
    (a, b) =>
      Number(Boolean(b.is_suite)) - Number(Boolean(a.is_suite)) ||
      Number(Boolean(b.finished)) - Number(Boolean(a.finished)) ||
      b.scored - a.scored ||
      b.attempted - a.attempted,
  );
  for (const e of bestFirst) {
    const track = e.track || (e.harness === "cursor" ? "vendor" : "controlled"),
      protocol = e.protocol || "suite-v1",
      key = [e.backend, track, protocol].join("|");
    if (!byBackend.has(key))
      byBackend.set(key, { backend: e.backend, track, protocol, entries: [] });
    const list = byBackend.get(key).entries;
    if (!list.some((row) => row.model === e.model && row.harness === e.harness))
      list.push({ ...e });
  }
  if (!byBackend.size)
    byBackend.set("", { backend: null, track: "controlled", entries: [] });
  const pending = [...byBackend.values()].map((g) => ({
    ...featured,
    ...g,
    selected: featured.games.reduce(
      (n, game) => n + Object.keys(game.tasks || {}).length,
      0,
    ),
    is_featured: true,
    sampling: true,
    scope: "subset",
    selection_sha256: "featured-five",
  }));
  return [
    ...pending,
    ...verified.filter((g) => g.is_featured || g.scope === "full"),
  ];
}
async function leaderboard(root, signal) {
  const [board, index] = await Promise.all([
    json("/api/leaderboard", signal),
    json("/api/runs", signal),
  ]);
  const forecastRuns = (index.runs || []).filter(isForecast),
    runIndex = new Map(forecastRuns.map((r) => [r.id, r]));
  const groups = predictionGroups(board).sort(
    (a, b) =>
      Number(Boolean(b.is_featured)) - Number(Boolean(a.is_featured)) ||
      Number(Boolean(b.sampling)) - Number(Boolean(a.sampling)) ||
      Number(b.track === "controlled") - Number(a.track === "controlled") ||
      Number(b.scope === "full") - Number(a.scope === "full") ||
      String(b.release).localeCompare(String(a.release), "en", {
        numeric: true,
      }) ||
      b.selected - a.selected,
  );
  const harnesses = [
    ...new Set([
      ...(board.harnesses || Object.keys(harnessNames)),
      ...groups.flatMap((g) => g.entries.map((e) => e.harness)),
    ]),
  ];
  const download = link("导出题单 CSV", "/api/leaderboard.csv", "btn", true);
  const lead = pageHeading("模型预测成绩", null, download);
  root.replaceChildren(lead);
  if (!groups.length) {
    root.append(
      box(
        "模型 × CLI",
        empty("暂无已完成、可比较的模型评测。"),
        link("查看真实运行 →", "#/runs"),
      ),
    );
    return;
  }
  const matrix = div(""),
    matches = div("section"),
    filters = div("board-toolbar");
  root.append(filters, matrix, matches);
  const descriptors = groups.map(groupLabel);
  const selectedGroup = choice(
    "评测题单",
    groups.map((g, i) => [
      String(i),
      descriptors.filter((x) => x === descriptors[i]).length > 1
        ? descriptors[i] +
          " · " +
          g.selection_sha256.slice(0, 6) +
          " / " +
          String(g.protocol || "").slice(0, 8)
        : descriptors[i],
    ]),
    "0",
    (v) => draw(groups[Number(v)]),
    true,
  );
  const meta = span("board-meta", "");
  filters.append(selectedGroup, meta);
  let latest = 0;
  function draw(g) {
    const params = new URLSearchParams();
    if (g.sampling) params.set("view", "featured");
    else {
      params.set("selection_sha256", g.selection_sha256);
      params.set("archive_sha256", g.archive_sha256);
    }
    for (const name of ["backend", "track", "protocol"])
      if (g[name]) params.set(name, g[name]);
    download.href = "/api/leaderboard.csv?" + params.toString();
    const entries = g.entries || [],
      keys = new Map(entries.map((e) => [e.model + "\n" + e.harness, e]));
    const otherModels = (board.lineup || [])
      .map((e) => e.model)
      .filter(Boolean);
    const models = [
      ...new Set([...entries.map((e) => e.model), ...otherModels]),
    ];
    const buttons = new Map();
    const rows = models.map((m) => [
      modelLink(m, "#/models/" + enc(m)),
      ...harnesses.map((h) => {
        const e = keys.get(m + "\n" + h);
        if (!e) {
          const emptyCell = span("unplayed", "—");
          emptyCell.setAttribute("aria-label", "未测");
          return emptyCell;
        }
        const b = node(
          "button",
          "matrix-cell",
          span(
            "cell-score",
            g.sampling
              ? e.scored
                ? fixed(e.mean_scored_reward)
                : e.status === "unfinished"
                  ? "进行中"
                  : e.attempted
                    ? "未交卷"
                    : "待测"
              : fixed(e.mean_reward),
          ),
          span(
            !e.scored && e.status !== "unfinished"
              ? "cell-note failed-note"
              : "cell-note",
            g.sampling
              ? nfmt(e.scored) + " / " + nfmt(g.selected) + " 已交"
              : !e.scored
                ? "未交卷 · 0 / " + nfmt(e.selected)
                : "已交 " + nfmt(e.scored) + " / " + nfmt(e.selected),
          ),
        );
        b.type = "button";
        if (g.sampling)
          b.title =
            "计划 " +
            g.selected +
            " 题，实际启动 " +
            e.attempted +
            " 题，已交 " +
            e.scored +
            " 题";
        b.setAttribute(
          "aria-label",
          m +
            " × " +
            harnessName(h) +
            (g.sampling
              ? "，已交 " + nfmt(e.scored) + " 题"
              : "，平均分 " + fixed(e.mean_reward)) +
            "，查看对局",
        );
        b.addEventListener("click", () => activate(e));
        buttons.set(e, b);
        return b;
      }),
    ]);
    matrix.replaceChildren(
      box(
        "模型 × CLI",
        rows.length
          ? table(
              [["模型"], ...harnesses.map((h) => [harnessName(h)])],
              rows,
              "模型与 CLI 平均得分",
            )
          : empty("本题单还没有模型提交。"),
        span("meta", g.sampling ? "已交题均分 · — 未测" : "平均得分 · — 未测"),
        "matrix-panel",
      ),
    );
    meta.textContent = g.display_title || g.short_title || g.release;
    const first =
      entries.find((e) => e.finished && e.is_suite) ||
      entries.find((e) => e.scored > 0) ||
      entries[0];
    if (first) activate(first);
    else {
      latest++;
      matches.replaceChildren(
        g.games?.length
          ? box("对局", matchTable(asGames({ trials: [] }, g.games), ""))
          : document.createDocumentFragment(),
      );
    }
    function activate(e) {
      for (const [item, btn] of buttons)
        btn.setAttribute("aria-pressed", String(item === e));
      const ids = [...(e.run_ids?.length ? e.run_ids : [e.run_id])].sort(
        (a, b) =>
          String(runIndex.get(b)?.created_at || "").localeCompare(
            String(runIndex.get(a)?.created_at || ""),
          ),
      );
      const picker =
        ids.length > 1
          ? choice(
              "运行记录",
              ids.map((id, i) => [
                id,
                runIndex.get(id)?.created_at
                  ? dateText(runIndex.get(id).created_at)
                  : "运行 " + (i + 1),
              ]),
              ids[0],
              load,
            )
          : null;
      const outcomes = div(""),
        toRun = link("运行详情 →", runPath(ids[0]), "btn");
      const controls = div("button-row", picker, toRun);
      matches.replaceChildren(
        box(
          humanModel(e.model) + " × " + harnessName(e.harness),
          outcomes,
          controls,
        ),
      );
      load(ids[0]);
      async function load(id) {
        const generation = ++latest;
        toRun.href = runPath(id);
        outcomes.replaceChildren(empty("正在读取逐场预测…"));
        try {
          const { report } = await json(baseApi(id), signal);
          if (signal.aborted || generation !== latest) return;
          const games = asGames(report, g.games);
          outcomes.replaceChildren(matchTable(games, id));
        } catch (err) {
          if (!signal.aborted && generation === latest)
            outcomes.replaceChildren(empty(err.message));
        }
      }
    }
  }
  draw(groups[0]);
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
      model ? "该模型的真实预测运行" : null,
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
        div(
          "",
          link(modelName(r), runPath(r.id), "primary"),
          span("secondary", r.name || r.id),
        ),
        harnessName(r.harness),
        r.short_title || r.release,
        span("secondary", r.edition || display(r.mode)),
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
              ["版本"],
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
  const board = await json("/api/leaderboard", signal);
  root.replaceChildren(
    heading("参赛与计分规范", "本地排行榜采用的证据窗口、交卷格式和统计口径。"),
    div(
      "grid",
      div(
        "stack",
        box(
          "提交一轮评测",
          div(
            "panel-body rule-body",
            node(
              "p",
              "",
              "在仓库根目录启动评测。先用 simple 验证本地安装，再选定模型、CLI 和题集版本运行 e2e。全量运行结束后，可在本地排行榜按相同执行条件比较成绩。",
            ),
            node(
              "pre",
              "code files-preview",
              "./bench simple\n./bench e2e --release worlds-lpl-2026 --backend harbor \\\n  --harness codex --model deepseek-v4-pro",
            ),
          ),
        ),
        box(
          "排行榜计算规则",
          div(
            "panel-body rule-body",
            node(
              "ol",
              "",
              (board.rules || []).map((r) => node("li", "", r)),
            ),
          ),
        ),
        box(
          "模型可见证据",
          div(
            "panel-body rule-body",
            node(
              "p",
              "",
              "参赛 CLI 可以使用本局题面、冻结快照和其中的历史，借助本地 shell 或 Python 检索。禁止外部搜索、读取验证器真值、跨会话取数，以及引用本局或后续比赛的已知赛果。",
            ),
          ),
        ),
      ),
      div(
        "stack",
        box(
          "两个预测窗口",
          div(
            "panel-body rule-body",
            node("h3", "", "BP 前 · lobby"),
            node("p", "", "首发与选边已知，在第一手选禁公开时截止。"),
            node("h3", "", "BP 后 · draft-lock"),
            node("p", "", "完整选禁顺序已知，在实际开局时截止。"),
          ),
        ),
        box(
          "交卷格式",
          div(
            "panel-body rule-body",
            node(
              "p",
              "",
              "向 prediction.json 写入两个 0 至 1 的数值。示例格式如下。",
            ),
            node(
              "pre",
              "code files-preview",
              '{\n  "p_blue_win": 0.50,\n  "p_blue_ahead_15": 0.50\n}',
            ),
          ),
        ),
      ),
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
    pageHeading(modelName(r), meta.join(" · "), reportExports(id)),
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
}
const PREVIEW_LIMIT = 2 * 1024 * 1024;
async function preview(url, signal) {
  const response = await fetch(url, { signal });
  if (!response.ok) throw Error("读取文件失败（HTTP " + response.status + "）");
  const reader = response.body.getReader(),
    decoder = new TextDecoder();
  let text = "",
    size = 0,
    truncated = false;
  try {
    for (;;) {
      const { done, value } = await reader.read();
      if (done) break;
      const count = Math.min(PREVIEW_LIMIT - size, value.length);
      text += decoder.decode(value.subarray(0, count), { stream: true });
      size += count;
      if (count < value.length) {
        truncated = true;
        await reader.cancel();
        break;
      }
    }
    text += decoder.decode();
    return { text, truncated };
  } finally {
    reader.releaseLock();
  }
}
function displayText(x) {
  return typeof x === "string" ? x : (JSON.stringify(x, null, 2) ?? "");
}
const nullNode = () => document.createDocumentFragment();
function fileBrowser(files, signal) {
  const list = div("file-list"),
    view = div("files-preview");
  let token = 0;
  for (const [k, url] of Object.entries(files)) {
    const title = fileLabels[k] || k;
    async function open() {
      const id = ++token;
      view.replaceChildren(empty("正在读取" + title + "…"));
      try {
        let { text, truncated } = await preview(url, signal);
        if (k === "snapshot" || k === "prediction") {
          if (!truncated) {
            try {
              text = JSON.stringify(JSON.parse(text), null, 2);
            } catch {
              /* original text remains available */
            }
          }
        }
        if (id === token)
          view.replaceChildren(
            div(
              "tools",
              node("strong", "", title),
              action("收起", () => {
                ++token;
                view.replaceChildren();
              }),
            ),
            node("pre", "code", text || "（空文件）"),
            truncated ? span("meta", "仅预览前 2 MiB。") : nullNode(),
          );
      } catch (err) {
        if (!signal.aborted && id === token)
          view.replaceChildren(empty(err.message));
      }
    }
    list.append(div("file", action(title, open), link("下载", url, "", true)));
  }
  return div("panel-body", list, view);
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
  const { run, trial: t, artifacts = {} } = await json(
    baseApi(id) + "/trials/" + enc(key),
    signal,
  );
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
      [humanModel(run.model), harnessName(t.harness || run.harness), run.billing_source].filter(Boolean).join(" · "),
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
  const details = div(
    "panel-body details-row",
    field("状态", display(t.status)),
    field("时点", ph),
    field("Harness", t.runtime?.cli || t.harness),
    field("版本", t.patch || t.runtime?.version),
    boundary && field("验收范围", t.scope),
  );
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
  const count = Number.isFinite(tr.shell_commands)
    ? span("meta", tr.shell_commands + " 条终端命令")
    : null;
  left.prepend(
    box(
      "执行轨迹",
      trialTimeline(
        t,
        files,
        baseApi(id) + "/trials/" + enc(key) + "/timeline",
        signal,
      ),
      count,
    ),
  );
  const right = div(
    "stack",
    box(
      "原始文件",
      Object.keys(files).length
        ? fileBrowser(files, signal)
        : empty("这次运行未保存可下载的原始文件。"),
    ),
  );
  if (!boundary) right.append(box("选手历史覆盖", coverageCard(t.coverage)));
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
  root.append(div("workspace", left, right));
}
async function route() {
  active?.abort();
  active = new AbortController();
  const { signal } = active;
  let parts;
  try {
    parts = location.hash
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
