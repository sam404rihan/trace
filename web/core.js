"use strict";
/* Trace core: tiny DOM helpers, random helpers, the "ask" model, and the renderers
   every drill draws with. Topics register themselves with Trace.topic({...}). */
(function () {
  const T = (window.Trace = { topics: [], byId: {}, V: {} });

  // ── DOM ────────────────────────────────────────────────────────────────────
  function build(node, attrs, children) {
    for (const [key, value] of Object.entries(attrs || {})) {
      if (value == null || value === false) continue;
      if (key === "class") node.setAttribute("class", value);
      else if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
      else node.setAttribute(key, value === true ? "" : value);
    }
    for (const child of children.flat(Infinity)) {
      if (child == null || child === false) continue;
      node.append(child instanceof Node ? child : document.createTextNode(String(child)));
    }
    return node;
  }
  T.h = (tag, attrs, ...children) => build(document.createElement(tag), attrs, children);
  T.s = (tag, attrs, ...children) => build(document.createElementNS("http://www.w3.org/2000/svg", tag), attrs, children);
  const { h, s } = T;

  // ── random ─────────────────────────────────────────────────────────────────
  T.rand = (lo, hi) => lo + Math.floor(Math.random() * (hi - lo + 1));
  T.pick = (arr) => arr[Math.floor(Math.random() * arr.length)];
  T.shuffle = (arr) => {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };
  T.sample = (arr, k) => T.shuffle(arr).slice(0, k);
  T.range = (n, start = 0) => Array.from({ length: n }, (_, i) => i + start);
  T.distinct = (k, lo, hi) => T.sample(T.range(hi - lo + 1, lo), k);
  T.letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

  // ── topics ─────────────────────────────────────────────────────────────────
  T.topic = (def) => {
    T.topics.push(def);
    T.byId[def.id] = def;
  };

  // ── asks ───────────────────────────────────────────────────────────────────
  // A drill is a generator. Each `yield` hands the host one question:
  //   { prompt, options?, picks?, answer, accept(v), why(v), note(v) }
  // options -> buttons; picks -> click elements with [data-pick] on the board.
  // The host keeps asking until accept(v) is true, then resumes the drill with v.
  const norm = (o) => (Array.isArray(o) ? { value: o[0], label: o[1] } : typeof o === "object" ? o : { value: o, label: String(o) });

  T.ask = (spec) => {
    const answers = [].concat(spec.answer);
    const accept = spec.accept || ((v) => answers.some((a) => String(a) === String(v)));
    const why = spec.why;
    return {
      prompt: spec.prompt,
      options: spec.options ? spec.options.map(norm) : null,
      picks: !!spec.picks,
      answer: answers[0],
      accept,
      why: (v) => (typeof why === "function" ? why(v) : why && typeof why === "object" ? why[v] ?? why._ : why) || "Not that one. Look again.",
      note: spec.note,
      onPick: spec.onPick,
    };
  };
  T.choose = (prompt, options, answer, why, note) => T.ask({ prompt, options, answer, why, note });
  T.click = (prompt, answer, why, note, options) => T.ask({ prompt, picks: true, options, answer, why, note });

  // Four nearby numbers for "how many?" questions, always containing the answer.
  T.numOptions = (answer, { spread = 3, min = 0, extra = [] } = {}) => {
    const set = new Set([answer]);
    for (const x of extra) if (x >= min && set.size < 4) set.add(x);
    let guard = 0;
    while (set.size < 4 && guard++ < 200) {
      const v = answer + T.rand(-spread, spread);
      if (v >= min) set.add(v);
    }
    for (let v = answer + 1; set.size < 4; v++) set.add(v);
    return [...set].sort((a, b) => a - b);
  };

  // ── renderers ──────────────────────────────────────────────────────────────
  const V = T.V;
  const ptrTone = ["a", "b", "c", "d"];

  V.line = (...parts) => h("p", { class: "line" }, parts);
  V.code = (text) => h("pre", { class: "code" }, text);
  V.k = (text) => h("code", { class: "k" }, text); // inline value
  V.row = (...parts) => h("div", { class: "row-wrap" }, parts);
  V.label = (text) => h("p", { class: "board-label" }, text);

  // Array strip. o: ptr {name: index}, cls(i,v), win [l,r], pick bool|fn(i), key(i), text(i,v), idx, label
  V.array = (vals, o = {}) => {
    const ptrNames = Object.keys(o.ptr || {});
    const tone = (name) => (o.tones && o.tones[name]) || ptrTone[ptrNames.indexOf(name) % 4];
    const cols = vals.map((v, i) => {
      const cls = ["cell"];
      const extra = o.cls ? o.cls(i, v) : "";
      if (extra) cls.push(extra);
      if (o.win && i >= o.win[0] && i <= o.win[1]) {
        cls.push("win");
        if (i === o.win[0]) cls.push("win-l");
        if (i === o.win[1]) cls.push("win-r");
      }
      const pickable = o.pick === true || (typeof o.pick === "function" && o.pick(i));
      const content = o.text ? o.text(i, v) : v;
      const cell = pickable
        ? h("button", { type: "button", class: cls.join(" "), "data-pick": o.key ? o.key(i) : String(i) }, content)
        : h("div", { class: cls.join(" ") }, content);
      const ptrs = ptrNames.filter((name) => o.ptr[name] === i).map((name) => h("span", { class: "ptr t-" + tone(name) }, name));
      return h("div", { class: "col" },
        cell,
        o.idx === false ? null : h("span", { class: "idx" }, o.idxText ? o.idxText(i) : i),
        ptrNames.length ? h("span", { class: "ptrs" }, ptrs) : null);
    });
    return h("figure", { class: "arr" + (o.small ? " small" : "") + (o.wide ? " wide" : "") },
      o.label ? h("figcaption", {}, o.label) : null,
      h("div", { class: "arr-row" }, cols));
  };

  // Vertical bars (heights). o: ptr, cls(i), water [l, r, level], label
  V.bars = (vals, o = {}) => {
    const cw = 44, H = 150, top = 22, max = Math.max(...vals, 1), sc = H / max;
    const W = vals.length * cw;
    const g = [];
    if (o.water) {
      const [l, r, level] = o.water;
      g.push(s("rect", { class: "water", x: l * cw + cw / 2, y: top + H - level * sc, width: (r - l) * cw, height: level * sc }));
    }
    vals.forEach((v, i) => {
      const x = i * cw + 9, bh = v * sc;
      g.push(s("rect", { class: "bar " + (o.cls ? o.cls(i) : ""), x, y: top + H - bh, width: cw - 18, height: bh, rx: 3 }));
      g.push(s("text", { class: "bar-v", x: i * cw + cw / 2, y: top + H - bh - 6 }, v));
      g.push(s("text", { class: "bar-i", x: i * cw + cw / 2, y: top + H + 16 }, i));
    });
    const names = Object.keys(o.ptr || {});
    names.forEach((name, k) => {
      const i = o.ptr[name];
      const sameBefore = names.slice(0, k).filter((n) => o.ptr[n] === i).length;
      g.push(s("text", { class: "bar-ptr t-" + ptrTone[k % 4], x: i * cw + cw / 2, y: top + H + 36 + sameBefore * 16 }, name));
    });
    return h("figure", { class: "svgfig" }, s("svg", { viewBox: `0 0 ${W} ${top + H + 62}`, width: W, class: "bars" }, g));
  };

  // Binary tree from {id, left, right} objects. o: label(n), cls(n), pick(n), badge(n), key(n)
  V.btree = (root, o = {}) => {
    const order = [];
    const depth = new Map();
    (function walk(n, d) {
      if (!n) return;
      walk(n.left, d + 1);
      order.push(n);
      depth.set(n, d);
      walk(n.right, d + 1);
    })(root, 0);
    const gap = o.gap || 46, dy = 62, pad = 28;
    const pos = new Map(order.map((n, i) => [n, { x: pad + i * gap, y: pad + depth.get(n) * dy }]));
    const maxD = Math.max(0, ...depth.values());
    const W = pad * 2 + Math.max(0, order.length - 1) * gap, Hh = pad * 2 + maxD * dy + 6;
    const edges = [], nodes = [];
    for (const n of order) {
      const p = pos.get(n);
      for (const c of [n.left, n.right]) {
        if (!c) continue;
        const q = pos.get(c);
        edges.push(s("line", { class: "edge " + (o.ecls ? o.ecls(n, c) : ""), x1: p.x, y1: p.y, x2: q.x, y2: q.y }));
      }
      nodes.push(nodeGlyph(p.x, p.y, o.label ? o.label(n) : n.val, o.cls ? o.cls(n) : "", o.pick && o.pick(n) ? (o.key ? o.key(n) : String(n.id)) : null, o.badge ? o.badge(n) : null));
    }
    return h("figure", { class: "svgfig" }, s("svg", { viewBox: `0 0 ${W} ${Hh}`, width: W, class: "tree" }, edges, nodes));
  };

  function nodeGlyph(x, y, label, cls, pickKey, badge, r = 17) {
    const g = s("g", {
      class: "node " + (cls || "") + (pickKey != null ? " pickable" : ""),
      transform: `translate(${x},${y})`,
      "data-pick": pickKey,
      tabindex: pickKey != null ? "0" : null,
      role: pickKey != null ? "button" : null,
      "aria-label": pickKey != null ? String(label) : null,
    },
      s("circle", { r }),
      s("text", { class: "nlabel", dy: "0.35em" }, label));
    if (badge != null && badge !== "") {
      g.append(s("rect", { class: "badge-bg", x: r - 6, y: -r - 10, width: String(badge).length * 7.4 + 10, height: 17, rx: 8.5 }));
      g.append(s("text", { class: "badge", x: r - 1, y: -r + 2.5 }, badge));
    }
    return g;
  }
  V.nodeGlyph = nodeGlyph;

  // N-ary trees / forests. roots: array. o: kids(n), label, cls, pick, key, badge, elabel(parent, child)
  V.ntree = (roots, o = {}) => {
    const gap = o.gap || 44, dy = o.dy || 60, pad = 26;
    const pos = new Map();
    let leaf = 0, maxD = 0;
    (function place(list, d) {
      for (const n of list) {
        const kids = o.kids(n);
        maxD = Math.max(maxD, d);
        if (!kids.length) {
          pos.set(n, { x: pad + leaf++ * gap, y: pad + d * dy });
        } else {
          place(kids, d + 1);
          const xs = kids.map((k) => pos.get(k).x);
          pos.set(n, { x: (xs[0] + xs[xs.length - 1]) / 2, y: pad + d * dy });
        }
      }
      return list;
    })(roots, 0);
    const W = pad * 2 + Math.max(0, leaf - 1) * gap, Hh = pad * 2 + maxD * dy + 6;
    const edges = [], nodes = [], labels = [];
    for (const [n, p] of pos) {
      for (const k of o.kids(n)) {
        const q = pos.get(k);
        edges.push(s("line", { class: "edge " + (o.ecls ? o.ecls(n, k) : ""), x1: p.x, y1: p.y, x2: q.x, y2: q.y }));
        if (o.elabel) labels.push(s("text", { class: "elabel", x: (p.x + q.x) / 2 + (q.x >= p.x ? 7 : -7), y: (p.y + q.y) / 2 }, o.elabel(n, k)));
      }
      nodes.push(nodeGlyph(p.x, p.y, o.label(n), o.cls ? o.cls(n) : "", o.pick && o.pick(n) ? o.key(n) : null, o.badge ? o.badge(n) : null, o.r || 17));
    }
    return h("figure", { class: "svgfig" }, s("svg", { viewBox: `0 0 ${W} ${Hh}`, width: W, class: "tree" }, edges, labels, nodes));
  };

  // Graph with fixed positions in unit coords. g: {nodes:[{id,x,y}], edges:[{a,b,w}]}
  // o: directed, ncls(id), ecls(e), badge(id), pickNodes(id)->bool, pickEdges, label(id), W, H
  V.graph = (g, o = {}) => {
    const W = o.W || 520, H = o.H || 300, pad = 34;
    const at = Object.fromEntries(g.nodes.map((n) => [n.id, { x: pad + n.x * (W - 2 * pad), y: pad + n.y * (H - 2 * pad) }]));
    const edges = [], weights = [], nodes = [];
    for (const e of g.edges) {
      const p = at[e.a], q = at[e.b];
      const dx = q.x - p.x, dy = q.y - p.y, len = Math.hypot(dx, dy) || 1;
      const ux = dx / len, uy = dy / len, r = 19;
      const x1 = p.x + ux * r, y1 = p.y + uy * r, x2 = q.x - ux * (r + (o.directed ? 4 : 0)), y2 = q.y - uy * (r + (o.directed ? 4 : 0));
      const ek = `${e.a}-${e.b}`;
      const pickable = o.pickEdges && o.pickEdges(e);
      edges.push(s("line", { class: "gedge " + (o.ecls ? o.ecls(e) : "") + (pickable ? " pickable" : ""), x1, y1, x2, y2, "marker-end": o.directed ? "url(#arrow)" : null, "data-pick": pickable ? ek : null }));
      if (e.w != null) {
        const mx = (p.x + q.x) / 2 - uy * 11, my = (p.y + q.y) / 2 + ux * 11;
        weights.push(s("g", { class: "wtag " + (o.ecls ? o.ecls(e) : ""), transform: `translate(${mx},${my})`, "data-pick": pickable ? ek : null },
          s("rect", { x: -10, y: -9, width: 20, height: 18, rx: 4 }),
          s("text", { dy: "0.35em" }, e.w)));
      }
    }
    for (const n of g.nodes) {
      const p = at[n.id];
      nodes.push(nodeGlyph(p.x, p.y, o.label ? o.label(n.id) : n.id, o.ncls ? o.ncls(n.id) : "", o.pickNodes && o.pickNodes(n.id) ? n.id : null, o.badge ? o.badge(n.id) : null, 19));
    }
    const defs = s("defs", {}, s("marker", { id: "arrow", viewBox: "0 0 10 10", refX: "8", refY: "5", markerWidth: "7", markerHeight: "7", orient: "auto-start-reverse" },
      s("path", { d: "M0,0 L10,5 L0,10 z", class: "arrowhead" })));
    return h("figure", { class: "svgfig" }, s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, class: "graph" }, defs, edges, weights, nodes));
  };

  // A queen on a board: drawn, so it matches the tiles. Cells with the "queen" class show it in place of their text.
  const queen = () => s("svg", { class: "piece", viewBox: "0 0 24 24", role: "img", "aria-label": "queen" },
    s("path", { d: "M3.5 8.5l4.6 3.9L12 5l3.9 7.4 4.6-3.9-1.9 9.5H5.4z" }), s("rect", { x: 5, y: 18.6, width: 14, height: 2.6, rx: 1.3 }));

  // Grid. cell(r,c) -> {t, cls, pick (key)}; o: rowHead[], colHead[], size
  V.grid = (R, C, cell, o = {}) => {
    const kids = [];
    if (o.colHead) {
      kids.push(h("span", { class: "ghead corner" }, o.corner || ""));
      o.colHead.forEach((t) => kids.push(h("span", { class: "ghead" }, t)));
    }
    for (let r = 0; r < R; r++) {
      if (o.colHead || o.rowHead) kids.push(h("span", { class: "ghead" }, o.rowHead ? o.rowHead[r] : ""));
      for (let c = 0; c < C; c++) {
        const d = cell(r, c) || {};
        const t = /(^| )queen( |$)/.test(d.cls || "") ? queen() : d.t ?? "";
        kids.push(d.pick != null
          ? h("button", { type: "button", class: "gcell " + (d.cls || ""), "data-pick": d.pick }, t)
          : h("span", { class: "gcell " + (d.cls || "") }, t));
      }
    }
    const heads = o.colHead || o.rowHead ? 1 : 0;
    return h("figure", { class: "gridfig" },
      o.label ? h("figcaption", {}, o.label) : null,
      h("div", { class: "grid " + (o.cls || ""), style: `grid-template-columns: repeat(${C + heads}, var(--gc, 40px))` }, kids));
  };

  // A row of chips: stacks, queues, sets. o: label, cls(i), dir ('h'|'v'), ends [leftTag, rightTag]
  V.chips = (items, o = {}) =>
    h("figure", { class: "chips " + (o.dir === "v" ? "vert" : "") },
      o.label ? h("figcaption", {}, o.label) : null,
      h("div", { class: "chip-row" },
        o.ends ? h("span", { class: "chip-end" }, o.ends[0]) : null,
        items.length ? items.map((t, i) => h("span", { class: "chip " + (o.cls ? o.cls(i) : "") }, t)) : h("span", { class: "chip-empty" }, o.empty || "empty"),
        o.ends ? h("span", { class: "chip-end" }, o.ends[1]) : null));

  // Key -> value table (hash maps). entries [[k, v]]; o: label, cls(k)
  V.kv = (entries, o = {}) =>
    h("figure", { class: "kv" },
      o.label ? h("figcaption", {}, o.label) : null,
      entries.length
        ? h("div", { class: "kv-rows" }, entries.map(([k, v]) => h("div", { class: "kv-row " + (o.cls ? o.cls(k) : "") }, h("span", { class: "kv-k" }, k), h("span", { class: "kv-v" }, v))))
        : h("p", { class: "chip-empty" }, o.empty || "empty"));

  // Intervals on a number line, one row each. items [{s, e, label, cls, lane, pick}]; o: min, max
  V.timeline = (items, o = {}) => {
    const min = o.min ?? Math.min(...items.map((i) => i.s)), max = o.max ?? Math.max(...items.map((i) => i.e));
    const lanes = o.lanes ?? items.length;
    const W = 540, padL = o.padL ?? 42, rowH = 30, top = 8;
    const x = (v) => padL + ((v - min) / (max - min || 1)) * (W - padL - 14);
    const H = top + lanes * rowH + 30;
    const g = [];
    for (let v = min; v <= max; v++) {
      g.push(s("line", { class: "tick", x1: x(v), x2: x(v), y1: top, y2: top + lanes * rowH }));
      g.push(s("text", { class: "tick-t", x: x(v), y: top + lanes * rowH + 18 }, v));
    }
    items.forEach((it, i) => {
      const lane = it.lane ?? i;
      const y = top + lane * rowH + 5;
      if (o.laneLabels && i === items.findIndex((t) => (t.lane ?? 0) === lane)) g.push(s("text", { class: "lane-t", x: 4, y: y + 14 }, o.laneLabels[lane] ?? ""));
      g.push(s("g", { class: "ival " + (it.cls || "") + (it.pick != null ? " pickable" : ""), "data-pick": it.pick ?? null, tabindex: it.pick != null ? "0" : null, role: it.pick != null ? "button" : null },
        s("rect", { x: x(it.s), y, width: Math.max(4, x(it.e) - x(it.s)), height: rowH - 10, rx: 4 }),
        s("text", { x: x(it.s) + 6, y: y + (rowH - 10) / 2, dy: "0.35em" }, it.label ?? `${it.s}–${it.e}`)));
    });
    for (const lane of o.laneLabels && !items.length ? o.laneLabels.keys() : []) g.push(s("text", { class: "lane-t", x: 4, y: top + lane * rowH + 19 }, o.laneLabels[lane]));
    return h("figure", { class: "svgfig" }, s("svg", { viewBox: `0 0 ${W} ${H}`, width: W, class: "timeline" }, g));
  };
})();
