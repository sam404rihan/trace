"use strict";
(function () {
  const T = window.Trace;
  const { h, V } = T;
  const STAGE = "Dynamic programming and bits";
  const INF = Infinity;
  const fmt = (x) => (x === INF ? "∞" : x);

  // ── 23 1D dynamic programming ────────────────────────────────────────────
  T.topic({
    id: "dp-1d", n: 23, stage: STAGE,
    title: "Dynamic programming in 1D",
    idea: "Name the state (dp[i] = the best answer for the first i things), then ask what the last decision was. Each cell is a small choice over cells you've already filled, so nothing gets computed twice.",
    signals: "\"Number of ways\", \"minimum or maximum\", choices that affect later options, or a naive recursion that keeps repeating subproblems.",
    invariant: "When you fill dp[i], every cell it depends on is already final.",
    drills: [
      {
        id: "robber", name: "Rob or skip",
        blurb: "Houses in a row, and you can't rob two neighbours. dp[i] = the most you can take from houses 0..i. For house i, either skip it or rob it plus whatever was safe before its neighbour.",
        *play(ctx) {
          const n = T.rand(7, 8);
          const a = Array.from({ length: n }, () => T.rand(1, 12));
          const dp = Array(n).fill("");
          dp[0] = a[0];
          for (let i = 1; i < n; i++) {
            const skip = dp[i - 1], rob = a[i] + (i >= 2 ? dp[i - 2] : 0);
            ctx.draw(
              V.array(a, { label: "house value", cls: (k) => (k === i ? "hot" : "") }),
              V.array(dp, { label: "dp[i] = best from houses 0..i", cls: (k) => (k === i - 1 ? "pa" : k === i - 2 ? "pb" : k === i ? "soft" : "") }));
            yield T.choose(`House ${i} (worth ${a[i]}). Which choice is better?`,
              [["skip", `Skip it: keep dp[${i - 1}]`], ["rob", i >= 2 ? `Rob it: ${a[i]} + dp[${i - 2}]` : `Rob it: ${a[i]} + nothing before`]],
              skip > rob ? "skip" : rob > skip ? "rob" : ["skip", "rob"],
              `Skip gives ${skip}. Rob gives ${a[i]} + ${i >= 2 ? dp[i - 2] : 0} = ${rob}. Take the bigger.`,
              `dp[${i}] = max(${skip}, ${rob}) = ${Math.max(skip, rob)}`);
            dp[i] = Math.max(skip, rob);
          }
          ctx.draw(V.array(a, { label: "house value" }), V.array(dp, { label: "dp", cls: (k) => (k === n - 1 ? "ok" : "") }));
          return { summary: `Best haul: ${dp[n - 1]}. You only ever look two cells back, so two variables are enough.` };
        },
      },
      {
        id: "coins", name: "Fewest coins",
        blurb: "dp[a] = the fewest coins that make amount a. The last coin used was one of the coin values, so dp[a] = 1 + the best dp[a − coin]. Click the cell dp[a] builds from.",
        *play(ctx) {
          const coins = T.pick([[1, 3, 4], [1, 4, 5], [1, 5, 6], [2, 3, 5]]);
          const amount = T.rand(8, 11);
          const dp = Array(amount + 1).fill(INF);
          dp[0] = 0;
          const shown = Array(amount + 1).fill("");
          shown[0] = 0;
          const from = Array(amount + 1).fill(-1);
          for (let a = 1; a <= amount; a++) {
            const cands = coins.filter((c) => c <= a && dp[a - c] < INF).map((c) => a - c);
            if (!cands.length) { shown[a] = "∞"; continue; }
            const best = Math.min(...cands.map((x) => dp[x]));
            if (a <= 2 && cands.length === 1) { dp[a] = best + 1; shown[a] = dp[a]; from[a] = cands[0]; continue; }
            ctx.draw(V.line(`coins: ${coins.join(", ")}   amount ${amount}`),
              V.array(shown, { label: "dp[a] = fewest coins for amount a", pick: (k) => k < a, cls: (k) => (k === a ? "hot" : coins.includes(a - k) && k >= 0 && k < a ? "soft" : "") }));
            const src = yield T.ask({
              prompt: `dp[${a}]: click the amount you build from (yellow tint = one coin away).`,
              picks: true,
              answer: cands.filter((x) => dp[x] === best).map(String),
              why: (v) => {
                const k = Number(v);
                if (!coins.includes(a - k)) return `There's no coin worth ${a - k}, so ${k} isn't one coin away from ${a}.`;
                if (dp[k] === INF) return `${k} can't be made at all.`;
                return `dp[${k}] = ${dp[k]}, but ${cands.filter((x) => dp[x] === best).map((x) => `dp[${x}]`).join(" or ")} = ${best} is fewer.`;
              },
            });
            dp[a] = best + 1;
            shown[a] = dp[a];
            from[a] = Number(src);
          }
          const greedy = (() => { let left = amount, cnt = 0; for (const c of coins.slice().sort((x, y) => y - x)) { while (left >= c) { left -= c; cnt++; } } return left ? INF : cnt; })();
          const used = [];
          for (let a = amount; a > 0 && from[a] >= 0; a = from[a]) used.push(a - from[a]);
          ctx.draw(V.line(`coins: ${coins.join(", ")}   amount ${amount}`), V.array(shown, { label: "dp", cls: (k) => (k === amount ? "ok" : "") }),
            V.line(`best: ${fmt(dp[amount])} coins (${used.join(" + ")})`));
          if (greedy !== dp[amount]) {
            yield T.choose(`Greedy (always take the biggest coin that fits) would use how many coins for ${amount}?`,
              T.numOptions(greedy === INF ? -1 : greedy, { spread: 2, min: -1 }).map((x) => [x, x === -1 ? "It gets stuck" : String(x)]),
              greedy === INF ? -1 : greedy, "Take the largest coin that fits, repeatedly, and count.",
              `Greedy gives ${fmt(greedy)}, DP gives ${dp[amount]}. That gap is why this needs DP.`);
          }
          return { summary: "Each cell is 1 + the best cell one coin back. Greedy fails on coin sets like these. DP doesn't." };
        },
      },
      {
        id: "stairs", name: "Count the ways",
        blurb: "Climb n stairs using the allowed step sizes. ways[i] = number of ways to stand on stair i. The last step had to be one of the allowed sizes, so add up those cells.",
        *play(ctx) {
          const steps = T.pick([[1, 2], [1, 3], [1, 2, 3], [2, 3]]);
          const n = T.rand(7, 8);
          const ways = Array(n + 1).fill("");
          const val = Array(n + 1).fill(0);
          val[0] = 1; ways[0] = 1;
          for (let i = 1; i <= n; i++) {
            const from = steps.filter((s) => i - s >= 0).map((s) => i - s);
            const v = from.reduce((s, k) => s + val[k], 0);
            if (i < Math.min(...steps) || (i === 1 && from.length === 1)) { val[i] = v; ways[i] = v; continue; }
            ctx.draw(V.line(`allowed steps: ${steps.join(" or ")}`),
              V.array(ways, { label: "ways[i]", cls: (k) => (k === i ? "hot" : from.includes(k) ? "pa" : "") }));
            yield T.choose(`ways[${i}] = ?`, T.numOptions(v, { spread: 3, min: 0, extra: [val[i - 1] * 2, v + 1] }), v,
              `The last step was ${steps.join(" or ")}: ${from.map((k) => `ways[${k}]`).join(" + ")} = ${from.map((k) => val[k]).join(" + ")} = ${v}.`,
              `${from.map((k) => val[k]).join(" + ")} = ${v}`);
            val[i] = v; ways[i] = v;
          }
          ctx.draw(V.line(`allowed steps: ${steps.join(" or ")}`), V.array(ways, { label: "ways[i]", cls: (k) => (k === n ? "ok" : "") }));
          return { summary: "\"What was the last move?\" gives you the recurrence. With steps 1 or 2, it's Fibonacci." };
        },
      },
    ],
  });

  // ── 24 2D dynamic programming ────────────────────────────────────────────
  function lcsInstance() {
    const a = Array.from({ length: T.rand(4, 5) }, () => T.pick("ABCD".split(""))).join("");
    const b = Array.from({ length: T.rand(4, 5) }, () => T.pick("ABCD".split(""))).join("");
    return { a, b };
  }

  function* fillTable(ctx, { R, C, rowHead, colHead, table, ask, cellsToAsk, header }) {
    // Draws the table filled in row-major order up to the asked cell, and asks about it.
    for (const [r, c] of cellsToAsk) {
      const shown = (i, j) => i < r || (i === r && j < c) || i === 0 || j === 0;
      const q = ask(r, c);
      ctx.draw(header, V.grid(R, C, (i, j) => {
        const k = `${i},${j}`;
        if (i === r && j === c) return { t: "?", cls: "hot" };
        const near = q.near.includes(k);
        return { t: shown(i, j) ? fmt(table[i][j]) : "", cls: q.cls ? q.cls(i, j) : near ? "cand" : "", pick: near ? k : null };
      }, { rowHead, colHead, cls: "big" }));
      yield q.ask;
    }
  }

  T.topic({
    id: "dp-2d", n: 24, stage: STAGE,
    title: "Dynamic programming in 2D",
    idea: "When the state needs two indexes (a position in each of two strings, or a row and a column) the table is a grid. Each cell looks only at its neighbours above, to the left and diagonally above-left.",
    signals: "Two strings (LCS, edit distance), grid paths, or knapsack (item × capacity).",
    invariant: "dp[i][j] answers the problem for prefixes a[:i] and b[:j]. Row 0 and column 0 are the empty-prefix base cases.",
    drills: [
      {
        id: "lcs", name: "Longest common subsequence",
        blurb: "dp[i][j] = LCS of the first i letters of the left word and the first j letters of the top word. Click the cell each answer comes from. If the letters match, take the diagonal + 1. If not, take the bigger of up and left.",
        *play(ctx) {
          const { a, b } = lcsInstance();
          const R = a.length + 1, C = b.length + 1;
          const t = Array.from({ length: R }, () => Array(C).fill(0));
          for (let i = 1; i < R; i++) for (let j = 1; j < C; j++) t[i][j] = a[i - 1] === b[j - 1] ? t[i - 1][j - 1] + 1 : Math.max(t[i - 1][j], t[i][j - 1]);
          const all = [];
          for (let i = 1; i < R; i++) for (let j = 1; j < C; j++) all.push([i, j]);
          const matches = all.filter(([i, j]) => a[i - 1] === b[j - 1]);
          const pickCells = T.shuffle([...T.sample(matches, Math.min(2, matches.length)), ...T.sample(all.filter(([i, j]) => a[i - 1] !== b[j - 1]), 4)]).slice(0, 6)
            .sort((p, q) => p[0] - q[0] || p[1] - q[1]);
          yield* fillTable(ctx, {
            R, C, rowHead: ["∅", ...a], colHead: ["∅", ...b], table: t, cellsToAsk: pickCells,
            header: V.line(`left word ${a}   top word ${b}`),
            ask: (i, j) => {
              const same = a[i - 1] === b[j - 1];
              const up = t[i - 1][j], left = t[i][j - 1], diag = t[i - 1][j - 1];
              const answer = same ? [`${i - 1},${j - 1}`] : [up >= left && `${i - 1},${j}`, left >= up && `${i},${j - 1}`].filter(Boolean);
              return {
                near: [`${i - 1},${j - 1}`, `${i - 1},${j}`, `${i},${j - 1}`],
                ask: T.ask({
                  prompt: `Cell (${a[i - 1]}, ${b[j - 1]}): which neighbour does it come from?`, picks: true, answer,
                  why: (v) => {
                    if (same) return `"${a[i - 1]}" matches "${b[j - 1]}". Pair them up: diagonal (${diag}) + 1.`;
                    if (v === `${i - 1},${j - 1}`) return `"${a[i - 1]}" ≠ "${b[j - 1]}", so they can't pair up. Drop one letter: the bigger of up (${up}) and left (${left}).`;
                    return `Up is ${up}, left is ${left}. Take the bigger.`;
                  },
                  note: same ? `Match: ${diag} + 1 = ${diag + 1}` : `max(${up}, ${left}) = ${t[i][j]}`,
                }),
              };
            },
          });
          ctx.draw(V.line(`left word ${a}   top word ${b}`), V.grid(R, C, (i, j) => ({ t: t[i][j], cls: i === R - 1 && j === C - 1 ? "ok" : "" }), { rowHead: ["∅", ...a], colHead: ["∅", ...b], cls: "big" }));
          return { summary: `LCS length ${t[R - 1][C - 1]}, in the bottom-right corner. A match means the diagonal plus one, and anything else means dropping a letter from one word.` };
        },
      },
      {
        id: "paths", name: "Grid paths",
        blurb: "Move only right or down from the top-left corner. Dark cells are blocked. paths[r][c] = the number of ways to reach that cell.",
        *play(ctx) {
          let R = 4, C = 5, block, t;
          do {
            block = new Set();
            while (block.size < T.rand(2, 3)) { const r = T.rand(0, R - 1), c = T.rand(0, C - 1); if ((r || c) && !(r === R - 1 && c === C - 1)) block.add(`${r},${c}`); }
            t = Array.from({ length: R }, () => Array(C).fill(0));
            for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) {
              if (block.has(`${r},${c}`)) continue;
              t[r][c] = r === 0 && c === 0 ? 1 : (r ? t[r - 1][c] : 0) + (c ? t[r][c - 1] : 0);
            }
          } while (t[R - 1][C - 1] < 3);
          const order = [];
          for (let r = 0; r < R; r++) for (let c = 0; c < C; c++) if ((r || c) && !block.has(`${r},${c}`)) order.push([r, c]);
          const asked = new Set(T.sample(order.filter(([r, c]) => r > 0 && c > 0), 5).map(([r, c]) => `${r},${c}`));
          asked.add(`${R - 1},${C - 1}`);
          const known = new Set(["0,0"]);
          for (const [r, c] of order) {
            const k = `${r},${c}`;
            if (!asked.has(k)) { known.add(k); continue; }
            ctx.draw(V.grid(R, C, (i, j) => {
              const kk = `${i},${j}`;
              if (block.has(kk)) return { cls: "wall" };
              if (kk === k) return { t: "?", cls: "hot" };
              const near = (i === r - 1 && j === c) || (i === r && j === c - 1);
              return { t: known.has(kk) ? t[i][j] : "", cls: near ? "cand" : "" };
            }, { cls: "big" }));
            const up = r ? t[r - 1][c] : 0, left = c ? t[r][c - 1] : 0;
            yield T.choose("How many paths reach the yellow cell?", T.numOptions(t[r][c], { spread: 3, extra: [up * left, Math.max(up, left)] }), t[r][c],
              `Every path arrives from above (${up}) or from the left (${left}). Blocked cells count as 0. ${up} + ${left} = ${t[r][c]}.`,
              `${up} + ${left} = ${t[r][c]}`);
            known.add(k);
          }
          ctx.draw(V.grid(R, C, (i, j) => (block.has(`${i},${j}`) ? { cls: "wall" } : { t: t[i][j], cls: i === R - 1 && j === C - 1 ? "ok" : "" }), { cls: "big" }));
          return { summary: "A cell's count is the sum of the cells that can step into it. Change the moves and you change which neighbours you add." };
        },
      },
      {
        id: "edit", name: "Edit distance",
        blurb: "The fewest single-letter inserts, deletes and replaces that turn the left word into the top word. If the letters match, it's free: copy the diagonal. Otherwise it's 1 + the cheapest of replace (↖), delete (↑) and insert (←).",
        *play(ctx) {
          const [a, b] = T.pick([["cat", "cut"], ["horse", "ros"], ["sun", "snow"], ["flaw", "lawn"], ["park", "spake"], ["tree", "three"], ["mean", "men"], ["code", "coder"], ["star", "stair"], ["form", "from"]]);
          const R = a.length + 1, C = b.length + 1;
          const t = Array.from({ length: R }, (_, i) => Array.from({ length: C }, (_, j) => (i === 0 ? j : j === 0 ? i : 0)));
          for (let i = 1; i < R; i++) for (let j = 1; j < C; j++)
            t[i][j] = a[i - 1] === b[j - 1] ? t[i - 1][j - 1] : 1 + Math.min(t[i - 1][j - 1], t[i - 1][j], t[i][j - 1]);
          const all = [];
          for (let i = 1; i < R; i++) for (let j = 1; j < C; j++) all.push([i, j]);
          const cells = T.sample(all, Math.min(6, all.length)).sort((p, q) => p[0] - q[0] || p[1] - q[1]);
          const OPS = { diag: "replace", up: "delete", left: "insert" };
          yield* fillTable(ctx, {
            R, C, rowHead: ["∅", ...a], colHead: ["∅", ...b], table: t, cellsToAsk: cells,
            header: V.line(`turn "${a}" into "${b}"`),
            ask: (i, j) => {
              const same = a[i - 1] === b[j - 1];
              const n = { diag: t[i - 1][j - 1], up: t[i - 1][j], left: t[i][j - 1] };
              const key = { diag: `${i - 1},${j - 1}`, up: `${i - 1},${j}`, left: `${i},${j - 1}` };
              const min = Math.min(n.diag, n.up, n.left);
              const answer = same ? [key.diag] : Object.keys(n).filter((d) => n[d] === min).map((d) => key[d]);
              return {
                near: Object.values(key),
                ask: T.ask({
                  prompt: `"${a[i - 1]}" vs "${b[j - 1]}": click the neighbour this cell builds from.`, picks: true, answer,
                  why: () => (same ? `The letters match, so no edit is needed. Copy the diagonal (${n.diag}).`
                    : `Different letters, so pay 1 plus the cheapest neighbour: replace ↖ ${n.diag}, delete ↑ ${n.up}, insert ← ${n.left}.`),
                  note: (v) => {
                    if (same) return `Free: ${n.diag}`;
                    const d = Object.keys(key).find((x) => key[x] === v);
                    return `${OPS[d]}: 1 + ${n[d]} = ${t[i][j]}`;
                  },
                }),
              };
            },
          });
          ctx.draw(V.line(`turn "${a}" into "${b}"`), V.grid(R, C, (i, j) => ({ t: t[i][j], cls: i === R - 1 && j === C - 1 ? "ok" : "" }), { rowHead: ["∅", ...a], colHead: ["∅", ...b], cls: "big" }));
          return { summary: `${t[R - 1][C - 1]} edits. Row 0 and column 0 are building from nothing (all inserts) or erasing everything (all deletes).` };
        },
      },
    ],
  });

  // ── 25 Bit tricks ────────────────────────────────────────────────────────
  const bin = (x) => (x >>> 0).toString(2).padStart(8, "0").slice(-8);
  const BITOPS = [
    { expr: "x & (x - 1)", f: (x) => x & (x - 1), why: "x − 1 flips the lowest 1 and every 0 below it. AND with x clears exactly that lowest 1." },
    { expr: "x & -x", f: (x) => x & -x & 255, why: "-x is ~x + 1. It agrees with x only at the lowest 1, so AND keeps just that bit." },
    { expr: "x | (1 << k)", k: true, f: (x, k) => x | (1 << k), why: "1 << k is a single 1 at position k. OR turns it on and leaves everything else alone." },
    { expr: "x & ~(1 << k)", k: "set", f: (x, k) => x & ~(1 << k) & 255, why: "~(1 << k) is all 1s except position k. AND clears that one bit." },
    { expr: "x ^ (1 << k)", k: true, f: (x, k) => x ^ (1 << k), why: "XOR with a single 1 flips that bit, whatever it was." },
    { expr: "x >> 1", f: (x) => x >> 1, why: "Every bit slides one place right, and the lowest bit falls off. That's x // 2." },
    { expr: "x << 1", small: true, f: (x) => (x << 1) & 255, why: "Every bit slides one place left and a 0 enters at the bottom. That's x × 2." },
    { expr: "x ^ 0b11110000", f: (x) => x ^ 0xf0, why: "XOR with 1s flips those bits, and XOR with 0s keeps them. The top four flip." },
  ];
  const TRICKS = [
    ["Is bit k of x set?", "(x >> k) & 1", ["x & k", "x >> (k & 1)", "x | (1 << k)"]],
    ["Turn off the lowest 1 bit", "x & (x - 1)", ["x - 1", "x & -x", "x ^ 1"]],
    ["Keep only the lowest 1 bit", "x & -x", ["x & (x - 1)", "x & 1", "x ^ -x"]],
    ["Is x a power of two? (x > 0)", "x & (x - 1) == 0", ["x % 2 == 0", "x & 1 == 0", "x ^ (x - 1) == 0"]],
    ["Find the one number that appears once (all others appear twice)", "XOR all the numbers", ["sum all the numbers", "AND all the numbers", "OR all the numbers"]],
    ["Flip bit k", "x ^ (1 << k)", ["x | (1 << k)", "x & ~(1 << k)", "~x"]],
    ["Is x odd?", "x & 1", ["x >> 1", "x & 2", "x ^ 1"]],
    ["Multiply x by 8", "x << 3", ["x << 8", "x >> 3", "x ^ 8"]],
    ["Count the 1 bits, one step per set bit", "while x: x &= x - 1; count += 1", ["while x: x >>= 2; count += 1", "count = x & 1", "count = x % 8"]],
    ["Loop over every subset of n items", "for mask in range(1 << n)", ["for mask in range(n)", "for mask in range(n << 1)", "for mask in range(2 * n)"]],
    ["Clear bit k", "x & ~(1 << k)", ["x ^ (1 << k)", "x | (1 << k)", "x & (1 << k)"]],
  ];

  T.topic({
    id: "bits", n: 25, stage: STAGE,
    title: "Bit tricks",
    idea: "An integer is a row of switches. AND keeps, OR sets, XOR flips, and shifts slide. A few patterns, like x & (x − 1), x & −x and XOR cancelling pairs, solve a surprising number of problems in O(1) space.",
    signals: "Powers of two, \"appears once\", subsets of small sets (n ≤ 20), toggling flags, or counting set bits.",
    invariant: "x ^ x = 0 and x ^ 0 = x, so XOR cancels pairs in any order.",
    drills: [
      {
        id: "predict", name: "Predict the bits",
        blurb: "Click bits in the result row to toggle them, then press Check. Bit 7 is on the left, bit 0 on the right.",
        *play(ctx) {
          for (const op of T.sample(BITOPS, 4)) {
            let x;
            do { x = T.rand(op.small ? 3 : 6, op.small ? 127 : 250); } while ((bin(x).match(/1/g) || []).length < 3);
            let k = T.rand(0, 7);
            if (op.k === "set") k = T.pick([...Array(8).keys()].filter((i) => (x >> i) & 1));
            const ans = bin(op.f(x, k));
            const bits = Array(8).fill("0");
            const expr = op.k ? op.expr.replace(/k/g, String(k)) : op.expr;
            const draw = () => ctx.draw(
              V.line(h("strong", {}, expr), `   x = ${x}`),
              h("div", { class: "bitrow" }, V.array(bin(x).split(""), { label: "x", idxText: (i) => 7 - i, cls: (i) => (bin(x)[i] === "1" ? "one" : "zero") })),
              h("div", { class: "bitrow" }, V.array(bits, { label: "result: click to toggle", pick: true, key: (i) => "b" + i, idxText: (i) => 7 - i, cls: (i) => (bits[i] === "1" ? "one" : "zero") })));
            draw();
            yield T.ask({
              prompt: "Set the result bits, then check.", picks: true,
              options: [["check", "Check"]], answer: "check",
              onPick: (v) => { const i = Number(v.slice(1)); bits[i] = bits[i] === "1" ? "0" : "1"; draw(); },
              accept: () => bits.join("") === ans,
              why: () => `Not quite. ${op.why}`,
              note: `${expr} = ${ans} = ${parseInt(ans, 2)}. ${op.why}`,
            });
          }
          return { summary: "x & (x − 1) drops the lowest 1 and x & −x isolates it. Those two cover most bit puzzles." };
        },
      },
      {
        id: "tricks", name: "Pick the trick",
        blurb: "Match each job to the one-liner that does it.",
        *play(ctx) {
          for (const [job, ans, wrong] of T.sample(TRICKS, 6)) {
            ctx.draw(h("p", { class: "line", style: "font-size:19px;font-weight:600" }, job));
            const opts = T.shuffle([ans, ...wrong]);
            yield T.ask({ prompt: "Which one?", options: opts.map((o) => ({ value: o, label: h("code", {}, o) })), answer: ans, why: `It's ${ans}.`, note: null });
          }
          return { summary: "These come up again and again. Learn to recognise them on sight." };
        },
      },
      {
        id: "xor", name: "XOR cancels pairs",
        blurb: "XOR is order-independent, and every pair cancels to 0. Find each result without doing the arithmetic.",
        *play(ctx) {
          for (let r = 0; r < 4; r++) {
            const lone = T.rand(1, 60);
            const pairs = T.distinct(T.rand(1, 3), 1, 60).filter((v) => v !== lone);
            const seq = T.shuffle([lone, ...pairs, ...pairs]);
            const withZero = r === 3;
            if (withZero) seq.splice(T.rand(0, seq.length), 0, 0);
            ctx.draw(h("p", { class: "line", style: "font:600 24px var(--mono)" }, seq.join(" ^ ")),
              h("div", { class: "bitrow" }, seq.map((v) => V.array(bin(v).split(""), { small: true, idx: false, label: String(v), cls: (i) => (bin(v)[i] === "1" ? "one" : "zero") }))));
            const opts = T.shuffle([...new Set([lone, ...pairs.slice(0, 2), seq.reduce((a, b) => a + b, 0) % 64, 0])]).slice(0, 4);
            if (!opts.includes(lone)) opts[0] = lone;
            yield T.choose("Result?", opts.sort((a, b) => a - b), lone,
              `Pairs cancel: ${pairs.map((p) => `${p} ^ ${p} = 0`).join(", ")}${withZero ? ", and ^ 0 changes nothing" : ""}. What's left is ${lone}.`,
              `Only ${lone} has no partner.`);
          }
          return { summary: "XOR everything to find the unpaired value: O(n) time, O(1) space, no hash set needed." };
        },
      },
    ],
  });
})();
