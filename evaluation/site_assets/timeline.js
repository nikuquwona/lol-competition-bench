"use strict";

function timelineStep(s, index) {
  const row = node("details", "tl-step" + (s.failed || s.kind === "diagnostic" ? " tl-alert" : ""));
  const category = s.kind === "tool" ? "工具" : s.kind === "message" ? "模型" : s.kind === "diagnostic" ? "诊断" : "事件";
  const end = Number.isInteger(s.exit_code) ? "退出 " + s.exit_code : s.unfinished ? "未完成" : "";
  const small = s.prediction ? "蓝方胜率 " + pct(s.prediction.p_blue_win) + " · 15′ 领先 " + pct(s.prediction.p_blue_ahead_15) : s.preview;
  row.append(node("summary", "",
    span("tl-index", String(index + 1).padStart(2,"0")),
    div("tl-heading", div("tl-top", span("tl-type", category), end && span("tl-state", end), s.repeat > 1 && span("tl-state", "连续 " + s.repeat + " 次")),
      node("strong", "", s.title),
      s.kind === "tool" && s.command && node("code", "tl-invocation", s.command.split("\n",1)[0].slice(0,115)),
      small && node("p", "tl-preview", small))));
  const content = div("tl-content");
  function add(title, value, chars) {
    content.append(node("h4", "", title), node("pre", "tl-code", value || "（无文本输出）"));
    if (chars > (value || "").length) content.append(node("p", "meta", "本段原长 " + nfmt(chars) + " 字符，完整内容见原生事件文件。"));
  }
  if (s.kind === "tool") {
    add("工具输入", s.command, s.command_chars);
    if (s.has_result) add("工具返回", s.output, s.output_chars);
    else content.append(empty("未找到可与此次调用配对的工具返回。"));
  } else add(s.title, s.body, s.body_chars);
  row.append(content);
  return row;
}

function trialTimeline(trial, files, url, signal) {
  const area = div("tl-wrap", empty("正在读取原生轨迹…"));
  async function load() {
    try {
      const data = await json(url, signal);
      if (signal.aborted) return;
      const steps = data.steps || [], counts = data.metrics || {}, tags = data.evidence || [];
      const head = div("tl-summary");
      const match = trial.match || {};
      const info = [display(phase(trial)), match.blue && match.red ? match.blue + " / " + match.red : null,
        trial.coverage ? nfmt(trial.coverage.history_games) + " 局可查历史" : null,
        phase(trial) === "draft-lock" ? "20 手 BP 已锁定" : phase(trial) === "lobby" ? "本局 BP 未公开" : null].filter(Boolean);
      if (info.length) head.append(span("tl-label", "观测范围"), node("p", "", info.join(" · ")));
      if (tags.length) head.append(span("tl-label", "成功查询涉及的快照字段"), div("tl-tags", tags.map(v => span("", v))));
      const readings = data.readbacks || [];
      if (readings.length) head.append(span("tl-label", "预测文件相关命令的数值回显"),
        div("tl-readbacks", readings.map((p,i) => span("", (i ? "→ " : "") +
          pct(p.p_blue_win) + " / " + pct(p.p_blue_ahead_15)))),
        node("small","meta","依次为蓝方胜率与 15′ 领先概率。最终交卷以保存的预测文件为准。"));
      area.replaceChildren(head);
      if (data.availability === "truncated") area.append(empty("原始日志或时间线读取范围已截断。可用事件仍按记录顺序展示。"));
      if (!steps.length) {
        area.append(empty(trial.status === "scored" ? "此记录没有可展示的原生执行步骤。评分和已保存文件仍可查看。" : "此次运行未留下可展示的原生执行步骤。"));
      } else {
        const bar = div("tl-bar"), body = div("tl-body");
        const filters = [["all","全部"],["tool","工具"],["message","模型消息"],["prediction","预测回显"],["error","异常"]];
        let selected = "all", limit = 12;
        const filterButtons = new Map();
        function draw() {
          for (const [key, button] of filterButtons) button.setAttribute("aria-pressed", String(selected === key));
          const chosen = steps.map((s,i) => ({s,i})).filter(({s})=>selected==="all" || s.kind===selected || (selected==="prediction" && s.prediction) || (selected==="error" && (s.failed || s.kind==="diagnostic")));
          body.replaceChildren(...chosen.slice(0,limit).map(({s,i})=>timelineStep(s,i)));
          if (chosen.length===0) body.append(empty("这一类没有记录。"));
          if (chosen.length>limit) body.append(action("显示余下 " + (chosen.length-limit) + " 步", ()=>{limit+=24;draw();}));
        }
        for (const [key,name] of filters) {
          const button=action(name,()=>{selected=key;limit=12;draw();});
          filterButtons.set(key,button);bar.append(button);
        }
        const total = [counts.shell_commands ? counts.shell_commands + " 条命令" : null,
          counts.failed_commands ? counts.failed_commands + " 条命令失败" : null].filter(Boolean).join(" · ");
        if (total) bar.append(span("tl-count", total));
        area.append(bar,body); draw();
      }
      if (data.omitted) area.append(empty("详细记录另含 " + nfmt(data.omitted) + " 步。"));
      const downloads = div("tl-downloads");
      if (files.events) downloads.append(link("下载原生事件", files.events, "", true));
      if (files.transcript) downloads.append(link("下载完整文字轨迹", files.transcript, "", true));
      if (downloads.childElementCount) area.append(downloads);
    } catch (err) {
      if (!signal.aborted) area.replaceChildren(empty(err.message), action("重试",load));
    }
  }
  load();
  return area;
}
