/* Show only the current observation delivered for this trial. Never join by game ID. */
"use strict";
window.LoLDraft = (() => {
  const sides = ["blue", "red"];
  function el(tag, cls, text) {
    const node = document.createElement(tag);
    node.className = cls;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function icon(action, cls) {
    const frame = el("span", cls);
    if (action.icon) {
      const img = document.createElement("img");
      img.src = action.icon;
      img.alt = "";
      img.width = img.height = 96;
      img.decoding = "async";
      img.addEventListener("error", () => img.remove(), { once: true });
      frame.append(img);
    }
    return frame;
  }
  function team(side, data, picks, match, locked) {
    const section = el("section", "draft-side draft-" + side);
    const head = el("header", "draft-team");
    if (match && typeof match[side + "_logo"] === "string") {
      const mark = el("img", "draft-mark");
      mark.src = match[side + "_logo"];
      mark.alt = "";
      head.append(mark);
    }
    head.append(el("h3", "draft-name", data.name), el("span", "draft-color", side === "blue" ? "蓝方" : "红方"));
    section.append(head);
    if (locked) {
      const list = el("ol", "draft-picks");
      for (const pick of picks) {
        const tile = el("li", "draft-pick");
        tile.title = pick.champion + " · 第 " + pick.turn + " 手";
        const portrait = icon(pick, "draft-portrait");
        portrait.append(el("small", "draft-turn", String(pick.turn).padStart(2, "0")));
        tile.append(portrait, el("span", "draft-caption", pick.label || pick.champion));
        list.append(tile);
      }
      section.append(list);
    }
    if (data.starters.length) {
      const roster = el("ul", "draft-roster");
      roster.setAttribute("aria-label", data.name + " 首发选手");
      for (const player of data.starters) roster.append(el("li", "", player));
      section.append(roster);
    }
    return section;
  }
  function order(actions) {
    const fold = el("details", "draft-order");
    const toggle = el("summary", "", "完整 BP");
    toggle.append(el("span", "", actions.length + " 手"));
    fold.append(toggle);
    // Build consecutive action groups from the actual data, including red-first drafts.
    const groups = el("div", "draft-groups");
    let last, list;
    for (const a of actions) {
      if (a.action !== last) {
        const group = el("div", "draft-group");
        group.append(el("strong", "", a.action === "ban" ? "禁用" : "选择"));
        list = el("ol", "draft-events");
        group.append(list); groups.append(group);
        last = a.action;
      }
      const row = el("li", "draft-event draft-" + a.side);
      row.value = a.turn;
      row.title = (a.side === "blue" ? "蓝方" : "红方") + " · " + a.champion;
      row.append(el("b", "draft-event-turn", String(a.turn).padStart(2, "0")),
        icon(a, "draft-event-icon"), el("span", "draft-event-name", a.label || a.champion),
        el("small", "draft-event-side", a.side === "blue" ? "蓝" : "红"));
      list.append(row);
    }
    fold.append(groups);
    return fold;
  }
  function render(data, match) {
    const host = el("section", "draft-board");
    if (!data || !data.teams || !["lobby", "draft-lock"].includes(data.phase)) {
      host.hidden = true;
      return host;
    }
    const locked = data.phase === "draft-lock";
    const head = el("header", "draft-board-head");
    head.append(el("h2", "", locked ? "双方阵容" : "首发名单"), el("span", "", "PATCH " + data.patch));
    host.append(head);
    const layout = el("div", "draft-sides" + (locked ? "" : " draft-lobby"));
    const actions = locked && Array.isArray(data.actions) ? data.actions : [];
    for (const side of sides) {
      layout.append(team(side, data.teams[side], actions.filter(a => a.action === "pick" && a.side === side), match, locked));
    }
    host.append(layout);
    if (locked && actions.length) host.append(order(actions));
    return host;
  }
  return { render };
})();
