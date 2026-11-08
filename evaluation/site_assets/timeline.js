"use strict";

function trialTimeline(trial, files, url, signal) {
  const root = div("trace-explorer", empty("正在读取执行记录…"));
  const pairs = (p) => pct(p.p_blue_win) + " / " + pct(p.p_blue_ahead_15);
  function button(label, cls, click) {
    const b = node("button", cls, label);
    b.type = "button";
    b.addEventListener("click", click);
    return b;
  }
  function build(data) {
    const steps = data.steps || [];
    const marks = new Map(
      (data.checkpoints || []).map((m, i) => [m.step_id, { ...m, index: i }]),
    );
    function stepName(s) {
      const m = marks.get(s.id);
      if (m)
        return (
          (m.index
            ? "更新预测"
            : ["write_tool", "reported_write"].includes(m.source)
              ? "首次写入预测"
              : "读回预测值") +
          " · " +
          pairs(m.values)
        );
      if (s.kind === "message")
        return (s.preview || "模型消息").split(/\r?\n/)[0].slice(0, 75);
      return s.title;
    }
    const kindName = (s) =>
      s.source?.tool ||
      {
        message: "模型消息",
        diagnostic: "诊断",
        tool: "工具",
        event: "原生事件",
      }[s.kind] ||
      "事件";
    const defaultStep =
      steps.findLast((s) => marks.has(s.id)) ||
      steps.find((s) => s.failed) ||
      steps.find((s) => s.kind === "tool") ||
      steps[0];
    const hashPath = location.hash.split("?", 1)[0];
    const line = Number(
      new URLSearchParams(location.hash.split("?")[1]).get("line"),
    );
    const linkedStep = line > 0 && steps.find((s) => s.source?.line === line);
    let current = (linkedStep || defaultStep)?.id;
    let filter = "all";
    let view = "io";
    const strip = div("tx-forecast"),
      nav = node("nav", "tx-nav"),
      inspector = node("section", "tx-inspector");
    nav.setAttribute("aria-label", "执行步骤");
    inspector.setAttribute("aria-label", "选中事件详情");
    const stripButtons = new Map();
    const readings = div("tx-points");
    for (const [id, m] of marks) {
      const tag = m.index
        ? "修订 " + m.index
        : ["write_tool", "reported_write"].includes(m.source)
          ? "首次写入"
          : "首次读回";
      const step = steps.find((s) => s.id === id);
      const b = button("", "tx-point", () => selectStep(id, true));
      b.append(
        span("tx-point-label", tag),
        node("strong", "", pairs(m.values)),
      );
      b.dataset.eventId = id;
      b.setAttribute(
        "aria-label",
        tag +
          " " +
          pairs(m.values) +
          "，查看原生事件第 " +
          (step?.source?.line || "—") +
          " 行",
      );
      stripButtons.set(id, b);
      readings.append(b);
    }
    const final = div(
      "tx-final",
      span("tx-point-label", "最终交卷"),
      node("strong", "", data.submission ? pairs(data.submission) : "未交卷"),
    );
    readings.append(final);
    strip.append(
      div(
        "tx-axis",
        node("h3", "", "预测记录"),
        span("", "蓝方胜率 / 15′ 领先"),
      ),
      readings,
    );
    if (!steps.length) {
      root.replaceChildren(
        strip,
        empty(
          data.availability === "truncated"
            ? "已保存的日志存在截断，读取范围内没有完整事件。"
            : "此题没有可展示的原生事件。",
        ),
      );
      if (trial.error) root.append(node("p", "tx-error", String(trial.error)));
      appendFiles();
      return;
    }
    const list = div("tx-list"),
      mobile = node("select", "tx-mobile-list");
    mobile.setAttribute("aria-label", "选择执行步骤");
    mobile.addEventListener("change", () => selectStep(mobile.value));
    const filterBox = node("select", "tx-filter");
    filterBox.setAttribute("aria-label", "筛选执行步骤");
    const filters = [
      ["all", "全部步骤"],
      ["evidence", "证据查询"],
      ["forecast", "预测记录"],
      ["error", "异常"],
      ["message", "模型消息"],
    ];
    for (const [v, title] of filters) {
      const option = node("option", "", title);
      option.value = v;
      filterBox.append(option);
    }
    const rows = new Map();
    const notes = (s) =>
      (data.review_notes || []).filter(
        (n) => s.kind === "message" && n.line === s.source?.line,
      );
    const disputed = (s) =>
      notes(s).some((n) => n.kind === "evidence_mismatch");
    const matches = (s) =>
      filter === "all" ||
      (filter === "evidence" && s.queries_snapshot) ||
      (filter === "forecast" && marks.has(s.id)) ||
      (filter === "error" &&
        (s.failed || s.kind === "diagnostic" || disputed(s))) ||
      s.kind === filter;
    filterBox.addEventListener("change", () => {
      filter = filterBox.value;
      const visible = steps.filter(matches);
      if (visible.length)
        selectStep(visible.find((s) => s.id === current)?.id || visible[0].id);
      else {
        current = null;
        view = "io";
        history.replaceState(null, "", hashPath);
        draw();
      }
    });
    nav.append(
      div("tx-navhead", node("h3", "", "执行步骤"), filterBox),
      mobile,
      list,
    );

    function selectStep(id, reveal = false) {
      const step = steps.find((s) => s.id === id);
      if (!step) return;
      if (step.source?.line)
        history.replaceState(null, "", hashPath + "?line=" + step.source.line);
      if (reveal || !matches(step)) filter = "all";
      current = id;
      view = "io";
      draw();
      revealRow(id);
    }
    function revealRow(id) {
      const active = rows.get(id);
      if (active && active.offsetTop >= 0 && list.clientHeight) {
        const y =
          list.scrollTop +
          active.getBoundingClientRect().top -
          list.getBoundingClientRect().top;
        if (
          y < list.scrollTop ||
          y + active.offsetHeight > list.scrollTop + list.clientHeight
        )
          list.scrollTop = Math.max(0, y - list.clientHeight / 3);
      }
    }
    function appendFiles() {
      const links = div("tx-files");
      if (files.events)
        links.append(link("原生事件 JSONL", files.events, "", true));
      if (files.transcript)
        links.append(link("文字轨迹 Markdown", files.transcript, "", true));
      if (links.childElementCount) root.append(links);
    }
    function detailBlock(label, value, length, reviews = []) {
      const full = value || "（无文本输出）";
      const field = div("tx-field", node("h5", "", label));
      const pre = node("pre", "tx-pre");
      let cursor = 0;
      for (const review of reviews) {
        if (!review.quote) continue;
        const at = full.indexOf(review.quote, cursor);
        if (at < 0) continue;
        pre.append(
          full.slice(cursor, at),
          node("mark", review.kind, review.quote),
        );
        cursor = at + review.quote.length;
      }
      pre.append(full.slice(cursor));
      field.append(pre);
      if (length > full.length)
        field.append(
          node(
            "small",
            "tx-hint",
            "展示节选，原始记录 " + nfmt(length) + " 字符。",
          ),
        );
      return field;
    }
    function reference(ref) {
      if (!ref?.line) return "未记录原生行号";
      return "JSONL L" + ref.line;
    }
    function inspection(s) {
      if (!s) {
        inspector.replaceChildren(empty("此筛选没有匹配的记录。"));
        return;
      }
      const first = s.source || {},
        second = s.result_source || {};
      const lines = [reference(first)];
      if (second.line && second.line !== first.line)
        lines.push("L" + second.line);
      const loc = lines.join(" → ");
      const status = s.failed ? "失败" : s.unfinished ? "未完成" : null;
      const io = button("输入与返回", "tx-tab", () => {
        view = "io";
        inspection(s);
      });
      const raw = button("原生记录", "tx-tab", () => {
        view = "raw";
        inspection(s);
      });
      io.setAttribute("aria-pressed", String(view === "io"));
      raw.setAttribute("aria-pressed", String(view === "raw"));
      inspector.dataset.selectedEvent = s.id;
      const meta = div(
        "tx-meta",
        span("", kindName(s)),
        s.turn && span("", "回合 " + s.turn),
        status && span("tx-status-error", status),
        Number.isInteger(s.exit_code) && span("", "退出码 " + s.exit_code),
        first.line
          ? link(loc, hashPath + "?line=" + first.line, "tx-location")
          : span("tx-location", loc),
      );
      inspector.replaceChildren(
        meta,
        node("h3", "tx-title", stepName(s)),
        div("tx-tabs", io, raw),
      );
      const body = div("tx-read");
      if (view === "raw") {
        for (const [title, ref] of [
          ["调用", first],
          ["返回", second],
        ]) {
          if (!ref?.line || (title === "返回" && ref.line === first.line))
            continue;
          const details = [
            ref.call_id && "call_id = " + ref.call_id,
            ref.item_id && "item_id = " + ref.item_id,
            ref.message_id && "message_id = " + ref.message_id,
          ].filter(Boolean);
          if (details.length)
            body.append(node("p", "tx-id", details.join(" · ")));
          body.append(
            detailBlock(title + " · " + reference(ref), ref.raw, ref.raw_chars),
          );
        }
      } else if (s.kind === "tool") {
        const mark = marks.get(s.id);
        if (mark) {
          const old = [...marks.values()][mark.index - 1];
          const values = div("tx-values");
          for (const [key, label] of [
            ["p_blue_win", "蓝方胜率"],
            ["p_blue_ahead_15", "15′ 蓝方领先"],
          ]) {
            values.append(
              div(
                "",
                span("", label),
                node(
                  "strong",
                  "",
                  old
                    ? pct(old.values[key]) + " → " + pct(mark.values[key])
                    : pct(mark.values[key]),
                ),
              ),
            );
          }
          body.append(values);
        }
        if (s.file) body.append(node("p", "tx-id", s.file));
        body.append(
          detailBlock(
            "输入",
            s.input_display || s.command,
            s.input_chars ?? s.command_chars,
          ),
        );
        if (s.has_result)
          body.append(detailBlock("返回", s.output, s.output_chars));
        else body.append(empty("没有与这次调用匹配的返回记录。"));
      } else
        body.append(
          detailBlock(
            s.kind === "message" ? "模型输出" : "记录",
            s.body,
            s.body_chars,
            notes(s),
          ),
        );
      for (const note of notes(s)) {
        const aside = node(
          "aside",
          "tx-review " +
            (note.kind === "evidence_mismatch" ? "mismatch" : "confirmed"),
        );
        aside.append(
          node(
            "strong",
            "",
            note.kind === "evidence_mismatch"
              ? "人工核查 · 与证据不符"
              : "人工核查 · 已核实",
          ),
          node("p", "", note.note),
          note.evidence && node("blockquote", "", note.evidence),
        );
        if (note.source) {
          const source = files.snapshot
            ? link(note.source + " ↗", files.snapshot)
            : node("code", "", note.source);
          if (files.snapshot) {
            source.target = "_blank";
            source.rel = "noopener";
            source.title = "查看这次预测使用的冻结快照";
          }
          aside.append(source);
        }
        body.append(aside);
      }
      inspector.append(body);
    }
    function draw() {
      const visible = steps.filter(matches);
      const savedScroll = list.scrollTop;
      rows.clear();
      list.replaceChildren();
      mobile.replaceChildren();
      filterBox.value = filter;
      for (const [id, b] of stripButtons)
        b.setAttribute("aria-current", id === current ? "step" : "false");
      for (const s of visible) {
        const idx = steps.indexOf(s);
        const b = button("", "tx-row", () => selectStep(s.id));
        b.setAttribute("aria-current", s.id === current ? "step" : "false");
        b.dataset.eventId = s.id;
        if (s.failed || s.kind === "diagnostic" || disputed(s))
          b.classList.add("tx-failure");
        if (marks.has(s.id)) b.classList.add("tx-revision");
        const index = String(idx + 1).padStart(2, "0");
        const category = disputed(s)
          ? "核查有异"
          : marks.has(s.id)
            ? "预测"
            : s.failed
              ? "失败"
              : [kindName(s), ...(s.fields || []).slice(0, 2)].join(" · ");
        b.append(
          span("tx-index", index),
          div(
            "tx-rowtext",
            span("tx-role", category),
            node("strong", "", stepName(s)),
          ),
        );
        const option = node("option", "", index + " · " + stepName(s));
        option.value = s.id;
        mobile.append(option);
        list.append(b);
        rows.set(s.id, b);
        b.addEventListener("keydown", (event) => {
          const at = visible.indexOf(s);
          const n =
            event.key === "ArrowDown"
              ? at + 1
              : event.key === "ArrowUp"
                ? at - 1
                : event.key === "Home"
                  ? 0
                  : event.key === "End"
                    ? visible.length - 1
                    : null;
          if (n !== null && visible[n]) {
            event.preventDefault();
            selectStep(visible[n].id);
            rows.get(visible[n].id)?.focus();
          }
        });
      }
      if (!visible.length) list.append(empty("没有匹配的步骤。"));
      mobile.value = current || "";
      list.scrollTop = savedScroll;
      inspection(visible.find((s) => s.id === current));
    }
    root.replaceChildren(strip);
    if (data.availability === "truncated" || data.omitted)
      root.append(
        node(
          "p",
          "tx-hint",
          "日志读取范围有限，完整保存的记录可从原生事件文件核对。",
        ),
      );
    root.append(div("tx-browser", nav, inspector));
    draw();
    revealRow(current);
    appendFiles();
    if (linkedStep) inspector.scrollIntoView({ block: "center" });
  }
  async function load() {
    try {
      const data = await json(url, signal);
      if (!signal.aborted) build(data);
    } catch (e) {
      if (!signal.aborted)
        root.replaceChildren(empty(e.message), action("重试", load));
    }
  }
  load();
  return root;
}
