"use strict";
/* Input drawings for problem statements: the first test's real arguments drawn as a tree, a graph, a
   grid, a linked list or an array, chosen from each parameter's type and name. Scalars aren't drawn. */
(function () {
  const T = window.Trace;
  const { s } = T;

  const scalar = (v) => v === null || ["number", "string", "boolean"].includes(typeof v);
  const isInt = (v) => Number.isInteger(v);
  const show = (v) => (v === null ? "None" : v === true ? "True" : v === false ? "False" : String(v));
  const svg = (kind, w, h, kids) => s("svg", { class: "viz", "data-kind": kind, viewBox: `0 0 ${w} ${h}`, width: w, "aria-hidden": "true" }, kids);
  const text = (x, y, t, cls = "v-label") => s("text", { x, y, class: cls }, show(t));
  function arrow(x1, y1, x2, y2) {
    const a = Math.atan2(y2 - y1, x2 - x1), k = 7;
    const pts = [[x2, y2], [x2 - k * Math.cos(a - 0.45), y2 - k * Math.sin(a - 0.45)], [x2 - k * Math.cos(a + 0.45), y2 - k * Math.sin(a + 0.45)]];
    return [s("line", { x1, y1, x2, y2, class: "v-edge" }), s("path", { d: "M" + pts.map((p) => p.join(",")).join("L") + "Z", class: "v-head" })];
  }
  const rim = (a, b, r) => { const d = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1; return [a[0] + ((b[0] - a[0]) * r) / d, a[1] + ((b[1] - a[1]) * r) / d]; };

  // Level-order with None for a missing child, as the course writes trees. x is the in-order position.
  function tree(values) {
    if (!values.length || values[0] === null) return null;
    const nodes = [{ v: values[0], kids: [] }], queue = [nodes[0]];
    let i = 1;
    while (queue.length && i < values.length) {
      const n = queue.shift();
      for (const side of [0, 1]) {
        if (i >= values.length) break;
        const v = values[i++];
        if (v === null) continue;
        const kid = { v, kids: [], side };
        n.kids[side] = kid;
        nodes.push(kid);
        queue.push(kid);
      }
    }
    if (nodes.length > 31) return null;
    let x = 0, depth = 0;
    (function place(n, d) {
      if (!n) return;
      place(n.kids[0], d + 1);
      n.x = x++; n.d = d; depth = Math.max(depth, d);
      place(n.kids[1], d + 1);
    })(nodes[0], 0);
    const dx = 38, dy = 52, r = 15, pad = 20;
    const at = (n) => [pad + n.x * dx, pad + n.d * dy];
    const edges = nodes.flatMap((n) => n.kids.filter(Boolean).map((k) => {
      const [a, b] = [rim(at(n), at(k), r), rim(at(k), at(n), r)];
      return s("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], class: "v-edge" });
    }));
    const dots = nodes.map((n) => s("g", {}, s("circle", { cx: at(n)[0], cy: at(n)[1], r, class: "v-node" }), text(at(n)[0], at(n)[1], n.v)));
    return svg("tree", pad * 2 + (x - 1) * dx, pad * 2 + depth * dy, [edges, dots]);
  }

  // Edges [u, v] or [u, v, w]; prerequisites [a, b] mean b comes before a.
  function graph(edges, name, others) {
    const flip = /prereq/i.test(name);
    const directed = /prereq|time|flight|ticket|order|depend|direct|trust/i.test(name);
    const ends = new Set(edges.flatMap((e) => [e[0], e[1]]));
    const n = others.find((o) => isInt(o.value) && /^(n|num_\w+|nodes?|count)$/i.test(o.name))?.value;
    if (isInt(n) && n <= 12) {
      const all = [...ends];
      const from = all.length && all.every((v) => v >= 1 && v <= n) && !all.includes(0) ? 1 : 0;
      for (let v = from; v < n + from; v++) ends.add(v);
    }
    const ids = [...ends].sort((a, b) => a - b);
    if (ids.length < 2 || ids.length > 12) return null;
    // Two nodes sit side by side; more go round a circle.
    const r = 15;
    let W, H, pos;
    if (ids.length === 2) {
      W = 200; H = 2 * r + 34;
      pos = new Map([[ids[0], [r + 24, H / 2]], [ids[1], [W - r - 24, H / 2]]]);
    } else {
      const R = 40 + ids.length * 9, c = R + r + 16;
      W = H = 2 * c;
      pos = new Map(ids.map((v, k) => {
        const t = (2 * Math.PI * k) / ids.length - Math.PI / 2;
        return [v, [c + R * Math.cos(t), c + R * Math.sin(t)]];
      }));
    }
    const lines = edges.map(([u, v, w]) => {
      const [p, q] = flip ? [pos.get(v), pos.get(u)] : [pos.get(u), pos.get(v)];
      const a = rim(p, q, r), b = rim(q, p, r + (directed ? 2 : 0));
      return s("g", {}, directed ? arrow(a[0], a[1], b[0], b[1]) : s("line", { x1: a[0], y1: a[1], x2: b[0], y2: b[1], class: "v-edge" }),
        w === undefined ? null : text((a[0] + b[0]) / 2 + 8, (a[1] + b[1]) / 2 - 9, w, "v-weight"));
    });
    const dots = ids.map((v) => { const [x, y] = pos.get(v); return s("g", {}, s("circle", { cx: x, cy: y, r, class: "v-node" }), text(x, y, v)); });
    return svg("graph", W, H, [lines, dots]);
  }

  function grid(rows) {
    const c = 26, g = 3, pad = 4;
    const on = (v) => v === 1 || v === "1" || v === "#" || v === "X" || v === true;
    const cells = rows.flatMap((row, i) => row.map((v, j) => s("g", {},
      s("rect", { x: pad + j * (c + g), y: pad + i * (c + g), width: c, height: c, rx: 6, class: "v-cell" + (on(v) ? " on" : "") }),
      text(pad + j * (c + g) + c / 2, pad + i * (c + g) + c / 2, v))));
    return svg("grid", 2 * pad + rows[0].length * (c + g) - g, 2 * pad + rows.length * (c + g) - g, cells);
  }

  function array(values, kind = "array") {
    const c = 30, g = 4, pad = 4;
    const cells = values.map((v, i) => s("g", {},
      s("rect", { x: pad + i * (c + g), y: pad, width: c, height: c, rx: 7, class: "v-cell" }),
      text(pad + i * (c + g) + c / 2, pad + c / 2, v),
      kind === "array" ? text(pad + i * (c + g) + c / 2, pad + c + 12, i, "v-index") : null));
    return svg(kind, 2 * pad + values.length * (c + g) - g, pad + c + (kind === "array" ? 20 : pad), cells);
  }

  function linked(values) {
    const w = 34, gap = 22, pad = 4, h = 30;
    const kids = values.map((v, i) => {
      const x = pad + i * (w + gap);
      return s("g", {}, s("rect", { x, y: pad, width: w, height: h, rx: 7, class: "v-node" }), text(x + w / 2, pad + h / 2, v),
        arrow(x + w + 2, pad + h / 2, x + w + gap - 3, pad + h / 2));
    });
    const end = pad + values.length * (w + gap);
    return svg("list", end + 34, 2 * pad + h, [kids, text(end + 14, pad + h / 2, null, "v-index")]);
  }

  function draw(value, param, others) {
    const { name, type = "" } = param;
    if (!Array.isArray(value) || value.length < 1) return null;
    if (/TreeNode/.test(type)) return tree(value);
    if (/ListNode/.test(type)) return value.length <= 12 && value.every(scalar) ? linked(value) : null;
    const pairs = value.every((e) => Array.isArray(e) && (e.length === 2 || e.length === 3) && e.every(isInt));
    if (pairs && /edge|prereq|time|flight|road|connection|pair|link|wire|trust|graph/i.test(name)) return graph(value, name, others);
    const rect = value.length >= 2 && value.every((r) => Array.isArray(r) && r.length === value[0].length && r.length >= 2 && r.every(scalar));
    if (rect && value.length <= 10 && value[0].length <= 12) return grid(value);
    if (value.length >= 2 && value.length <= 16 && value.every((v) => scalar(v) && String(show(v)).length <= 4)) return array(value);
    return null;
  }

  // A JSON value written the way Python prints it: None, True, [1, 2], 'a'.
  T.pyRepr = (v) => v === null ? "None" : v === true ? "True" : v === false ? "False"
    : Array.isArray(v) ? `[${v.map(T.pyRepr).join(", ")}]` : typeof v === "string" ? `'${v}'`
      : typeof v === "object" ? `{${Object.entries(v).map(([k, x]) => `'${k}': ${T.pyRepr(x)}`).join(", ")}}` : String(v);

  // One figure per drawable parameter of the first example, at most two. Returns [] when nothing draws.
  T.inputFigures = (params, example) => {
    if (!example || !params || !params.length) return [];
    const args = params.map((p, k) => ({ name: p.name, type: p.type, value: example.args[k] }));
    const out = [];
    for (const a of args) {
      if (out.length === 2) break;
      const pic = draw(a.value, a, args.filter((o) => o !== a));
      if (!pic) continue;
      const what = { tree: "a tree", graph: "a graph", grid: "a grid", list: "a linked list", array: "an array" }[pic.dataset.kind];
      out.push(T.h("figure", { class: "st-figure" }, pic, T.h("figcaption", {}, T.h("code", {}, a.name), ` as ${what}`)));
    }
    return out;
  };
})();
