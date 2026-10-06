"use strict";
(function () {
  const T = window.Trace;
  const { h, V } = T;
  const STAGE = "Graphs and search";

  // Random planar-ish graph: jittered 2-row (or 3-row) grid, non-crossing candidate edges,
  // a random spanning tree plus some extras. Labels are shuffled so alphabetical order isn't positional.
  function makeGraph(n, { extra = 0.35, weighted = false } = {}) {
    const rows = n <= 8 ? 2 : 3, cols = Math.ceil(n / rows);
    let slots = [];
    for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) slots.push({ r, c });
    slots = T.shuffle(slots).slice(0, n);
    const at = new Map(slots.map((p, i) => [`${p.r},${p.c}`, i]));
    const cand = [];
    for (const { r, c } of slots) {
      const i = at.get(`${r},${c}`);
      const right = at.get(`${r},${c + 1}`), down = at.get(`${r + 1},${c}`);
      if (right != null) cand.push([i, right]);
      if (down != null) cand.push([i, down]);
      if (Math.random() < 0.5) { const d = at.get(`${r + 1},${c + 1}`); if (d != null) cand.push([i, d]); }
      else { const a = at.get(`${r},${c + 1}`), b = at.get(`${r + 1},${c}`); if (a != null && b != null && !cand.some(([x, y]) => (x === a && y === b) || (x === b && y === a))) cand.push([a, b]); }
    }
    // union-find for a spanning tree
    const par = T.range(n);
    const find = (x) => (par[x] === x ? x : (par[x] = find(par[x])));
    const chosen = [];
    for (const [a, b] of T.shuffle(cand)) {
      const ra = find(a), rb = find(b);
      if (ra !== rb) { par[ra] = rb; chosen.push([a, b]); }
      else if (Math.random() < extra) chosen.push([a, b]);
    }
    const comps = new Set(T.range(n).map(find));
    if (comps.size > 1) return makeGraph(n, { extra, weighted });
    const labels = T.shuffle(T.letters.slice(0, n).split(""));
    const jit = () => (Math.random() - 0.5) * 0.14;
    const nodes = slots.map((p, i) => ({
      id: labels[i],
      x: Math.min(1, Math.max(0, (cols === 1 ? 0.5 : p.c / (cols - 1)) + jit())),
      y: Math.min(1, Math.max(0, (rows === 1 ? 0.5 : p.r / (rows - 1)) + jit())),
    }));
    const edges = chosen.map(([a, b]) => ({ a: labels[a], b: labels[b], w: weighted ? T.rand(1, 9) : null }));
    return { nodes, edges };
  }
  const neighbors = (g, x) => g.edges.filter((e) => e.a === x || e.b === x).map((e) => ({ v: e.a === x ? e.b : e.a, w: e.w, e })).sort((p, q) => p.v.localeCompare(q.v));
  T.makeGraph = makeGraph;

  // ── 19 Graph traversal ───────────────────────────────────────────────────
  function gridInstance() {
    for (;;) {
      const R = 6, C = 7;
      const wall = Array.from({ length: R }, () => Array.from({ length: C }, () => Math.random() < 0.24));
      const sr = T.rand(0, R - 1), sc = T.rand(0, C - 1);
      wall[sr][sc] = false;
      const dist = Array.from({ length: R }, () => Array(C).fill(-1));
      dist[sr][sc] = 0;
      const q = [[sr, sc]];
      while (q.length) {
        const [r, c] = q.shift();
        for (const [dr, dc] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
          const nr = r + dr, nc = c + dc;
          if (nr < 0 || nc < 0 || nr >= R || nc >= C || wall[nr][nc] || dist[nr][nc] >= 0) continue;
          dist[nr][nc] = dist[r][c] + 1;
          q.push([nr, nc]);
        }
      }
      const reach = dist.flat().filter((d) => d >= 0).length;
      const maxD = Math.max(...dist.flat());
      if (reach >= 14 && maxD >= 5) return { R, C, wall, dist, sr, sc, maxD };
    }
  }

  T.topic({
    id: "graph-traversal", n: 19, stage: STAGE,
    title: "Graph traversal",
    idea: "BFS spreads like a ripple: everything 1 step away, then everything 2 steps away. That's why it finds shortest paths in unweighted graphs. DFS dives down one path until it can't go further, then backs up: good for \"is it connected\", islands and cycles.",
    signals: "Grids, mazes, networks, islands, \"minimum number of moves\" (BFS), or \"explore everything reachable\" (either one).",
    invariant: "BFS: the queue holds at most two neighbouring distances, d and d + 1. Every node gets marked visited once, when it's first discovered.",
    drills: [
      {
        id: "ripple", name: "Draw the ripple",
        blurb: "BFS from S. Moves go up, down, left and right (no diagonals), and dark cells are walls. Click every cell in the next ring, in any order.",
        *play(ctx) {
          const g = gridInstance();
          const known = new Set([`${g.sr},${g.sc}`]);
          const rings = Math.min(4, g.maxD - 1);
          const draw = (d) => ctx.draw(V.grid(g.R, g.C, (r, c) => {
            const k = `${r},${c}`;
            if (g.wall[r][c]) return { cls: "wall" };
            if (r === g.sr && c === g.sc) return { t: "S", cls: "src" };
            if (known.has(k)) return { t: g.dist[r][c], cls: g.dist[r][c] === d - 1 ? "d0" : "ok" };
            return { pick: k };
          }, { cls: "big" }));
          for (let d = 1; d <= rings; d++) {
            const ring = [];
            for (let r = 0; r < g.R; r++) for (let c = 0; c < g.C; c++) if (g.dist[r][c] === d) ring.push(`${r},${c}`);
            while (ring.some((k) => !known.has(k))) {
              draw(d);
              const left = ring.filter((k) => !known.has(k));
              const v = yield T.ask({
                prompt: `Ring ${d}: ${left.length} cell${left.length > 1 ? "s" : ""} left to find.`,
                picks: true,
                answer: left,
                why: (k) => {
                  const [r, c] = k.split(",").map(Number);
                  const dd = g.dist[r][c];
                  if (dd < 0) return "Walls cut that cell off from S. It's never reached.";
                  return `That cell is ${dd} steps from S. Ring ${d} cells are the unvisited cells next to ring ${d - 1}.`;
                },
              });
              known.add(v);
            }
          }
          const far = [];
          for (let r = 0; r < g.R; r++) for (let c = 0; c < g.C; c++) if (g.dist[r][c] > rings) far.push([r, c]);
          const [tr, tc] = T.pick(far.filter(([r, c]) => g.dist[r][c] === Math.max(...far.map(([a, b]) => g.dist[a][b]))));
          ctx.draw(V.grid(g.R, g.C, (r, c) => {
            if (g.wall[r][c]) return { cls: "wall" };
            if (r === g.sr && c === g.sc) return { t: "S", cls: "src" };
            if (r === tr && c === tc) return { t: "T", cls: "target" };
            if (known.has(`${r},${c}`)) return { t: g.dist[r][c], cls: "ok" };
            return {};
          }, { cls: "big" }));
          const dT = g.dist[tr][tc];
          yield T.choose("Keep the ripple going in your head. How many steps from S to T?", T.numOptions(dT, { spread: 3, min: 1 }), dT,
            `Continue the rings past ${rings}. T is first reached in ring ${dT}, which is its shortest distance.`, `${dT}: the ring number is the shortest distance.`);
          return { summary: "The ring a cell first appears in is its shortest distance. That's BFS's whole guarantee, as long as every edge costs the same." };
        },
      },
      {
        id: "order", name: "BFS or DFS order",
        blurb: "Visit the graph from the start node. Neighbours are always tried in alphabetical order. Click the nodes in the order they're visited.",
        *play(ctx) {
          const g = makeGraph(7, { extra: 0.3 });
          const start = T.pick(g.nodes).id;
          const mode = T.pick(["bfs", "dfs"]);
          const order = [];
          if (mode === "bfs") {
            const seen = new Set([start]), q = [start];
            while (q.length) { const x = q.shift(); order.push(x); for (const { v } of neighbors(g, x)) if (!seen.has(v)) { seen.add(v); q.push(v); } }
          } else {
            const seen = new Set();
            (function dfs(x) { seen.add(x); order.push(x); for (const { v } of neighbors(g, x)) if (!seen.has(v)) dfs(v); })(start);
          }
          for (let k = 0; k < order.length; k++) {
            const done = order.slice(0, k);
            ctx.draw(V.line(h("strong", {}, mode === "bfs" ? "Breadth-first (queue)" : "Depth-first (recursion)"), `   start at ${start}`),
              V.graph(g, { pickNodes: (id) => !done.includes(id), ncls: (id) => (done.includes(id) ? "ok" : ""), badge: (id) => (done.includes(id) ? done.indexOf(id) + 1 : null) }),
              V.line("visited: ", V.k(done.join(" ") || "nothing yet")));
            yield T.click(k === 0 ? "Click the first node visited." : "Next node visited?", order[k],
              mode === "bfs" ? "BFS finishes every node at distance d before any node at distance d + 1, and nodes join the queue in alphabetical order of discovery."
                : "DFS goes as deep as it can: from the latest node, take its first unvisited neighbour alphabetically. Back up only when there's none left.");
          }
          return { summary: mode === "bfs" ? "BFS fans out by distance. Use it for shortest steps." : "DFS commits to a path and backtracks. Use it to explore or detect structure." };
        },
      },
      {
        id: "islands", name: "Count the islands",
        blurb: "Land cells that touch up, down, left or right form one island. Diagonal contact doesn't count.",
        *play(ctx) {
          for (let round = 0; round < 3; round++) {
            const R = 5, C = 7;
            const land = Array.from({ length: R }, () => Array.from({ length: C }, () => Math.random() < 0.42));
            const seen = Array.from({ length: R }, () => Array(C).fill(-1));
            let count = 0, diagTouch = false;
            for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) {
              if (!land[r][c] || seen[r][c] >= 0) continue;
              const st = [[r, c]];
              seen[r][c] = count;
              while (st.length) {
                const [a, b] = st.pop();
                for (const [dr, dc] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) {
                  const x = a + dr, y = b + dc;
                  if (x >= 0 && y >= 0 && x < R && y < C && land[x][y] && seen[x][y] < 0) { seen[x][y] = count; st.push([x, y]); }
                }
              }
              count++;
            }
            for (let r = 0; r + 1 < R; r++) for (let c = 0; c + 1 < C; c++) {
              if (land[r][c] && land[r + 1][c + 1] && seen[r][c] !== seen[r + 1][c + 1]) diagTouch = true;
              if (land[r][c + 1] && land[r + 1][c] && seen[r][c + 1] !== seen[r + 1][c]) diagTouch = true;
            }
            ctx.draw(V.grid(R, C, (r, c) => ({ cls: land[r][c] ? "land" : "" }), { cls: "big" }));
            yield T.choose("How many islands?", T.numOptions(count, { spread: 2, min: 1 }), count,
              `Flood each new piece of land and count the floods. ${diagTouch ? "Careful: some cells only touch diagonally, and they're separate islands." : ""}`);
            ctx.draw(V.grid(R, C, (r, c) => ({ t: land[r][c] ? seen[r][c] + 1 : "", cls: land[r][c] ? "land" : "" }), { cls: "big" }));
            if (round < 2) yield T.choose(`${count} islands, numbered by discovery order.`, [["go", "Next map"]], "go");
          }
          return { summary: "Scan every cell. Each unvisited land cell starts a new island, and a flood marks the whole island so it's never counted twice." };
        },
      },
    ],
  });

  // ── 20 Topological sort and union-find ───────────────────────────────────
  function dagInstance() {
    const n = T.rand(6, 7);
    const order = T.shuffle(T.letters.slice(0, n).split(""));
    const edges = [];
    for (let j = 1; j < n; j++) {
      const parents = T.sample(T.range(j), Math.min(j, T.rand(1, 2)));
      for (const i of parents) edges.push({ a: order[i], b: order[j] });
    }
    const cyclic = Math.random() < 0.25;
    if (cyclic) {
      const j = T.rand(2, n - 1), i = T.rand(0, j - 1);
      edges.push({ a: order[j], b: order[i] });
    }
    // layer by longest path from sources (ignoring the back edge) for layout
    const layer = {};
    for (const x of order) layer[x] = 0;
    for (const x of order) for (const e of edges) if (e.a === x && order.indexOf(e.b) > order.indexOf(x)) layer[e.b] = Math.max(layer[e.b], layer[x] + 1);
    const maxL = Math.max(...Object.values(layer));
    const byLayer = {};
    for (const x of order) (byLayer[layer[x]] ||= []).push(x);
    const nodes = order.map((x) => {
      const col = byLayer[layer[x]];
      return { id: x, x: maxL ? layer[x] / maxL : 0.5, y: col.length === 1 ? 0.5 : col.indexOf(x) / (col.length - 1) };
    });
    return { nodes, edges, cyclic };
  }

  T.topic({
    id: "topo-union-find", n: 20, stage: STAGE,
    title: "Topological sort and union-find",
    idea: "Topological sort: repeatedly take something with no unfinished prerequisites. If you get stuck before taking everything, there's a cycle. Union-find: every group has one representative (its root). Two items are connected exactly when they have the same root.",
    signals: "Prerequisites, build orders, \"can all courses be finished\" (topological sort), or connectivity questions arriving one edge at a time, redundant edges, and counting groups (union-find).",
    invariant: "Kahn's algorithm only ever takes nodes with no incoming edges from unfinished nodes. In union-find, every node's parent chain ends at its group's root.",
    drills: [
      {
        id: "kahn", name: "Take what's ready",
        blurb: "An arrow X → Y means X must come before Y. Repeatedly click any course whose prerequisites are all done.",
        *play(ctx) {
          const g = dagInstance();
          const done = [];
          for (;;) {
            const left = g.nodes.map((x) => x.id).filter((x) => !done.includes(x));
            if (!left.length) break;
            const waits = (x) => g.edges.filter((e) => e.b === x && !done.includes(e.a)).map((e) => e.a);
            const ready = left.filter((x) => waits(x).length === 0);
            ctx.draw(V.graph(g, { directed: true, W: 540, H: 280, pickNodes: (id) => !done.includes(id), ncls: (id) => (done.includes(id) ? "dim" : ""), ecls: (e) => (done.includes(e.a) ? "dim" : ""), badge: (id) => (done.includes(id) ? done.indexOf(id) + 1 : null) }),
              V.line("order so far: ", V.k(done.join(" → ") || "nothing yet")));
            const v = yield T.ask({
              prompt: "Click a course that's ready, or…",
              picks: true, options: [["stuck", "Stuck: everything left waits on something"]],
              answer: ready.length ? ready : "stuck",
              why: (v) => (v === "stuck" ? `${ready[0]} has no unfinished prerequisites. It's ready.` : `${v} still waits on ${waits(v).join(" and ")}.`),
            });
            if (!ready.length) {
              ctx.draw(V.graph(g, { directed: true, W: 540, H: 280, ncls: (id) => (done.includes(id) ? "dim" : "bad"), ecls: (e) => (done.includes(e.a) ? "dim" : "") }));
              return { summary: `Stuck with ${left.join(", ")} left: they wait on each other in a cycle. Fewer than n nodes taken means a cycle.` };
            }
            done.push(v);
          }
          return { summary: "Any order that only ever takes ready nodes is valid. In code: a queue of nodes whose in-degree has dropped to 0." };
        },
      },
      {
        id: "uf", name: "Union by size",
        blurb: "Each tree is one group, and its root names the group. union(a, b) hangs the smaller tree under the bigger tree's root. (No path compression here, to keep the trees visible.)",
        *play(ctx) {
          const ids = T.letters.slice(0, 8).split("");
          const parent = Object.fromEntries(ids.map((x) => [x, x]));
          const size = Object.fromEntries(ids.map((x) => [x, 1]));
          const root = (x) => (parent[x] === x ? x : root(parent[x]));
          const kids = (x) => ids.filter((y) => parent[y] === x && y !== x);
          const draw = (hot = []) => ctx.draw(V.ntree(ids.filter((x) => parent[x] === x), {
            kids: (x) => kids(x).map((y) => y), label: (x) => x, key: (x) => x, pick: () => true,
            cls: (x) => (hot.includes(x) ? "hot" : parent[x] === x ? "pa" : ""), badge: (x) => (parent[x] === x && size[x] > 1 ? size[x] : null), gap: 46,
          }));
          for (let step = 0; step < 7; step++) {
            const a = T.pick(ids), b = T.pick(ids.filter((y) => y !== a));
            const ra = root(a), rb = root(b);
            if (step > 1 && Math.random() < 0.3) {
              draw([a, b]);
              yield T.choose(`connected(${a}, ${b})?`, [["yes", "Yes, same group"], ["no", "No"]], ra === rb ? "yes" : "no",
                `Follow parents up: ${a} → ${ra}, ${b} → ${rb}. ${ra === rb ? "Same" : "Different"} root.`);
              continue;
            }
            draw([a, b]);
            yield T.click(`union(${a}, ${b}). First, click ${a}'s root.`, ra, `Follow parent links up from ${a} until a node is its own parent.`, `root(${a}) = ${ra}`);
            yield T.click(`Now click ${b}'s root.`, rb, `Follow parent links up from ${b} until a node is its own parent.`, `root(${b}) = ${rb}`);
            if (ra === rb) {
              yield T.choose("Same root. So:", [["same", "Already connected: do nothing"], ["link", "Link them anyway"]], "same", "Linking a root to itself would create a cycle. They're already one group.");
              continue;
            }
            const ans = size[ra] > size[rb] ? "rb" : size[ra] < size[rb] ? "ra" : ["ra", "rb"];
            const v = yield T.choose(`Sizes: ${ra} has ${size[ra]}, ${rb} has ${size[rb]}.`, [["ra", `${ra} goes under ${rb}`], ["rb", `${rb} goes under ${ra}`]], ans,
              "Hang the smaller tree under the bigger root. Only the smaller group's nodes get one step deeper, which keeps trees about log n tall.",
              size[ra] === size[rb] ? "Equal sizes: either way works." : null);
            const [child, par] = v === "ra" ? [ra, rb] : [rb, ra];
            parent[child] = par;
            size[par] += size[child];
          }
          draw();
          return { summary: "Two operations: find (walk up to the root) and union (link roots). Add path compression and both become nearly O(1)." };
        },
      },
    ],
  });

  // ── 21 Weighted graphs ───────────────────────────────────────────────────
  T.topic({
    id: "weighted", n: 21, stage: STAGE,
    title: "Weighted graphs",
    idea: "Dijkstra: always settle the closest unsettled node. With no negative edges, nothing found later can beat it. Kruskal: take edges cheapest first, skipping any that would close a loop.",
    signals: "Cheapest or fastest route (Dijkstra), connecting everything at minimum total cost (MST), or network delay.",
    invariant: "Dijkstra: a settled node's distance is final. Kruskal: the chosen edges never form a cycle.",
    drills: [
      {
        id: "dijkstra", name: "Settle the closest",
        blurb: "Shortest distances from the source. Badges are the best distances known so far. Each step, settle a node, then improve its neighbours.",
        *play(ctx) {
          const g = makeGraph(T.rand(6, 7), { extra: 0.45, weighted: true });
          const src = T.pick(g.nodes).id;
          const dist = Object.fromEntries(g.nodes.map((x) => [x.id, Infinity]));
          dist[src] = 0;
          const settled = [];
          let changed = [];
          const fmt = (d) => (d === Infinity ? "∞" : d);
          for (;;) {
            const open = g.nodes.map((x) => x.id).filter((x) => !settled.includes(x) && dist[x] < Infinity);
            if (!open.length) break;
            const min = Math.min(...open.map((x) => dist[x]));
            ctx.draw(V.graph(g, { pickNodes: () => true, ncls: (id) => (settled.includes(id) ? "ok" : changed.includes(id) ? "pa" : ""), badge: (id) => fmt(dist[id]), ecls: () => "" }),
              V.line(`source ${src}   settled: ${settled.join(" ") || "none yet"}`));
            const u = yield T.ask({
              prompt: "Click the node to settle next.",
              picks: true,
              answer: open.filter((x) => dist[x] === min),
              why: (v) => {
                if (settled.includes(v)) return `${v} is already settled. Its distance is final.`;
                if (dist[v] === Infinity) return `There's no known path to ${v} yet.`;
                const best = open.find((x) => dist[x] === min);
                return `${v} is at ${dist[v]}, but ${best} is closer at ${min}. Settle the closest first. No other route can undercut it, because every edge adds a positive cost.`;
              },
            });
            settled.push(u);
            const improve = neighbors(g, u).filter(({ v, w }) => !settled.includes(v) && dist[u] + w < dist[v]);
            changed = [];
            if (improve.length) {
              const { v, w } = improve[0];
              ctx.draw(V.graph(g, { ncls: (id) => (settled.includes(id) ? "ok" : id === v ? "hot" : ""), badge: (id) => fmt(dist[id]), ecls: (e) => ((e.a === u && e.b === v) || (e.a === v && e.b === u) ? "hot" : "") }),
                V.line(`source ${src}   settled: ${settled.join(" ")}`));
              const nd = dist[u] + w;
              yield T.choose(`${u} is settled at ${dist[u]}. Through ${u}, what's the new best distance to ${v}?`, T.numOptions(nd, { spread: 3, min: 1, extra: [w] }), nd,
                `Distance to ${u} plus the edge: ${dist[u]} + ${w}.${dist[v] < Infinity ? ` It beats the old ${dist[v]}.` : ""}`,
                improve.length > 1 ? `Also improved: ${improve.slice(1).map((x) => `${x.v} → ${dist[u] + x.w}`).join(", ")}.` : null);
              for (const x of improve) { dist[x.v] = dist[u] + x.w; changed.push(x.v); }
            }
          }
          ctx.draw(V.graph(g, { ncls: () => "ok", badge: (id) => fmt(dist[id]) }), V.line(`Shortest distances from ${src}.`));
          return { summary: "A min-heap keyed by distance hands you the closest node in O(log n). Stale heap entries just get skipped." };
        },
      },
      {
        id: "kruskal", name: "Cheapest safe edge",
        blurb: "Connect every node with the least total weight. Go through the edges from cheapest to most expensive. Take an edge unless its two ends are already connected.",
        *play(ctx) {
          const g = makeGraph(T.rand(6, 7), { extra: 0.6, weighted: true });
          const edges = g.edges.slice().sort((p, q) => p.w - q.w);
          const par = Object.fromEntries(g.nodes.map((x) => [x.id, x.id]));
          const find = (x) => (par[x] === x ? x : find(par[x]));
          const taken = [], skipped = [];
          const tones = ["pa", "pb", "pc", "pd"];
          for (const e of edges) {
            if (taken.length === g.nodes.length - 1) break;
            const roots = [...new Set(g.nodes.map((x) => find(x.id)))];
            const comp = (id) => {
              const r = find(id);
              const size = g.nodes.filter((x) => find(x.id) === r).length;
              return size > 1 ? tones[roots.indexOf(r) % 4] : "";
            };
            ctx.draw(V.graph(g, { ncls: comp, ecls: (x) => (x === e ? "hot" : taken.includes(x) ? "on" : skipped.includes(x) ? "dim" : "") }),
              V.line(`total so far: ${taken.reduce((s, x) => s + x.w, 0)}   edges taken: ${taken.length} of ${g.nodes.length - 1}`));
            const same = find(e.a) === find(e.b);
            yield T.choose(`Next cheapest: ${e.a}–${e.b} (weight ${e.w}).`, [["take", "Take it"], ["skip", "Skip: it would close a loop"]], same ? "skip" : "take",
              same ? `${e.a} and ${e.b} are already joined by edges you've taken. This one would only add a loop.` : `${e.a} and ${e.b} are in different pieces. This is the cheapest way left to join them.`);
            if (same) skipped.push(e);
            else { taken.push(e); par[find(e.a)] = find(e.b); }
          }
          const total = taken.reduce((s, x) => s + x.w, 0);
          ctx.draw(V.graph(g, { ncls: () => "ok", ecls: (x) => (taken.includes(x) ? "on" : "dim") }), V.line("Minimum spanning tree weight: ", h("strong", {}, total)));
          return { summary: "Union-find answers \"already connected?\" in Kruskal. That's the reason union-find exists." };
        },
      },
    ],
  });

  // ── 22 Backtracking ──────────────────────────────────────────────────────
  function queensInstance() {
    for (let tries = 0; tries < 400; tries++) {
      const n = Math.random() < 0.5 ? 4 : 5;
      const blocked = new Set();
      const holes = n === 4 ? T.rand(0, 1) : T.rand(2, 3);
      while (blocked.size < holes) blocked.add(`${T.rand(0, n - 1)},${T.rand(0, n - 1)}`);
      // simulate the systematic search and count decisions
      const qs = [], tried = Array(n).fill(-1);
      let r = 0, steps = 0, ok = false;
      const safe = (row, col) => !blocked.has(`${row},${col}`) && qs.every(([qr, qc]) => qc !== col && Math.abs(qr - row) !== Math.abs(qc - col));
      while (steps < 80) {
        if (r === n) { ok = true; break; }
        let c = tried[r] + 1;
        while (c < n && !safe(r, c)) c++;
        steps++;
        if (c < n) { qs.push([r, c]); tried[r] = c; r++; }
        else { if (r === 0) break; tried[r] = -1; r--; qs.pop(); }
      }
      if (ok && steps >= 7 && steps <= 22) return { n, blocked };
    }
    return { n: 4, blocked: new Set() };
  }

  const catalan = (n) => { let c = 1; for (let i = 0; i < n; i++) c = (c * 2 * (2 * i + 1)) / (i + 2); return c; };
  const fact = (n) => (n <= 1 ? 1 : n * fact(n - 1));
  const choose = (n, k) => fact(n) / (fact(k) * fact(n - k));

  T.topic({
    id: "backtracking", n: 22, stage: STAGE,
    title: "Backtracking",
    idea: "Build the answer one choice at a time. The moment a partial answer can't work, undo the last choice and try the next option. Pruning dead branches early is what makes it fast enough.",
    signals: "\"All\" combinations, permutations, subsets or arrangements, puzzles (N-Queens, Sudoku), small n (≤ 20).",
    invariant: "The partial answer is always valid so far. Choose, explore, then un-choose before trying the next option.",
    drills: [
      {
        id: "queens", name: "Place the queens",
        blurb: "Place one queen per row so that no two share a column or a diagonal. Dark squares are blocked: no queen can stand there, but attacks pass straight through. Search systematically: try columns left to right, and when a row has no safe square, backtrack.",
        *play(ctx) {
          const { n, blocked } = queensInstance();
          const qs = [], tried = Array(n).fill(-1);
          let r = 0;
          const attacker = (row, col) => qs.find(([qr, qc]) => qc === col || Math.abs(qr - row) === Math.abs(qc - col));
          const safe = (row, col) => !blocked.has(`${row},${col}`) && !attacker(row, col);
          let backtracks = 0;
          while (r < n) {
            let c = tried[r] + 1;
            while (c < n && !safe(r, c)) c++;
            ctx.draw(V.grid(n, n, (row, col) => {
              const k = `${row},${col}`;
              if (qs.some(([a, b]) => a === row && b === col)) return { t: "♛", cls: "queen" + (row === r - 1 ? " soft" : "") };
              if (blocked.has(k)) return { cls: "wall" };
              if (row === r && col <= tried[r]) return { t: "×", cls: "dim", pick: k };
              return { pick: k, cls: row === r ? "soft" : "" };
            }, { cls: "big", rowHead: T.range(n, 1), colHead: T.range(n, 1), corner: "row" }),
              V.line(`Placing row ${r + 1}.   backtracks: ${backtracks}`));
            const ans = c < n ? `${r},${c}` : "back";
            yield T.ask({
              prompt: c < n || r > 0 ? `Click where the queen in row ${r + 1} goes, or…` : "Click where the first queen goes.",
              picks: true, options: r > 0 ? [["back", "Dead end: backtrack"]] : null,
              answer: ans,
              why: (v) => {
                if (v === "back") return `Column ${c + 1} in row ${r + 1} is still safe.`;
                const [row, col] = v.split(",").map(Number);
                if (row !== r) return `Work row by row. This step places a queen in row ${r + 1}.`;
                if (col <= tried[r]) return "That column was already tried in this row, and it led to a dead end.";
                if (blocked.has(v)) return "That square is blocked.";
                const at = attacker(row, col);
                if (at) return `Attacked by the queen in row ${at[0] + 1}, column ${at[1] + 1}${at[1] === col ? " (same column)" : " (diagonal)"}.`;
                if (c >= n) return `Every square in row ${r + 1} is either attacked or already tried. Backtrack.`;
                return `Try columns left to right: column ${c + 1} is safe and comes first.`;
              },
              note: ans === "back" ? `Row ${r + 1} is impossible, so the queen in row ${r} moves on to its next column.` : null,
            });
            if (c < n) { qs.push([r, c]); tried[r] = c; r++; }
            else { tried[r] = -1; r--; qs.pop(); backtracks++; }
          }
          ctx.draw(V.grid(n, n, (row, col) => (qs.some(([a, b]) => a === row && b === col) ? { t: "♛", cls: "queen ok" } : blocked.has(`${row},${col}`) ? { cls: "wall" } : {}), { cls: "big" }));
          return { summary: `Solved after ${backtracks} backtrack${backtracks === 1 ? "" : "s"}. In code: a set each for used columns and both diagonals (r − c and r + c), so each safety check is O(1).` };
        },
      },
      {
        id: "parens", name: "Which branches live?",
        blurb: "Generate every valid string of n pairs of parentheses. At each step you can add \"(\" or \")\", but some branches are dead on arrival. Prune them.",
        *play(ctx) {
          const n = T.rand(3, 4);
          let str = "";
          for (;;) {
            const open = [...str].filter((c) => c === "(").length, close = str.length - open;
            const canOpen = open < n, canClose = close < open;
            ctx.draw(V.line(`n = ${n} pairs`), h("p", { class: "line", style: "font:600 30px var(--mono);letter-spacing:0.08em" }, str || "(empty)"));
            const ans = canOpen && canClose ? "both" : canOpen ? "open" : canClose ? "close" : "none";
            yield T.choose("Which characters can you add without ruining the string?", [["open", "Only ("], ["close", "Only )"], ["both", "Both"], ["none", "Neither: it's complete"]], ans,
              `Here open = ${open}, close = ${close}. "(" is allowed while open < ${n}. ")" is allowed while close < open.`,
              ans === "both" ? "Two live branches. The search explores both." : null);
            if (ans === "none") break;
            str += ans === "both" ? T.pick(["(", ")"]) : ans === "open" ? "(" : ")";
          }
          return { summary: `With those two rules, every leaf is a valid string. There are ${catalan(n)} of them for n = ${n}, and nothing is ever generated and then thrown away.` };
        },
      },
      {
        id: "size", name: "How big is the search?",
        blurb: "Before backtracking, estimate how many answers there are. That's how you know whether brute force is even possible.",
        *play(ctx) {
          const qs = [
            () => { const n = T.rand(3, 6); return [`All orderings (permutations) of ${n} distinct items`, fact(n), [n ** 2, 2 ** n, n * (n - 1)], `${n} choices for the first slot, ${n - 1} for the next… = ${n}!`]; },
            () => { const n = T.rand(3, 7); return [`All subsets of ${n} items (including the empty set)`, 2 ** n, [n ** 2, fact(n), 2 ** n - 1], `Each item is either in or out: 2 × 2 × … = 2^${n}.`]; },
            () => { const n = T.rand(5, 7), k = T.rand(2, 3); return [`All ways to choose ${k} items from ${n} (order doesn't matter)`, choose(n, k), [n * k, n ** k, fact(n) / fact(n - k)], `C(${n}, ${k}) = ${n}! / (${k}! · ${n - k}!). Ordered picks divided by the ${k}! orders of each group.`]; },
            () => { const n = T.rand(3, 4); return [`Valid strings of ${n} pairs of parentheses`, catalan(n), [2 ** (2 * n), fact(n), n * n], `The Catalan number: 1, 2, 5, 14 for n = 1 to 4. Far fewer than the 2^${2 * n} raw strings.`]; },
            () => { const a = T.rand(2, 4), k = T.rand(3, 4); return [`Strings of length ${k} using ${a} letters (repeats allowed)`, a ** k, [k ** a, a * k, choose(a + k - 1, k)], `${a} choices at each of ${k} positions: ${a}^${k}.`]; },
          ];
          for (const make of T.shuffle(qs)) {
            const [q, ans, wrong, why] = make();
            ctx.draw(h("p", { class: "line", style: "font-size:19px;font-weight:600" }, q));
            const opts = [...new Set([ans, ...wrong.filter((x) => Number.isInteger(x) && x > 0)])].slice(0, 4);
            yield T.choose("How many?", opts.sort((x, y) => x - y), ans, () => why, why);
          }
          return { summary: "n! is hopeless past about 11, and 2ⁿ past about 25. Pruning can only remove part of that." };
        },
      },
    ],
  });
})();
