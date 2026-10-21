"use strict";
/* Topic drawings: each topic's data structure in SVG, built from a few primitives. Every part carries
   --i, its place in the build order, so the home hero can draw it in piece by piece. Colours come
   from the stage of whatever the drawing sits in (see .art in app.css). */
(function () {
  const T = window.Trace;
  const { s } = T;
  const W = 320, H = 200;

  let order = 0;
  const part = (...kids) => s("g", { style: `--i:${order++}` }, kids);
  const tone = (t) => (t ? " " + t : "");    // "hi" partner colour, "key" stage shade, "dim" faded

  // ── atoms ──────────────────────────────────────────────────────────────────
  const box = (x, y, w, h, label, t) => [
    s("rect", { x, y, width: w, height: h, rx: Math.min(9, w / 4), class: "a-cell" + tone(t) }),
    label == null ? null : s("text", { x: x + w / 2, y: y + h / 2, class: "a-label" + tone(t) }, label)];
  const cell = (x, y, w, h, label, t) => part(...box(x, y, w, h, label, t));
  const dot = (x, y, r, label, t) => [
    s("circle", { cx: x, cy: y, r, class: "a-cell" + tone(t) }),
    label == null ? null : s("text", { x, y, class: "a-label" + tone(t) }, label)];
  const node = (x, y, r, label, t) => part(...dot(x, y, r, label, t));
  const line = (x1, y1, x2, y2, t) => s("line", { x1, y1, x2, y2, class: "a-line" + tone(t) });
  function arrow(x1, y1, x2, y2, t) {
    const a = Math.atan2(y2 - y1, x2 - x1), k = 7;
    const head = [[x2, y2], [x2 - k * Math.cos(a - 0.45), y2 - k * Math.sin(a - 0.45)], [x2 - k * Math.cos(a + 0.45), y2 - k * Math.sin(a + 0.45)]];
    return [line(x1, y1, x2, y2, t), s("path", { d: "M" + head.map((p) => p.join(",")).join("L") + "Z", class: "a-head" + tone(t) })];
  }
  const note = (x, y, text, t) => s("text", { x, y, class: "a-note" + tone(t) }, text);
  // a point `gap` along the segment from (x1, y1) to (x2, y2): where an edge leaves a node's rim
  const along = (x1, y1, x2, y2, gap) => { const d = Math.hypot(x2 - x1, y2 - y1); return [x1 + ((x2 - x1) * gap) / d, y1 + ((y2 - y1) * gap) / d]; };
  const edge = (a, b, r, t) => { const [x1, y1] = along(a[0], a[1], b[0], b[1], r), [x2, y2] = along(b[0], b[1], a[0], a[1], r); return line(x1, y1, x2, y2, t); };
  const link = (a, b, r, t) => { const [x1, y1] = along(a[0], a[1], b[0], b[1], r), [x2, y2] = along(b[0], b[1], a[0], a[1], r + 2); return arrow(x1, y1, x2, y2, t); };

  // a row of equal cells; tones maps index -> tone
  function row(values, { x = null, y = 80, w = 34, h = 34, gap = 6, tones = {} } = {}) {
    const x0 = x ?? (W - (values.length * w + (values.length - 1) * gap)) / 2;
    return values.map((v, i) => cell(x0 + i * (w + gap), y, w, h, v, tones[i]));
  }
  const rowX = (n, { w = 34, gap = 6 } = {}) => (i) => (W - (n * w + (n - 1) * gap)) / 2 + i * (w + gap) + w / 2;

  // a tree from [label, parentIndex, x, y, tone] rows
  function tree(nodes, { r = 17, edgeTone = () => null } = {}) {
    const edges = nodes.map(([, p, x, y], i) => (p < 0 ? null : part(edge([nodes[p][2], nodes[p][3]], [x, y], r, edgeTone(i)))));
    return [...edges, ...nodes.map(([label, , x, y, t]) => node(x, y, r, label, t))];
  }
  const BIN = [[8, -1, 160, 34], [3, 0, 96, 92], [10, 0, 224, 92], [1, 1, 60, 152], [6, 1, 132, 152], [14, 2, 260, 152]];

  // ── primitives ─────────────────────────────────────────────────────────────
  const KINDS = {
    curves: () => [
      part(arrow(40, 176, 40, 20), arrow(40, 176, 296, 176)),
      part(s("path", { d: "M44 170 C 120 168, 200 150, 290 130", class: "a-curve" }), note(286, 120, "n log n")),
      part(s("path", { d: "M44 172 C 140 172, 220 168, 290 162", class: "a-curve key" }), note(286, 154, "n")),
      part(s("path", { d: "M44 172 C 110 168, 160 120, 200 28", class: "a-curve hi" }), note(206, 30, "n²", "hi")),
      part(note(150, 196, "input size"))],
    boxes: () => [
      ...row([3, 1, 4, 1, 5], { y: 40, tones: { 2: "hi" } }), part(note(160, 30, "list[2] = 4")),
      ...[["'a'", 1], ["'b'", 2]].map(([k, v], i) => part(...box(84, 108 + i * 42, 60, 32, k, "key"), arrow(148, 124 + i * 42, 182, 124 + i * 42), ...box(186, 108 + i * 42, 44, 32, v)))],
    array: () => {
      const vals = [1, 3, 4, 6, 8, 11, 15], x = rowX(7);
      return [...row(vals, { tones: { 0: "hi", 6: "hi" } }),
        part(arrow(x(0), 150, x(0), 120, "hi"), note(x(0), 166, "L", "hi")),
        part(arrow(x(6), 150, x(6), 120, "hi"), note(x(6), 166, "R", "hi")),
        part(note(160, 54, "1 + 15 = 16"))];
    },
    window: () => {
      const x = rowX(8);
      return [...row([2, 1, 5, 1, 3, 2, 6, 1], { tones: { 2: "key", 3: "key", 4: "key" } }),
        part(s("rect", { x: x(2) - 23, y: 72, width: x(4) - x(2) + 46, height: 50, rx: 14, class: "a-frame" })),
        part(note(x(3), 146, "sum = 9", "hi")), part(arrow(x(4) + 30, 60, x(5) + 6, 60, "hi"), note(x(4) + 20, 50, "slide"))];
    },
    prefix: () => {
      const vals = [3, 1, 4, 1, 5, 9], sums = [3, 4, 8, 9, 14, 23], x = rowX(6);
      return [...row(vals, { y: 44 }), part(note(24, 61, "a")),
        ...sums.map((v, i) => cell(x(i) - 17, 124, 34, 34, v, i === 4 ? "hi" : "key")), part(note(22, 141, "sum")),
        part(...vals.map((_, i) => arrow(x(i), 82, x(i), 120, "dim")))];
    },
    search: () => {
      const x = rowX(8);
      return [...row([2, 5, 8, 12, 16, 23, 38, 56], { tones: { 3: "hi" } }),
        part(note(x(0), 150, "lo")), part(note(x(3), 150, "mid", "hi"), arrow(x(3), 140, x(3), 120, "hi")), part(note(x(7), 150, "hi")),
        part(note(160, 60, "23 > 12, go right"))];
    },
    intervals: () => {
      const bars = [[30, 120, 40], [90, 190, 76], [170, 230, 112], [250, 300, 148]];
      return [part(arrow(24, 182, 300, 182)),
        ...bars.map(([a, b, y], i) => cell(a, y, b - a, 24, null, i === 1 || i === 2 ? "hi" : "key")),
        part(s("rect", { x: 82, y: 66, width: 156, height: 80, rx: 14, class: "a-frame" }), note(160, 160, "overlap: merge"))];
    },
    buckets: () => {
      const chains = [["cat"], [], ["ant", "owl"], ["bee"]];
      return [...chains.map((_, i) => cell(40, 26 + i * 40, 34, 32, i, "key")),
        ...chains.flatMap((c, i) => c.map((w, j) => part(arrow(78 + j * 92, 42 + i * 40, 104 + j * 92, 42 + i * 40), ...box(108 + j * 92, 26 + i * 40, 60, 32, w, j ? "hi" : null)))),
        part(note(230, 190, "hash(key) % 4"))];
    },
    calls: () => [0, 1, 2, 3].map((k) => cell(30 + k * 24, 22 + k * 36, 260 - k * 48, 150 - k * 36, null, k === 3 ? "hi" : k % 2 ? "key" : null))
      .concat([0, 1, 2, 3].map((k) => part(s("text", { x: 160, y: 38 + k * 36, class: "a-label" + (k === 3 ? " hi" : "") }, `fib(${4 - k})`)))),
    stack: () => [
      ...[["push 7", 7], [null, 4], [null, 9], [null, 2]].map(([, v], i) => cell(120, 40 + i * 38, 80, 32, v, i === 0 ? "hi" : null)),
      part(arrow(246, 20, 206, 54, "hi"), note(262, 18, "push", "hi")), part(note(84, 60, "top")),
      part(s("path", { d: "M112 34 V 196 H 208 V 34", class: "a-wall" }))],
    queue: () => [
      part(s("path", { d: "M44 72 H 276 M44 128 H 276", class: "a-wall" })),
      ...[5, 8, 2, 7, 3].map((v, i) => cell(62 + i * 42, 82, 34, 36, v, i === 0 ? "hi" : null)),
      part(arrow(56, 100, 14, 100, "hi"), note(30, 150, "out", "hi")), part(arrow(310, 100, 276, 100), note(292, 150, "in"))],
    linked: () => {
      const vals = [3, 7, 1, 9];
      return [...vals.map((v, i) => part(...box(10 + i * 70, 82, 46, 36, v, i === 1 ? "hi" : null),
        ...arrow(58 + i * 70, 100, 76 + i * 70, 100, i === 1 ? "hi" : null))),
        part(note(298, 101, "None")), part(note(33, 64, "head"))];
    },
    tree: () => tree(BIN.map((n, i) => [...n, i === 0 ? "key" : i === 4 ? "hi" : null])),
    bst: () => tree(BIN.map((n, i) => [...n, [0, 1, 4].includes(i) ? "hi" : null]), { edgeTone: (i) => (i === 1 || i === 4 ? "hi" : null) }).concat(part(note(214, 186, "find 6: left, then right"))),
    lift: () => {
      const nodes = [[0, -1, 160, 24], [1, 0, 160, 66], [2, 1, 160, 108], [3, 2, 160, 150], [4, 3, 160, 192 - 14]];
      return [...tree(nodes.map((n, i) => [...n, i === 4 ? "hi" : i === 2 ? "key" : null]), { r: 13 }),
        part(s("path", { d: "M176 176 C 236 160, 236 120, 176 110", class: "a-curve hi" }), note(250, 146, "2¹", "hi")),
        part(s("path", { d: "M144 176 C 60 160, 60 50, 144 30", class: "a-curve key" }), note(56, 104, "2²"))];
    },
    heap: () => [
      ...tree([[1, -1, 160, 26, "hi"], [3, 0, 104, 76], [2, 0, 216, 76], [7, 1, 74, 126], [4, 1, 134, 126]], { r: 16 }),
      ...row([1, 3, 2, 7, 4], { y: 160, w: 30, h: 28, tones: { 0: "hi" } })],
    trie: () => tree([["", -1, 160, 22, "key"], ["c", 0, 104, 70], ["d", 0, 226, 70], ["a", 1, 104, 120], ["o", 2, 226, 120],
      ["t", 3, 64, 172, "hi"], ["r", 3, 144, 172, "hi"], ["g", 4, 226, 172, "hi"]], { r: 16 }),
    graph: () => {
      const P = [[160, 100], [96, 52], [228, 52], [86, 156], [236, 150], [40, 100], [292, 100]];
      const E = [[0, 1], [0, 2], [0, 3], [0, 4], [1, 5], [3, 5], [2, 6], [4, 6]];
      return [part(s("circle", { cx: 160, cy: 100, r: 86, class: "a-ring" })),
        ...E.map(([a, b]) => part(edge(P[a], P[b], 17, a === 0 ? "key" : null))),
        ...P.map(([x, y], i) => node(x, y, 17, i, i === 0 ? "hi" : i <= 4 ? "key" : null))];
    },
    dag: () => {
      const P = [[40, 60], [40, 150], [128, 100], [214, 50], [214, 150], [292, 100]];
      const E = [[0, 2], [1, 2], [2, 3], [2, 4], [3, 5], [4, 5]];
      return [...E.map(([a, b]) => part(link(P[a], P[b], 17))),
        ...P.map(([x, y], i) => node(x, y, 17, String.fromCharCode(65 + i), i < 2 ? "hi" : null))];
    },
    weighted: () => {
      const P = [[40, 100], [130, 40], [130, 160], [226, 70], [290, 150]];
      const E = [[0, 1, 4, "hi"], [0, 2, 1], [2, 1, 2], [1, 3, 5, "hi"], [2, 4, 8], [3, 4, 3, "hi"]];
      return [...E.map(([a, b, w, t]) => part(edge(P[a], P[b], 17, t),
        note((P[a][0] + P[b][0]) / 2 + 8, (P[a][1] + P[b][1]) / 2 - 6, w, t))),
        ...P.map(([x, y], i) => node(x, y, 17, String.fromCharCode(65 + i), i === 0 || i === 4 ? "hi" : null))];
    },
    flow: () => {
      const P = [[36, 100], [130, 44], [130, 156], [226, 44], [226, 156], [292, 100]];
      const E = [[0, 1, "3/4"], [0, 2, "2/2"], [1, 3, "3/3"], [2, 4, "2/5"], [1, 4, "0/2"], [3, 5, "3/3"], [4, 5, "2/6"]];
      return [...E.map(([a, b, c]) => part(link(P[a], P[b], 17, c.startsWith("0") ? "dim" : "key"),
        note((P[a][0] + P[b][0]) / 2, (P[a][1] + P[b][1]) / 2 - 7, c))),
        ...P.map(([x, y], i) => node(x, y, 17, i === 0 ? "s" : i === 5 ? "t" : i, i === 0 || i === 5 ? "hi" : null))];
    },
    decisions: () => [
      ...tree([["{}", -1, 160, 24, "key"], ["1", 0, 92, 82], ["–", 0, 228, 82], ["1,2", 1, 52, 146, "hi"], ["1", 1, 128, 146], ["2", 2, 196, 146], ["–", 2, 262, 146, "dim"]], { r: 19 }),
      part(note(262, 186, "pruned", "dim")), part(note(52, 186, "found", "hi"))],
    dp_row: () => {
      const x = rowX(7);
      return [...row([1, 1, 2, 3, 5, 8, "?"], { tones: { 4: "key", 5: "key", 6: "hi" } }),
        part(s("path", { d: `M${x(4)} 74 C ${x(4) + 10} 40, ${x(6) - 20} 40, ${x(6) - 4} 70`, class: "a-curve key" })),
        part(s("path", { d: `M${x(5)} 122 C ${x(5) + 8} 140, ${x(6) - 8} 140, ${x(6) - 4} 122`, class: "a-curve key" })),
        part(note(160, 170, "dp[i] = dp[i-1] + dp[i-2]"))];
    },
    grid: () => {
      const g = [[1, 3, 1, 2], [1, 5, 1, 4], [4, 2, 1, 3], [2, 1, 6, 1]];
      const path = new Set(["0,0", "1,0", "1,1", "2,1", "2,2", "3,2", "3,3"]);
      return g.flatMap((r, i) => r.map((v, j) => cell(84 + j * 40, 18 + i * 42, 36, 36, v, path.has(`${j},${i}`) ? "hi" : null)));
    },
    bits: () => {
      const a = [1, 0, 1, 1, 0, 1, 0, 0], m = [0, 0, 0, 0, 0, 1, 0, 0];
      const at = { x: 48, w: 28, gap: 5 };
      return [...row(a, { ...at, y: 30, tones: { 5: "key" } }), part(note(28, 44, "x")),
        ...row(m, { ...at, y: 76, tones: { 5: "key" } }), part(note(28, 90, "&")),
        ...row(a.map((b, i) => b & m[i]), { ...at, y: 132, tones: { 5: "hi" } }), part(note(178, 186, "is bit 2 set? yes"))];
    },
    segments: () => tree([["0–7", -1, 160, 26, "key"], ["0–3", 0, 90, 82], ["4–7", 0, 230, 82, "hi"], ["0–1", 1, 52, 146], ["2–3", 1, 128, 146, "hi"]], { r: 22 })
      .concat(part(note(230, 146, "sum(2, 7)", "hi"))),
    text: () => {
      const t = "abacabcab".split(""), x = rowX(9, { w: 28, gap: 4 });
      return [...row(t, { y: 52, w: 28, gap: 4, tones: { 4: "hi", 5: "hi", 6: "hi" } }),
        ...["a", "b", "c"].map((c, i) => cell(x(4 + i) - 14, 124, 28, 34, c, "key")),
        part(...[4, 5, 6].map((i) => line(x(i), 90, x(i), 120, "dim"))), part(note(160, 186, "match at 4"))];
    },
    numbers: () => {
      const prime = (n) => n > 1 && [...Array(n).keys()].slice(2).every((d) => n % d);
      return Array.from({ length: 24 }, (_, k) => k + 2).map((n, k) =>
        cell(40 + (k % 8) * 31, 34 + Math.floor(k / 8) * 44, 27, 34, n, prime(n) ? "hi" : "dim"));
    },
    hull: () => {
      const P = [[50, 120], [96, 40], [190, 30], [276, 84], [258, 168], [120, 176], [140, 100], [196, 120], [110, 130], [220, 70]];
      return [part(s("path", { d: "M50 120 L96 40 L190 30 L276 84 L258 168 L120 176 Z", class: "a-hull" })),
        ...P.map(([x, y], i) => node(x, y, 7, null, i < 6 ? "hi" : null))];
    },
    string: () => {
      const x = rowX(5, { w: 40, gap: 6 });
      return [...[0, 1, 2, 3, 4].map((i) => part(note(x(i), 52, i, "dim"))),
        ...row(["t", "r", "a", "c", "e"], { y: 66, w: 40, gap: 6, tones: { 1: "hi", 2: "hi", 3: "hi" } }),
        part(s("path", { d: `M${x(1) - 20} 120 v 10 H ${x(3) + 20} v -10`, class: "a-wall" })),
        part(note(160, 154, "s[1:4] → 'rac'", "hi"))];
    },
    coins: () => [
      part(note(160, 20, "make 41 with the fewest coins")),
      ...[[25, 26, 60], [10, 20, 132], [5, 16, 194], [1, 12, 246]].map(([v, r, x]) => node(x, 82, r, v, "hi")),
      part(...arrow(160, 120, 160, 146)),
      part(note(160, 168, "41 = 25 + 10 + 5 + 1")), part(note(160, 190, "take the biggest coin that fits", "dim"))],
    triangle: () => {
      const n = 5, c = 30, x0 = 86, y0 = 22;
      const cells = [];
      for (let i = 0; i < n; i++) for (let j = i; j < n; j++)
        cells.push(cell(x0 + j * (c + 4), y0 + i * (c + 4), c, c, i === j ? 1 : i === 0 && j === n - 1 ? "?" : "", i === j ? "key" : i === 0 && j === n - 1 ? "hi" : null));
      return [...cells, part(note(118, 178, "dp[i][j] from shorter ranges"))];
    },
    negcycle: () => {
      const P = [[44, 100], [130, 46], [236, 46], [236, 154], [130, 154]];
      const E = [[0, 1, 3], [1, 2, 2, "hi"], [2, 3, -4, "hi"], [3, 4, 1, "hi"], [4, 1, 0, "hi"]];
      return [...E.map(([a, b, w, t]) => part(link(P[a], P[b], 17, t), note((P[a][0] + P[b][0]) / 2 + 10, (P[a][1] + P[b][1]) / 2 - 8, w, t))),
        ...P.map(([x, y], i) => node(x, y, 17, String.fromCharCode(65 + i), i === 0 ? "key" : null)),
        part(note(184, 102, "loop: −1", "hi"))];
    },
    digits: () => [
      part(note(160, 16, "count numbers ≤ 4072")),
      ...[4, 0, 7, 2].map((d, i) => cell(70 + i * 46, 34, 40, 44, d, i === 0 ? "hi" : "key")),
      part(...arrow(90, 84, 70, 124), ...box(36, 128, 68, 32, "0–3", null), note(70, 180, "free")),
      part(...arrow(90, 84, 170, 124, "hi"), ...box(140, 128, 60, 32, "4", "hi"), note(170, 180, "tight", "hi"))],
  };

  T.ART_KINDS = {
    1: "curves", 2: "boxes", 3: "string", 4: "buckets", 5: "calls", 6: "array", 7: "window", 8: "prefix", 9: "search",
    10: "intervals", 11: "coins", 12: "stack", 13: "queue", 14: "linked", 15: "tree", 16: "bst", 17: "heap", 18: "trie",
    19: "graph", 20: "dag", 21: "weighted", 22: "decisions", 23: "dp_row", 24: "grid", 25: "bits", 26: "segments",
    27: "text", 28: "triangle", 29: "negcycle", 30: "numbers", 31: "hull", 32: "lift", 33: "flow", 34: "digits",
  };

  // Trim a drawing's viewBox to what it actually draws (it must be in the document to be measured),
  // so it fills whatever box it's given. Measure before any build-in starts: parts begin moved and shrunk.
  T.cropArt = (svg, pad = 10) => {
    if (!svg || !svg.isConnected) return svg;
    const b = svg.getBBox();
    if (b.width && b.height) svg.setAttribute("viewBox", `${b.x - pad} ${b.y - pad} ${b.width + 2 * pad} ${b.height + 2 * pad}`);
    return svg;
  };

  T.topicArt = (n) => {
    order = 0;
    const kind = T.ART_KINDS[n] || "graph";
    return s("svg", { class: "art", viewBox: `0 0 ${W} ${H}`, "aria-hidden": "true", "data-kind": kind }, KINDS[kind]());
  };
})();
