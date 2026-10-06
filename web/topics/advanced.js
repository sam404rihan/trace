"use strict";
(function () {
  const T = window.Trace;
  const { h, V } = T;
  const STAGE = "Advanced techniques";
  const bin = (x, w) => x.toString(2).padStart(w, "0");
  const lowbit = (i) => i & -i;

  // ── 26 Range queries ─────────────────────────────────────────────────────
  T.topic({
    id: "range-queries", n: 26, stage: STAGE,
    title: "Range queries",
    idea: "A Fenwick tree stores sums of blocks whose sizes are powers of two, read off the index's lowest set bit. A prefix query strips one bit per step, and an update adds one. Either way it touches at most log n cells.",
    signals: "Many range sums or counts while values keep changing, rank queries (\"how many smaller so far\"), or range min/max.",
    invariant: "tree[i] holds the sum of the lowbit(i) elements ending at position i.",
    drills: [
      {
        id: "fenwick", name: "Fenwick walk",
        blurb: "tree[i] covers the block (i − lowbit(i), i]. The binary under each cell shows its lowest set bit. Click the cells a query adds up, in order.",
        *play(ctx) {
          const n = T.rand(10, 16);
          const nums = Array.from({ length: n }, () => T.rand(1, 9));
          const tree = Array(n + 1).fill(0);
          nums.forEach((x, k) => { for (let i = k + 1; i <= n; i += lowbit(i)) tree[i] += x; });
          const w = n.toString(2).length;
          for (let round = 0; round < 2; round++) {
            const mode = round === 0 ? "prefix" : "update";
            const start = mode === "prefix" ? T.rand(Math.ceil(n / 2), n) : T.rand(1, Math.floor(n / 2));
            const path = [];
            if (mode === "prefix") for (let i = start; i > 0; i -= lowbit(i)) path.push(i);
            else for (let i = start; i <= n; i += lowbit(i)) path.push(i);
            const clicked = [];
            for (let step = 0; step <= path.length; step++) {
              const last = clicked[clicked.length - 1];
              const covered = (k) => last && k >= last - lowbit(last) + 1 && k <= last;
              ctx.draw(
                V.line(h("strong", {}, mode === "prefix" ? `prefix(${start}): sum of the first ${start} numbers` : `update(${start}): position ${start} changed`)),
                V.array(nums, { label: "nums (positions 1..n)", idxText: (k) => k + 1, cls: (k) => (covered(k + 1) ? "pa" : mode === "prefix" && k < start ? "soft" : mode === "update" && k === start - 1 ? "hot" : "") }),
                V.array(tree.slice(1), { label: "tree[i]", pick: step < path.length, key: (k) => String(k + 1), idxText: (k) => `${k + 1}: ${bin(k + 1, w)}`, cls: (k) => (clicked.includes(k + 1) ? "ok" : "") }),
                V.line(mode === "prefix" ? `running total: ${clicked.reduce((s, i) => s + tree[i], 0)}` : `cells updated: ${clicked.length}`));
              if (step === path.length) break;
              const want = path[step];
              const from = step === 0 ? null : path[step - 1];
              yield T.click(step === 0 ? `Click the first tree cell ${mode} touches.` : "Next cell?", String(want), () => {
                if (step === 0) return `It starts at tree[${start}] itself.`;
                return mode === "prefix"
                  ? `From ${from} (${bin(from, w)}), strip the lowest set bit: ${from} − ${lowbit(from)} = ${want}.`
                  : `From ${from} (${bin(from, w)}), add the lowest set bit: ${from} + ${lowbit(from)} = ${want}.`;
              }, mode === "prefix" ? `tree[${want}] covers positions ${want - lowbit(want) + 1}..${want}.` : `tree[${want}] covers position ${start}, so it changes.`);
              clicked.push(want);
            }
            yield T.choose(mode === "prefix" ? `Done: ${path.length} cells instead of ${start} numbers.` : `Done: ${path.length} cells to fix.`, [["go", round === 0 ? "Now an update" : "Finish"]], "go");
          }
          return { summary: "Queries walk down by stripping the lowest bit, and updates walk up by adding it. Both take O(log n) steps." };
        },
      },
    ],
  });

  // ── 27 String matching ───────────────────────────────────────────────────
  T.topic({
    id: "string-matching", n: 27, stage: STAGE,
    title: "String matching",
    idea: "KMP never re-reads the text. When a match breaks, the pattern itself tells you how much of what you already matched can be reused: the longest border, a prefix that is also a suffix.",
    signals: "Find every occurrence of a pattern, repeated or periodic strings, borders (prefix equals suffix), or duplicate substrings (rolling hash).",
    invariant: "k is the length of the longest prefix of the pattern that ends exactly at the current position.",
    drills: [
      {
        id: "prefix-function", name: "Build the prefix function",
        blurb: "pi[i] = the length of the longest proper prefix of s[0..i] that is also a suffix of it. Fill it in left to right. On a mismatch, k falls back to pi[k − 1].",
        *play(ctx) {
          const n = T.rand(7, 10);
          const s = Array.from({ length: n }, () => T.pick(["a", "a", "b"])).join("");
          const pi = Array(n).fill(0);
          let k = 0;
          const shown = Array(n).fill("");
          shown[0] = 0;
          for (let i = 1; i < n; i++) {
            const steps = [];
            let kk = k;
            while (kk && s[i] !== s[kk]) { steps.push(`"${s[i]}" ≠ s[${kk}] = "${s[kk]}", fall back to pi[${kk - 1}] = ${pi[kk - 1]}`); kk = pi[kk - 1]; }
            if (s[i] === s[kk]) { steps.push(`"${s[i]}" = s[${kk}], so the border grows to ${kk + 1}`); kk++; } else steps.push(`"${s[i]}" ≠ s[0], so there's no border`);
            ctx.draw(
              V.array(s.split(""), { label: "s", cls: (j) => (j === i ? "hot" : j < k ? "pa" : "") }),
              V.array(shown, { label: "pi", cls: (j) => (j === i ? "soft" : shown[j] !== "" ? "ok" : "") }),
              V.line(`k (border so far) = ${k}: the blue prefix "${s.slice(0, k)}" also ends just before i`));
            yield T.choose(`pi[${i}] = ?`, T.numOptions(kk, { spread: 2, extra: [k + 1, 0] }), kk, steps.join(". ") + ".", steps.join(". ") + ".");
            pi[i] = kk; k = kk; shown[i] = kk;
          }
          ctx.draw(V.array(s.split(""), { label: "s" }), V.array(pi, { label: "pi", cls: () => "ok" }));
          return { summary: "k rises by at most 1 per character, so all the fall-backs add up to O(n). That's why KMP is linear." };
        },
      },
    ],
  });

  // ── 28 Advanced DP ───────────────────────────────────────────────────────
  T.topic({
    id: "advanced-dp", n: 28, stage: STAGE,
    title: "Advanced dynamic programming",
    idea: "When the state is \"which items have I used\", store it as a bitmask: one bit per item, a whole subset in one integer. n! orderings collapse into 2ⁿ subsets, and states can be array indexes.",
    signals: "n <= 20 with \"visit all\" or \"assign everything\", intervals that merge or burst, decisions on trees, or several modes per step (holding/sold).",
    invariant: "A smaller mask is always computed before any mask that contains it, because supersets are numerically larger.",
    drills: [
      {
        id: "masks", name: "Read the mask",
        blurb: "Bit i of the mask is item i. Bit 0 is the rightmost bit. Translate between masks and subsets until it's automatic.",
        *play(ctx) {
          const n = 5;
          const items = "ABCDE".split("");
          for (let round = 0; round < 4; round++) {
            const mask = T.rand(1, (1 << n) - 2);
            if (round % 2 === 0) {
              const on = Array(n).fill(false);
              const draw = () => ctx.draw(
                V.line(h("strong", {}, `mask = ${mask}`), `   (binary ${bin(mask, n)})`),
                h("div", { class: "bitrow" }, V.array(items, { label: "items: click the ones in the subset", pick: true, key: (i) => "i" + i, idxText: (i) => `bit ${i}`, cls: (i) => (on[i] ? "one" : "") })));
              draw();
              yield T.ask({
                prompt: "Select the items in this subset, then check.", picks: true, options: [["check", "Check"]], answer: "check",
                onPick: (v) => { const i = Number(v.slice(1)); on[i] = !on[i]; draw(); },
                accept: () => on.every((x, i) => x === Boolean(mask >> i & 1)),
                why: () => `Read the binary right to left: bit 0 (the rightmost) is A. ${bin(mask, n)} means {${items.filter((_, i) => mask >> i & 1).join(", ")}}.`,
                note: `{${items.filter((_, i) => mask >> i & 1).join(", ")}} = ${bin(mask, n)} = ${mask}`,
              });
            } else {
              const chosen = items.filter((_, i) => mask >> i & 1);
              ctx.draw(V.line("subset ", h("strong", {}, `{${chosen.join(", ")}}`)),
                h("div", { class: "bitrow" }, V.array(items, { label: "items", idxText: (i) => `bit ${i}`, cls: (i) => (mask >> i & 1 ? "one" : "") })));
              const decoys = new Set([mask]);
              const rev = parseInt(bin(mask, n).split("").reverse().join(""), 2);
              for (const d of [rev, mask ^ 1, mask ^ (1 << (n - 1)), (mask + 1) % 32]) if (decoys.size < 4 && d > 0) decoys.add(d);
              yield T.choose("Which mask is this subset?", [...decoys].sort((a, b) => a - b).map((d) => [d, `${d}  (${bin(d, n)})`]), mask,
                (v) => (v === rev ? "That's the bits read in the wrong direction: A is bit 0, the RIGHTMOST bit." : `Add 2^i for each chosen item i: ${items.map((c, i) => (mask >> i & 1 ? `2^${i}` : null)).filter(Boolean).join(" + ")} = ${mask}.`),
                `${chosen.map((c) => `${c} = 2^${items.indexOf(c)}`).join(", ")}: total ${mask}`);
            }
          }
          ctx.draw(V.code("mask | (1 << i)    add item i\nmask & ~(1 << i)   remove item i\nmask >> i & 1      is item i in?\nmask & (mask - 1)  drop the lowest item"));
          yield T.choose("These four moves are all a bitmask DP needs.", [["go", "Got it"]], "go");
          return { summary: "One integer per subset means states fit in a plain list: dp[mask] instead of a dict of frozensets." };
        },
      },
    ],
  });

  // ── 29 Advanced graphs ───────────────────────────────────────────────────
  T.topic({
    id: "advanced-graphs", n: 29, stage: STAGE,
    title: "Advanced graphs",
    idea: "Many structural questions are a search with one extra piece of bookkeeping. A bipartite check is BFS with two colours, and finding bridges is DFS with discovery times. Notice the contradiction or the low-link, and the answer follows.",
    signals: "\"Split into two groups\", critical edges or nodes, mutually reachable groups, negative weights, all-pairs distances, or 0/1 edge costs.",
    invariant: "In a bipartite colouring, every edge joins two different colours. The first edge that doesn't proves an odd cycle.",
    drills: [
      {
        id: "two-colour", name: "Two-colour it",
        blurb: "BFS colouring. The popped node is yellow. Give each uncoloured neighbour the opposite colour, and call out a neighbour that already has the SAME colour.",
        *play(ctx) {
          const g = T.makeGraph(T.rand(6, 7), { extra: T.pick([0.15, 0.45]) });
          const adj = Object.fromEntries(g.nodes.map((x) => [x.id, []]));
          for (const e of g.edges) { adj[e.a].push(e.b); adj[e.b].push(e.a); }
          Object.values(adj).forEach((l) => l.sort());
          const color = {};
          const start = g.nodes.map((x) => x.id).sort()[0];
          color[start] = 0;
          const queue = [start];
          const name = ["blue", "pink"];
          const draw = (hot) => ctx.draw(
            V.graph(g, { ncls: (id) => (id === hot ? "hot" : color[id] === 0 ? "pa" : color[id] === 1 ? "pb" : ""), badge: (id) => (color[id] == null ? null : name[color[id]][0].toUpperCase()) }),
            V.chips(queue.slice(), { label: "queue", ends: ["front", "back"], empty: "empty" }));
          while (queue.length) {
            const v = queue.shift();
            for (const u of adj[v]) {
              if (color[u] == null) {
                draw(v);
                const want = 1 - color[v];
                yield T.choose(`${v} is ${name[color[v]]}. What colour does its neighbour ${u} get?`, [["0", "Blue"], ["1", "Pink"], ["x", "Conflict: not bipartite"]], String(want),
                  `Neighbours always get the opposite colour: ${v} is ${name[color[v]]}, so ${u} must be ${name[want]}.`);
                color[u] = want;
                queue.push(u);
              } else if (color[u] === color[v]) {
                draw(v);
                yield T.choose(`${v} and its neighbour ${u} are both ${name[color[v]]}. So:`, [["x", "Conflict: not bipartite"], ["ok", "Fine, keep going"]], "x",
                  "An edge whose ends share a colour can't be fixed by recolouring: it closes an odd cycle.");
                ctx.draw(V.graph(g, { ncls: (id) => (id === u || id === v ? "bad" : color[id] === 0 ? "pa" : color[id] === 1 ? "pb" : "") }));
                return { summary: "Found an odd cycle, so it's not bipartite. Graphs with only even cycles can always be two-coloured." };
              }
            }
          }
          draw(null);
          yield T.choose("Queue empty and no conflicts. Verdict?", [["yes", "Bipartite"], ["no", "Not bipartite"]], "yes", "Every edge joins blue to pink, so it's bipartite.");
          return { summary: "Colour on discovery, check on every edge. It's O(n + E), the same as plain BFS." };
        },
      },
    ],
  });
})();
