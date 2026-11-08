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
const modelName = (r) =>
  r.model ||
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
          r.map((v, i) => node("td", headers[i]?.[1] || "", v)),
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
function smallRun(r) {
  const a = link("", runPath(r.id), "list-item");
  a.append(
    div("row", node("strong", "", r.harness || "运行"), badge(r.status)),
    span("secondary", modelName(r)),
    span("secondary", display(r.mode) + " · " + dateText(r.created_at)),
  );
  return a;
}
function groupLabel(g) {
  return [
    g.short_title || g.display_title || g.release,
    g.edition,
    display(g.scope),
    nfmt(g.selected) + " 题",
    display(g.track),
    display(g.backend),
    String(g.selection_sha256 || "").slice(0, 6),
    g.protocol && String(g.protocol).slice(0, 8),
    g.verification && display(g.verification),
  ]
    .filter(Boolean)
    .join(" · ");
}
async function leaderboard(root, signal) {
  const [board, index] = await Promise.all([
    json("/api/leaderboard", signal),
    json("/api/runs", signal),
  ]);
  const groups = [...(board.groups || [])].sort(
      (a, b) =>
        Number(Boolean(b.official)) - Number(Boolean(a.official)) ||
        Number(b.track === "controlled") - Number(a.track === "controlled") ||
        String(b.release).localeCompare(String(a.release), "en", {
          numeric: true,
        }) ||
        b.selected - a.selected ||
        b.entries.length - a.entries.length,
    ),
    runs = index.runs || [];
  root.replaceChildren(
    heading(
      "对局预测排行榜",
      "在相同题集与执行条件下，比较模型和 CLI 对胜负及 15 分钟经济领先的预测。",
      [
        ["比较组", nfmt(groups.length)],
        ["本地运行", nfmt(runs.length)],
      ],
    ),
  );
  const ranking = div(""),
    content = div("");
  const idx = 0;
  function draw(i) {
    const g = groups[i];
    if (!g) {
      content.replaceChildren(
        empty("暂无符合排名规则的运行。可在运行记录中查看已收录的报告。"),
      );
      return;
    }
    const rows = (g.entries || []).map((e) => {
      const meter = node("meter", "bar");
      meter.min = 0;
      meter.max = 1;
      meter.value = e.mean_reward || 0;
      meter.setAttribute("aria-label", "平均 reward");
      return [
        span("rank" + (e.rank === 1 ? " first" : ""), nfmt(e.rank)),
        div(
          "",
          link(e.harness, runPath(e.run_id), "primary"),
          span("secondary", e.model),
        ),
        div("number strong", fixed(e.mean_reward), meter),
        div(
          "number",
          pct(e.completion_rate),
          span("secondary", nfmt(e.scored) + " / " + nfmt(e.selected)),
        ),
        div(
          "number",
          fixed(e.brier_win),
          span("secondary number", fixed(e.brier_ahead15)),
        ),
        e.run_ids?.length > 1
          ? node(
              "details",
              "",
              node("summary", "number", nfmt(e.attempts)),
              e.run_ids.map((id, i) =>
                link("第 " + (i + 1) + " 轮", runPath(id), "secondary"),
              ),
            )
          : span("number", nfmt(e.attempts)),
      ];
    });
    content.replaceChildren(
      rows.length
        ? table(
            [
              ["排名"],
              ["Harness / 模型"],
              ["平均 reward", "right"],
              ["完成率", "right"],
              ["Brier 胜负 / 15′", "right"],
              ["轮次", "right"],
            ],
            rows,
            "比较组排名",
          )
        : empty("该比较组还没有排名记录。"),
      div(
        "panel-foot",
        div(
          "",
          span("primary", g.display_title || g.short_title || g.release),
          span(
            "secondary",
            [
              g.edition,
              "题号集合 " + String(g.selection_sha256 || "—").slice(0, 12),
            ]
              .filter(Boolean)
              .join(" · "),
          ),
        ),
        span(
          "badge",
          g.official
            ? "全量正式排名"
            : g.scope === "subset"
              ? "同题子集对照"
              : display(g.track),
        ),
      ),
    );
  }
  if (groups.length)
    ranking.append(
      div(
        "tools",
        choice(
          "比较组",
          groups.map((g, i) => [String(i), groupLabel(g)]),
          String(idx),
          (v) => draw(Number(v)),
          true,
        ),
      ),
    );
  ranking.append(content);
  draw(idx);
  const latest = box(
    "最近运行",
    runs.length
      ? div("", runs.slice(0, 4).map(smallRun))
      : empty("本机尚无运行记录。"),
    link("查看全部 →", "#/runs"),
  );
  const reading = box(
    "如何读榜",
    div(
      "panel-body rule-body",
      node("h3", "", "平均 reward"),
      node("p", "", "越高越好。失败和中断按零分计入。"),
      node("h3", "", "Brier 分数"),
      node("p", "", "胜负与 15 分钟领先分别评分，越低越好。仅统计成功交卷。"),
      node("p", "section", link("完整参赛规范 →", "#/rules")),
    ),
  );
  root.append(
    div(
      "grid",
      box(
        "模型与 Harness",
        ranking,
        link("导出榜单 CSV", "/api/leaderboard.csv", "btn", true),
      ),
      div("stack", latest, reading),
    ),
  );
}
async function listRuns(root, signal) {
  const { runs = [] } = await json("/api/runs", signal);
  const counts = new Set(runs.map((r) => r.release).filter(Boolean));
  root.replaceChildren(
    heading("运行记录", "查看本机收录的模型预测、基线和隔离验收。", [
      ["运行", nfmt(runs.length)],
      ["题集版本", nfmt(counts.size)],
    ]),
  );
  let mode = "",
    status = "",
    query = "",
    page = 0;
  const holder = div("");
  function render() {
    const rows = runs.filter(
      (r) =>
        (!mode || r.mode === mode) &&
        (!status || r.status === status) &&
        [
          r.harness,
          r.model,
          r.name,
          r.release,
          r.display_title,
          r.short_title,
          r.edition,
          r.id,
        ]
          .join(" ")
          .toLowerCase()
          .includes(query),
    );
    const total = rows.length,
      numPages = Math.max(1, Math.ceil(total / 30));
    page = Math.max(0, Math.min(page, numPages - 1));
    const body = rows
      .slice(page * 30, (page + 1) * 30)
      .map((r) => [
        div(
          "",
          link(modelName(r), runPath(r.id), "primary"),
          span("secondary", r.name || r.id),
        ),
        div(
          "",
          span("strong", r.harness),
          span("secondary", display(r.backend)),
        ),
        div("badges", badge(r.mode)),
        div(
          "",
          span("primary", r.short_title || r.display_title || r.release),
          r.edition && span("secondary", r.edition),
        ),
        badge(r.status),
        span("number", nfmt(r.scored) + " / " + nfmt(r.selected)),
        span("number", fixed(r.mean_reward)),
        span("nowrap", dateText(r.created_at)),
      ]);
    holder.replaceChildren(
      total
        ? table(
            [
              ["模型 / 运行"],
              ["Harness"],
              ["模式"],
              ["题集"],
              ["状态"],
              ["完成", "right"],
              ["reward", "right"],
              ["记录时间"],
            ],
            body,
            "本地运行",
          )
        : empty("没有匹配的运行。"),
      pager(total, page, numPages, (v) => {
        page = v;
        render();
      }),
    );
  }
  const search = node("input", "");
  search.type = "search";
  search.placeholder = "模型、Harness 或运行名称";
  search.addEventListener("input", () => {
    query = search.value.trim().toLowerCase();
    page = 0;
    render();
  });
  const opts = (key) => [
    ["", "全部"],
    ...Array.from(new Set(runs.map((r) => r[key]).filter(Boolean)))
      .sort()
      .map((v) => [v, display(v)]),
  ];
  const controls = div(
    "tools",
    node("label", "grow", "搜索", search),
    choice("模式", opts("mode"), "", (v) => {
      mode = v;
      page = 0;
      render();
    }),
    choice("状态", opts("status"), "", (v) => {
      status = v;
      page = 0;
      render();
    }),
  );
  root.append(box("全部运行", div("", controls, holder), null, "section"));
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
              "./bench simple\n./bench e2e --release datasets/replay-v3 --backend harbor \\\n  --harness codex --model deepseek-v4-pro",
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
  const trials = report.trials || [];
  if (!r) throw Error("找不到运行记录");
  const boundary = r.mode === "boundary";
  root.replaceChildren(
    crumb(link("运行记录", "#/runs"), r.name || id),
    heading(
      modelName(r),
      [
        r.harness,
        r.display_title || r.short_title || r.release,
        r.edition,
        display(r.backend),
        display(r.mode),
        dateText(r.created_at),
      ]
        .filter(Boolean)
        .join(" · "),
      [
        [
          boundary ? "验收通过" : "成功交卷",
          nfmt(r.scored) + " / " + nfmt(r.selected),
        ],
        ["完成率", pct(r.coverage)],
        ...(!boundary ? [["平均 reward", fixed(r.mean_reward)]] : []),
      ],
    ),
  );
  let phaseFilter = "",
    page = 0;
  const holder = div("");
  function draw() {
    const available = trials.filter(
        (t) => !phaseFilter || phase(t) === phaseFilter,
      ),
      pages = Math.max(1, Math.ceil(available.length / 30));
    page = Math.min(page, pages - 1);
    const rows = available.slice(page * 30, (page + 1) * 30).map((t) => {
      const match = t.match || {},
        title =
          match.blue && match.red ? match.blue + " vs " + match.red : null;
      const entry = div(
        "",
        link(title || t.task, taskPath(id, trialKey(t)), "primary"),
        title && span("secondary", t.task),
        t.scope && span("secondary", t.harness + " · " + t.scope),
      );
      return [
        entry,
        span("nowrap", display(phase(t))),
        badge(t.status),
        ...(!boundary
          ? [
              span("number", pct(t.prediction?.p_blue_win)),
              span("number", pct(t.prediction?.p_blue_ahead_15)),
              span("number", fixed(t.reward)),
            ]
          : []),
        link("查看详情 →", taskPath(id, trialKey(t)), "nowrap"),
      ];
    });
    const headers = [
      ["题目"],
      ["阶段"],
      ["状态"],
      ...(!boundary
        ? [
            ["蓝方胜率", "right"],
            ["15′ 领先", "right"],
            ["reward", "right"],
          ]
        : []),
      [""],
    ];
    holder.replaceChildren(
      rows.length
        ? table(headers, rows, "逐题结果")
        : empty("此运行还没有匹配的试题记录。"),
      pager(available.length, page, pages, (v) => {
        page = v;
        draw();
      }),
    );
  }
  const controls = div(
    "tools",
    choice(
      "观测时点",
      [
        ["", "全部"],
        ["lobby", "BP 前"],
        ["draft-lock", "BP 后"],
      ],
      "",
      (v) => {
        phaseFilter = v;
        page = 0;
        draw();
      },
    ),
    badge(r.status),
    span("meta", "发布 ID " + r.release),
  );
  const exports = div(
    "button-row",
    link("完整记录 ZIP", baseApi(id) + "/bundle.zip", "btn", true),
    link("报告 JSON", baseApi(id) + "/report.json", "btn", true),
    link("逐题 CSV", baseApi(id) + "/trials.csv", "btn", true),
  );
  root.append(
    box(
      boundary ? "隔离验收结果" : "逐题预测",
      div("", controls, holder),
      exports,
      "section",
    ),
  );
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
function eventSections(text, isTranscript) {
  if (!isTranscript)
    return text
      .split("\n")
      .filter((l) => l.trim())
      .map((l) => {
        try {
          const e = JSON.parse(l),
            i = e.item || {},
            name = i.type || e.toolName || e.type || e.role || "原生事件";
          return {
            title: String(name),
            body: i.command
              ? i.command + "\n\n" + (i.aggregated_output || "")
              : displayText(e),
          };
        } catch {
          return { title: "CLI 输出", body: l };
        }
      });
  // The generated transcript chooses fences longer than any run of backticks in its data.
  const blocks = [];
  let recording = false,
    current = null,
    fence = "";
  for (const line of text.split("\n")) {
    if (line === "## 执行轨迹" && !fence) {
      recording = true;
      continue;
    }
    if (!recording) continue;
    const delimiter = line.match(/^(\x60{3,})$/);
    if (delimiter && (!fence || delimiter[1] === fence)) {
      fence = fence ? "" : delimiter[1];
      continue;
    }
    const title = !fence && line.match(/^###\s+\d+\.\s+(.+)$/);
    if (title) {
      if (current) blocks.push(current);
      current = { title: title[1], lines: [] };
    } else if (current) current.lines.push(line);
  }
  if (current) blocks.push(current);
  return blocks.map((b) => ({
    title: b.title,
    body: b.lines.join("\n").trim(),
  }));
}
function browseTrace(files, signal) {
  const outer = div(""),
    available = files.transcript || files.events;
  if (!available) {
    outer.append(empty("此题没有已保存的逐步轨迹或原生事件。"));
    return outer;
  }
  const start = action("读取执行轨迹", load);
  outer.append(div("panel-body", start));
  async function load() {
    start.disabled = true;
    start.textContent = "正在读取…";
    try {
      const { text, truncated } = await preview(available, signal);
      const sections = eventSections(text, Boolean(files.transcript));
      const list = div(""),
        actions = div("panel-foot");
      let shown = 0,
        filter = "";
      function appendPage() {
        const selected = sections.filter(
          (e) => !filter || classify(e.title) === filter,
        );
        for (const [offset, section] of selected
          .slice(shown, shown + 40)
          .entries()) {
          const kind = classify(section.title),
            d = node("details", "event " + kind);
          const first = section.body.split("\n", 1)[0].trim().slice(0, 120);
          d.append(
            node(
              "summary",
              "",
              span("event-index", String(shown + offset + 1).padStart(2, "0")),
              span("event-icon", ""),
              div(
                "event-title",
                node("strong", "", section.title),
                first && node("small", "", first),
              ),
            ),
          );
          d.addEventListener("toggle", () => {
            if (d.open && !d.querySelector(".body"))
              d.append(
                div("body", node("pre", "code", section.body || "（无输出）")),
              );
          });
          list.append(d);
        }
        shown = Math.min(selected.length, shown + 40);
        actions.replaceChildren(
          span("meta", "已显示 " + shown + " / " + selected.length + " 个步骤"),
          shown < selected.length ? action("显示更多", appendPage) : nullNode(),
        );
        if (!shown) list.replaceChildren(empty("这份记录中没有匹配的步骤。"));
      }
      const filterControl = choice(
        "步骤",
        [
          ["", "全部"],
          ["tool", "命令与工具"],
          ["message", "模型消息"],
          ["warning", "诊断"],
        ],
        "",
        (v) => {
          filter = v;
          shown = 0;
          list.replaceChildren();
          appendPage();
        },
      );
      outer.replaceChildren(
        div("tools", filterControl, link("下载原文件", available, "btn", true)),
        list,
        actions,
      );
      if (truncated)
        outer.append(empty("预览已截到 2 MiB。可下载原文件查看全部内容。"));
      appendPage();
    } catch (e) {
      if (signal.aborted) return;
      outer.replaceChildren(
        empty(e.message),
        div("panel-body", action("重试", load)),
      );
    }
  }
  return outer;
}
const nullNode = () => document.createDocumentFragment();
function classify(s) {
  if (/退出码 [1-9]|诊断|错误|error|failed/i.test(s)) return "warning";
  if (/命令|工具|tool|exec|shell/i.test(s)) return "tool";
  if (/模型|message|assistant/i.test(s)) return "message";
  return "other";
}
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
  const { trial: t, artifacts = {} } = await json(
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
      t.task,
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
  left.append(box("执行轨迹", browseTrace(files, signal), count));
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
    if (a.dataset.nav === tab) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  }
  const titles = { leaderboard: "排行榜", runs: "运行记录", rules: "参赛规范" };
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
