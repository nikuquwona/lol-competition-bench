"use strict";

// Wire captures and historical CLI transcripts have different evidence boundaries.
const ContextReader = (() => {
  let vendor;
  function trajectoryLibrary() {
    if (!vendor)
      vendor = new Promise((resolve, reject) => {
        const script = document.createElement("script");
        script.src = "/vendor/trajectory.js";
        script.onload = () =>
          window.Trajectory
            ? resolve(window.Trajectory)
            : reject(Error("轨迹解析器加载失败"));
        script.onerror = () => {
          vendor = null;
          reject(Error("无法加载本地轨迹解析器"));
        };
        document.head.append(script);
      });
    return vendor;
  }

  const stringify = (value) =>
    typeof value === "string" ? value : (JSON.stringify(value, null, 2) ?? "");
  const array = (value) =>
    Array.isArray(value) ? value : value == null ? [] : [value];
  function button(title, fn, cls = "mc-btn") {
    const b = node("button", cls, title);
    b.type = "button";
    b.addEventListener("click", fn);
    return b;
  }
  function fullText(value, force = false) {
    const text = stringify(value);
    const pre = () => node("pre", "mc-text", text || "（空）");
    if (force || (text.length <= 820 && text.split("\n", 12).length < 12))
      return pre();
    const outer = div("mc-long"),
      preview = node(
        "pre",
        "mc-text mc-excerpt",
        text.slice(0, 400).trimEnd() + "…",
      );
    let expanded = false;
    const toggle = button(
      "展开全文 · " + nfmt(text.length) + " 字符",
      () => {
        expanded = !expanded;
        outer.replaceChildren(expanded ? pre() : preview, toggle);
        toggle.textContent = expanded
          ? "收起全文"
          : "展开全文 · " + nfmt(text.length) + " 字符";
        toggle.setAttribute("aria-expanded", String(expanded));
      },
      "mc-inline",
    );
    toggle.setAttribute("aria-expanded", "false");
    outer.append(preview, toggle);
    return outer;
  }
  async function localText(href, signal) {
    if (!href) return null;
    const r = await fetch(href, { signal });
    if (!r.ok) throw Error("读取本地证据失败（HTTP " + r.status + "）");
    return r.text();
  }
  const roleName = {
    system: "System",
    developer: "Developer",
    user: "User",
    assistant: "Assistant",
    tool: "Tool",
    function: "Function",
  };
  function message(role, title, value, meta = "", force = false) {
    if (
      Array.isArray(value) &&
      value.every((b) => b?.type === "text" && typeof b.text === "string")
    )
      value = value.map((b) => b.text).join("\n");
    return node(
      "article",
      "mc-message mc-role-" + (roleName[role] ? role : "data"),
      div(
        "mc-mhead",
        span("mc-role", roleName[role] || role),
        span("mc-message-title", title || ""),
        meta && span("mc-ref", meta),
      ),
      fullText(value, force),
    );
  }
  function reference(note) {
    return node(
      "aside",
      "mc-review " +
        (note.kind === "evidence_mismatch" ? "mismatch" : "confirmed"),
      node(
        "strong",
        "",
        note.kind === "evidence_mismatch"
          ? "人工核查 · 与快照不符"
          : "人工核查 · 已核实",
      ),
      node("p", "", note.note),
      note.evidence && node("blockquote", "", note.evidence),
      note.source && node("code", "", note.source),
    );
  }

  // These adapters expose the actual wire roles and content types, including
  // content that cannot be represented as a simple user/assistant chat.
  function contentBlocks(role, content, meta = "") {
    return array(content).map((b) => {
      if (typeof b === "string") return message(role, "", b, meta);
      if (!b || typeof b !== "object") return message(role, "", b, meta);
      if (
        ["text", "input_text", "output_text"].includes(b.type) &&
        typeof b.text === "string"
      )
        return message(role, "", b.text, meta);
      if (b.type === "tool_use")
        return message("assistant", "调用 " + b.name, b.input, b.id || meta);
      if (b.type === "reasoning_text" && typeof b.text === "string")
        return message(role, "提供方记录的推理文本", b.text, meta);
      if (b.type === "tool_result")
        return message(
          "tool",
          b.is_error ? "调用失败" : "工具返回",
          b.content,
          b.tool_use_id || meta,
        );
      if (b.type === "thinking" || b.type === "reasoning")
        return message(
          role,
          "提供方记录的推理内容",
          b.thinking ?? b.summary ?? b,
          meta,
        );
      return message(role, b.type || "", b, meta);
    });
  }
  function wireMessages(input) {
    const rows = [];
    for (const m of array(input)) {
      if (!m || typeof m !== "object") {
        rows.push(message("user", "", m));
        continue;
      }
      if (m.type === "function_call" || m.type === "custom_tool_call") {
        rows.push(
          message(
            "assistant",
            "调用 " + (m.name || "工具"),
            m.arguments ?? m.input,
            m.call_id || m.id,
          ),
        );
        continue;
      }
      if (
        m.type === "function_call_output" ||
        m.type === "custom_tool_call_output"
      ) {
        rows.push(message("tool", "工具返回", m.output, m.call_id));
        continue;
      }
      const role = m.role || (m.type === "reasoning" ? "assistant" : "data");
      if (m.content != null)
        rows.push(...contentBlocks(role, m.content, m.tool_call_id || ""));
      for (const t of array(m.tool_calls))
        rows.push(
          message(
            "assistant",
            "调用 " + (t.function?.name || t.name || "工具"),
            t.function?.arguments ?? t,
            t.id,
          ),
        );
      if (m.reasoning_content)
        rows.push(message(role, "提供方记录的推理内容", m.reasoning_content));
      if (m.content == null && !m.tool_calls && !m.reasoning_content)
        rows.push(message(role, m.type || "", m));
    }
    return rows;
  }
  // Prefer terminal provider records. If a stream ends early, expose only the
  // chunks actually received; never manufacture a completed assistant turn.
  function responseParts(raw, createParser) {
    if (raw == null || raw === "") return [];
    let obj = raw;
    if (typeof raw === "string") {
      try {
        obj = JSON.parse(raw);
      } catch {
        obj = null;
      }
    }
    if (obj && typeof obj === "object") {
      if (obj.error) return [{ role: "provider", content: obj.error }];
      if (Array.isArray(obj.output)) return obj.output;
      if (Array.isArray(obj.choices))
        return obj.choices.map((c) => c.message ?? c);
      if (obj.content != null) return [obj];
      return [{ role: "provider", content: obj }];
    }
    const packets = [];
    const parser = createParser({
      onEvent({ data }) {
        if (!data || data === "[DONE]") return;
        try {
          const event = JSON.parse(data);
          if (event && typeof event === "object") packets.push(event);
        } catch {
          /* The raw tab preserves every byte captured, including incomplete JSON. */
        }
      },
    });
    parser.feed(String(raw));
    const terminal = packets.findLast(
      (e) =>
        e.type === "response.completed" && Array.isArray(e.response?.output),
    );
    if (terminal) return terminal.response.output;
    const items = new Map(),
      anthropic = new Map(),
      chat = new Map(),
      errors = [];
    for (const e of packets) {
      if (!e || typeof e !== "object") continue;
      if (e.error) errors.push({ role: "provider", content: e.error });
      if (
        e.type === "response.output_item.added" ||
        e.type === "response.output_item.done"
      )
        items.set(e.output_index, e.item);
      if (e.type === "response.output_text.delta") {
        const item = items.get(e.output_index) || {
          role: "assistant",
          content: [],
        };
        const idx = e.content_index ?? 0;
        const block = item.content?.[idx] || { type: "output_text", text: "" };
        block.text = (block.text || "") + (e.delta || "");
        (item.content ||= [])[idx] = block;
        items.set(e.output_index, item);
      }
      if (e.type === "response.function_call_arguments.delta") {
        const item = items.get(e.output_index);
        if (item) item.arguments = (item.arguments || "") + (e.delta || "");
      }
      if (e.type === "message_start" && e.message?.content)
        e.message.content.forEach((b, i) => anthropic.set(i, b));
      if (e.type === "content_block_start")
        anthropic.set(e.index, { ...e.content_block });
      if (e.type === "content_block_delta") {
        const b = anthropic.get(e.index) || {};
        const delta = e.delta || {};
        for (const k of ["text", "thinking", "signature"])
          if (typeof delta[k] === "string") b[k] = (b[k] || "") + delta[k];
        if (typeof delta.partial_json === "string")
          b.partial = (b.partial || "") + delta.partial_json;
        anthropic.set(e.index, b);
      }
      for (const c of Array.isArray(e.choices) ? e.choices : []) {
        const choice = chat.get(c.index) || {
          role: "assistant",
          content: "",
          tool_calls: [],
        };
        const d = c.delta || {};
        choice.content += d.content || "";
        if (d.reasoning_content)
          choice.reasoning_content =
            (choice.reasoning_content || "") + d.reasoning_content;
        for (const t of d.tool_calls || []) {
          const i = t.index ?? 0,
            call = choice.tool_calls[i] || {
              function: { name: "", arguments: "" },
            };
          if (t.id) call.id = t.id;
          call.function.name += t.function?.name || "";
          call.function.arguments += t.function?.arguments || "";
          choice.tool_calls[i] = call;
        }
        chat.set(c.index, choice);
      }
    }
    const byIndex = (m) =>
      [...m]
        .sort((a, b) => a[0] - b[0])
        .map((x) => x[1])
        .filter(Boolean);
    const parts = byIndex(items);
    if (anthropic.size) {
      const content = byIndex(anthropic);
      for (const b of content)
        if (b.partial !== undefined) {
          try {
            b.input = JSON.parse(b.partial);
          } catch {
            b.input = b.partial;
          }
          delete b.partial;
        }
      parts.push({ role: "assistant", content });
    }
    parts.push(...byIndex(chat), ...errors);
    return parts.length ? parts : [{ role: "provider", content: raw }];
  }
  function wireRequest(req) {
    const section = div("mc-stream");
    if (req.system != null)
      section.append(...contentBlocks("system", req.system));
    if (req.instructions != null)
      section.append(...contentBlocks("system", req.instructions));
    if (Array.isArray(req.tools)) {
      const tools = node(
        "details",
        "mc-tools",
        node("summary", "", "可用工具 · " + req.tools.length),
      );
      for (const t of req.tools)
        tools.append(message("tool", t.name || t.function?.name || t.type, t));
      section.append(tools);
    }
    section.append(...wireMessages(req.messages ?? req.input));
    const extra = Object.fromEntries(
      Object.entries(req).filter(
        ([k]) =>
          !["input", "messages", "tools", "instructions", "system"].includes(k),
      ),
    );
    if (Object.keys(extra).length)
      section.append(
        node(
          "details",
          "mc-extra",
          node("summary", "", "请求参数"),
          fullText(extra),
        ),
      );
    return section;
  }
  async function wire(root, endpoint, signal) {
    const stateName = (c) =>
      ({
        interrupted: "响应流中断",
        upstream_error:
          c.status >= 200 && c.status < 300 && c.response_bytes
            ? "响应流中断（上游错误）"
            : "上游连接错误",
        client_disconnected: "CLI 已断开",
        response_unrecorded: "尚无响应记录",
        http_error: "提供方错误",
      })[c.state] || (c.status >= 400 ? "提供方错误" : "");
    const [index, { createParser }] = await Promise.all([
      json(endpoint, signal),
      import("/vendor/eventsource-parser.js"),
    ]);
    if (index.format !== "model-context-v1" || !Array.isArray(index.calls))
      throw Error("不支持的模型调用记录格式");
    const calls = index.calls;
    if (!calls.length) {
      root.replaceChildren(empty("没有已记录的模型调用。"));
      return;
    }
    const nav = node("nav", "mc-call-list", node("h3", "", "模型调用"));
    const panel = node("section", "mc-call-detail");
    const menu = div("mc-menu"),
      header = div(
        "mc-wire-head",
        node("h3", "", "调用记录"),
        span("", nfmt(calls.length) + " 次调用"),
      );
    const params = new URLSearchParams(location.hash.split("?")[1]),
      base = location.hash.split("?", 1)[0];
    let activeId,
      generation = 0,
      controller;
    const selectors = new Map();
    const stop = () => controller?.abort();
    signal.addEventListener("abort", stop, { once: true });
    async function choose(call, n, updateHash) {
      activeId = call.id;
      const ticket = ++generation;
      controller?.abort();
      controller = new AbortController();
      if (updateHash)
        history.replaceState(
          null,
          "",
          base + "?call=" + encodeURIComponent(call.id),
        );
      for (const [id, b] of selectors)
        b.setAttribute("aria-current", id === call.id ? "step" : "false");
      panel.replaceChildren(empty("正在读取本次调用…"));
      try {
        const d = await json(
          endpoint + "?call=" + encodeURIComponent(call.id),
          controller.signal,
        );
        if (signal.aborted || ticket !== generation) return;
        const title = div(
          "mc-call-head",
          node("h3", "", "调用 " + (n + 1)),
          span("mc-ref", d.model || call.model || ""),
          span("mc-ref", d.route || call.route || ""),
          span(
            "mc-ref",
            (d.source || call.source) === "fixture"
              ? "本地固定响应"
              : d.provider || call.provider || "",
          ),
        );
        const unavailable = (withheld, truncated) =>
          withheld
            ? "此正文在归档前已隐去。"
            : truncated
              ? "记录已截断，以下为实际保留的片段。"
              : null;
        const tabs = div("mc-tabs"),
          body = div("mc-call-body"),
          content = () => {
            const request = d.request,
              response = d.response;
            body.replaceChildren(node("h4", "mc-divider", "发出的请求"));
            const missingRequest = unavailable(
              d.request_withheld,
              d.request_truncated,
            );
            if (missingRequest) body.append(empty(missingRequest));
            if (request && typeof request === "object")
              body.append(wireRequest(request));
            else if (d.request_excerpt)
              body.append(fullText(d.request_excerpt));
            else if (!missingRequest)
              body.append(empty("本次请求内容未保存。"));
            const state = stateName(d);
            const failure = d.status >= 400 || d.state === "http_error";
            body.append(
              node("h4", "mc-divider", failure ? "提供方错误响应" : "本次响应"),
            );
            if (state && d.state !== "response_unrecorded") {
              body.append(
                node(
                  "p",
                  "mc-state-notice",
                  [Number.isInteger(d.status) && "HTTP " + d.status, state]
                    .filter(Boolean)
                    .join(" · "),
                ),
              );
            }
            const missingResponse = unavailable(
              d.response_withheld,
              d.response_truncated,
            );
            if (missingResponse) body.append(empty(missingResponse));
            const parts = responseParts(response, createParser);
            if (!parts.length)
              body.append(
                empty(
                  d.state === "response_unrecorded"
                    ? "尚无响应记录。"
                    : "未收到可展示的响应正文。",
                ),
              );
            else body.append(...wireMessages(parts));
            if (
              d.state !== "response_unrecorded" &&
              (d.complete === false || call.complete === false)
            )
              body.append(
                empty("调用记录未完整结束。以上仅展示实际保存的内容。"),
              );
          };
        const views = [
          ["对话", content],
          [
            "请求 JSON",
            () => {
              body.replaceChildren(
                fullText(
                  d.request ?? d.request_excerpt ?? "没有可读取的请求正文。",
                  true,
                ),
              );
              const note = unavailable(d.request_withheld, d.request_truncated);
              if (note) body.prepend(empty(note));
            },
          ],
          [
            "原始响应",
            () => {
              body.replaceChildren(
                fullText(
                  d.response ||
                    (d.state === "response_unrecorded"
                      ? "尚无响应记录。"
                      : "没有可读取的响应正文。"),
                  true,
                ),
              );
              const note = unavailable(
                d.response_withheld,
                d.response_truncated,
              );
              if (note) body.prepend(empty(note));
            },
          ],
        ];
        for (const [label, show] of views) {
          const b = button(
            label,
            () => {
              for (const x of tabs.children)
                x.setAttribute("aria-pressed", String(x === b));
              show();
            },
            "mc-tab",
          );
          tabs.append(b);
        }
        tabs.firstElementChild.setAttribute("aria-pressed", "true");
        panel.replaceChildren(title, tabs, body);
        content();
      } catch (err) {
        if (!signal.aborted && ticket === generation)
          panel.replaceChildren(
            empty(err.message),
            button("重试", () => choose(call, n, false)),
          );
      }
    }
    calls.forEach((c, i) => {
      const b = button("", () => choose(c, i, true), "mc-call");
      b.append(
        node("strong", "", "调用 " + (i + 1)),
        span("mc-ref", c.status != null ? "HTTP " + c.status : "未返回"),
        node(
          "small",
          "",
          [
            stateName(c),
            Number.isFinite(c.request_bytes) &&
              "请求 " + nfmt(c.request_bytes) + " B",
          ]
            .filter(Boolean)
            .join(" · "),
        ),
      );
      selectors.set(c.id, b);
      menu.append(b);
    });
    nav.append(menu);
    root.replaceChildren(header, div("mc-wire", nav, panel));
    let i = calls.findIndex((c) => String(c.id) === params.get("call"));
    if (i < 0) i = 0;
    await choose(calls[i], i, false);
  }

  function archiveRows(lines, library) {
    const entries = [];
    for (const [i, line] of lines.split(/\r?\n/).entries()) {
      if (!line.trim()) continue;
      try {
        const obj = JSON.parse(line);
        if (obj && typeof obj === "object" && !Array.isArray(obj))
          entries.push([i + 1, obj]);
      } catch {
        /* malformed tail remains in the source download */
      }
    }
    const claude =
      entries.some(([, e]) => e.type === "system" && e.claude_code_version) ||
      entries.some(([, e]) =>
        e.message?.content?.some?.((b) => b?.type === "tool_use"),
      );
    const calls = new Map(),
      observations = new Map(),
      repeated = new Set();
    if (claude && library) {
      // Use the upstream normalizer for Claude's split messages and paired
      // tool observations, then project them back to exact JSONL line anchors.
      const native = entries
        .map(([, e]) => e)
        .filter((e) => e.type === "assistant" || e.type === "user");
      const safeIds = native.every((e) =>
        array(e.message?.content).every(
          (b) =>
            !b ||
            ![b.id, b.tool_use_id].some(
              (id) =>
                typeof id === "string" &&
                (id === "__proto__" || Object.hasOwn(Object.prototype, id)),
            ),
        ),
      );
      const normalized = safeIds
        ? library.claudeCodeToAtif(native)
        : { steps: [] };
      for (const step of normalized.steps) {
        for (const c of step.tool_calls || []) {
          if (calls.has(c.tool_call_id)) repeated.add(c.tool_call_id);
          calls.set(c.tool_call_id, c);
        }
        for (const r of step.observation?.results || [])
          observations.set(r.source_call_id, r);
      }
    }
    const rows = [],
      opened = new Set(),
      usedUuids = new Set(),
      commands = new Map();
    const add = (line, role, title, body, id) =>
      rows.push({ line, role, title, body, id });
    for (const [line, e] of entries) {
      if (e.uuid && usedUuids.has(e.uuid)) continue;
      if (e.uuid) usedUuids.add(e.uuid);
      if (
        e.isApiErrorMessage ||
        (e.type === "assistant" && e.message?.model === "<synthetic>")
      )
        continue;
      if ((e.type === "assistant" || e.type === "user") && e.message) {
        for (const b of array(e.message.content)) {
          if (!b) continue;
          if (typeof b === "string" || b.type === "text")
            add(line, e.type, "", typeof b === "string" ? b : b.text);
          else if (b.type === "tool_use" || b.type === "server_tool_use") {
            const mapped = !repeated.has(b.id) && calls.get(b.id);
            add(
              line,
              "assistant",
              "调用 " + (mapped?.function_name || b.name),
              mapped?.arguments ?? b.input,
              b.id,
            );
          } else if (
            b.type === "tool_result" ||
            b.type === "web_search_tool_result"
          ) {
            const mapped =
              !repeated.has(b.tool_use_id) && observations.get(b.tool_use_id);
            add(
              line,
              "tool",
              b.is_error ? "工具返回 · 失败" : "工具返回",
              mapped?.content ?? b.content,
              b.tool_use_id,
            );
          }
        }
      } else if (e.type === "item.started" || e.type === "item.completed") {
        const item = e.item || {};
        if (item.type === "agent_message" && e.type === "item.completed")
          add(line, "assistant", "", item.text);
        if (item.type === "command_execution") {
          if (!opened.has(item.id)) {
            add(line, "assistant", "调用 Shell", item.command, item.id);
            opened.add(item.id);
          }
          if (e.type === "item.completed") {
            add(
              line,
              "tool",
              "Shell 返回" +
                (Number.isInteger(item.exit_code)
                  ? " · 退出 " + item.exit_code
                  : ""),
              item.aggregated_output,
              item.id,
            );
            opened.delete(item.id);
          }
        }
        if (item.type === "mcp_tool_call" && e.type === "item.completed") {
          add(
            line,
            "assistant",
            "调用 " + (item.tool || "MCP"),
            item.arguments,
            item.id,
          );
          add(line, "tool", "工具返回", item.result ?? item.error, item.id);
        }
      } else if (e.role === "assistant") {
        for (const b of array(e.content))
          if (typeof b === "string" || b?.type === "text")
            add(line, "assistant", "", typeof b === "string" ? b : b.text);
        for (const c of e.tool_calls || []) {
          add(
            line,
            "assistant",
            "调用 " + (c.function?.name || c.name || "工具"),
            c.function?.arguments ?? c,
            c.id,
          );
        }
      } else if (e.role === "tool")
        add(
          line,
          "tool",
          e.is_error ? "工具返回 · 失败" : "工具返回",
          e.content,
          e.tool_call_id,
        );
      else if (e.type === "message_end" && e.message?.role === "assistant") {
        for (const b of array(e.message.content))
          if (typeof b === "string" || b?.type === "text")
            add(line, "assistant", "", typeof b === "string" ? b : b.text);
      } else if (e.type === "tool_execution_start") {
        add(line, "assistant", "调用 " + e.toolName, e.args, e.toolCallId);
      } else if (e.type === "tool_execution_end") {
        add(
          line,
          "tool",
          e.toolName + " 返回" + (e.isError ? " · 失败" : ""),
          e.result,
          e.toolCallId,
        );
      } else if (e.type === "tool_call" && e.tool_call) {
        for (const [tool, payload] of Object.entries(e.tool_call)) {
          if (
            e.subtype === "started" ||
            (e.subtype === "completed" && !commands.has(e.call_id))
          ) {
            add(line, "assistant", "调用 " + tool, payload.args, e.call_id);
            commands.set(e.call_id, tool);
          }
          if (e.subtype === "completed") {
            add(line, "tool", tool + " 返回", payload.result, e.call_id);
            commands.delete(e.call_id);
          }
        }
      }
    }
    return rows;
  }
  async function historical(root, files, url, signal) {
    const [data, prompt, raw] = await Promise.all([
      json(url + "?notes=1", signal),
      localText(files.prompt, signal),
      localText(files.events, signal),
    ]);
    let library = null;
    if (
      raw &&
      (raw.includes('"claude_code_version"') || raw.includes('"tool_use"'))
    )
      library = await trajectoryLibrary();
    if (signal.aborted) return;
    const rows = raw ? archiveRows(raw, library) : [];
    const params = new URLSearchParams(location.hash.split("?")[1]),
      base = location.hash.split("?", 1)[0];
    const target = Number(params.get("line")),
      refs = new Map(),
      flow = div("mc-history");
    const notes = new Map();
    for (const n of data.review_notes || []) {
      if (!notes.has(n.line)) notes.set(n.line, []);
      notes.get(n.line).push(n);
    }
    const banner = div(
      "mc-history-head",
      node("h3", "", "历史会话"),
      span(
        "mc-hint",
        "",
        "未采集逐次 API 请求。本页展示保存的题面和 CLI 事件。",
      ),
    );
    const selectLine = (line) => {
      for (const r of flow.querySelectorAll(".mc-picked"))
        r.classList.remove("mc-picked");
      const r = refs.get(line);
      if (!r) return;
      r.classList.add("mc-picked");
      for (const d of r.querySelectorAll(".mc-inline[aria-expanded=false]"))
        d.click();
      r.scrollIntoView({ block: "center" });
    };
    if (prompt !== null) flow.append(message("user", "保存的完整题面", prompt));
    for (const r of rows) {
      const row = message(r.role, r.title, r.body);
      row.dataset.nativeLine = String(r.line);
      const anchor = link("L" + r.line, base + "?line=" + r.line, "mc-line");
      anchor.addEventListener("click", (e) => {
        e.preventDefault();
        history.replaceState(null, "", anchor.href);
        selectLine(r.line);
      });
      row.querySelector(".mc-mhead").append(anchor);
      if (r.id) row.querySelector(".mc-mhead").title = "call_id: " + r.id;
      if (r.role === "assistant" && !r.title)
        for (const note of notes.get(r.line) || []) row.append(reference(note));
      flow.append(row);
      if (!refs.has(r.line)) refs.set(r.line, row);
    }
    if (!rows.length)
      flow.append(empty("没有保存可展示的原生对话或工具记录。"));
    root.replaceChildren(banner, flow);
    if (target) requestAnimationFrame(() => selectLine(target));
  }

  function mount(trial, files, url, signal) {
    const root = div("trace-explorer", empty("正在读取模型记录…"));
    async function load() {
      try {
        if (files.context)
          await wire(root, url.replace(/\/timeline$/, "/context"), signal);
        else await historical(root, files, url, signal);
      } catch (e) {
        if (!signal.aborted)
          root.replaceChildren(empty(e.message), button("重试", load));
      }
    }
    load();
    return root;
  }
  return { mount };
})();
function trialTimeline(trial, files, url, signal) {
  return ContextReader.mount(trial, files, url, signal);
}
