"use strict";
(function () {
  const T = window.Trace;
  const { h, V } = T;
  const STAGE = "Specialist topics";

  // ── 30 Number theory ─────────────────────────────────────────────────────
  T.topic({
    id: "number-theory", n: 30, stage: STAGE,
    title: "Number theory",
    idea: "The sieve finds primes by elimination. The smallest number nobody has crossed out must be prime, because nothing smaller divides it. Each prime then crosses out its multiples, starting at p², since smaller multiples already fell to a smaller prime.",
    signals: "Answers \"modulo 10^9 + 7\", counting or listing primes, factoring many numbers, gcd and lcm, nCr for large n.",
    invariant: "Before sieving with p, every crossed-out number has a prime factor smaller than p.",
    drills: [
      {
        id: "sieve", name: "Run the sieve",
        blurb: "Pick each prime in turn, say where its crossing-out starts, and notice when you can stop.",
        *play(ctx) {
          const N = T.rand(5, 7) * 10;
          const COLS = 10;
          const crossed = new Set(), primes = [];
          let current = null;
          const draw = (pick) => ctx.draw(
            V.grid(Math.ceil((N - 1) / COLS), COLS, (r, c) => {
              const x = 2 + r * COLS + c;
              if (x > N) return { t: "", cls: "dim" };
              const cls = x === current ? "hot" : primes.includes(x) ? "ok" : crossed.has(x) ? "soft" : "";
              return { t: crossed.has(x) ? "·" : x, cls, pick: pick && !crossed.has(x) && !primes.includes(x) ? String(x) : undefined };
            }, { label: `numbers 2..${N}: green = prime found, dot = crossed out` }),
            V.line(primes.length ? `primes so far: ${primes.join(", ")}` : "Nothing crossed out yet."));
          for (;;) {
            let p = 2;
            while (p <= N && (crossed.has(p) || primes.includes(p))) p++;
            current = null;
            draw(true);
            yield T.click("Click the next number to sieve with.", String(p),
              "Take the smallest number that is neither crossed out nor already used.",
              `${p} survived every earlier prime, so nothing smaller divides it: it's prime.`);
            current = p;
            primes.push(p);
            if (p * p > N) {
              draw(false);
              yield T.choose(`${p}² = ${p * p}, which is past ${N}. Is there anything left to cross out?`,
                [["no", "No: every number still standing is prime"], ["yes", `Yes, keep sieving with ${p}`]], "no",
                `A composite x ≤ ${N} has a factor ≤ √x < ${p}, and those primes have already crossed it out.`);
              break;
            }
            const opts = [...new Set([p * p, 2 * p, p * p + p, p + 1, 3 * p])].filter((v) => v <= N + p * p).slice(0, 4).sort((a, b) => a - b);
            draw(false);
            yield T.choose(`Sieving with ${p}. Which number does it cross out first?`, opts, p * p,
              (v) => (v === 2 * p ? `${2 * p} = 2 × ${p} has the smaller factor 2, so 2 already crossed it out.` : `Multiples of ${p} below ${p}² have a factor smaller than ${p}.`),
              `Start at ${p}² = ${p * p}: smaller multiples k × ${p} with k < ${p} are already crossed out.`);
            for (let m = p * p; m <= N; m += p) crossed.add(m);
          }
          for (let x = 2; x <= N; x++) if (!crossed.has(x) && !primes.includes(x)) primes.push(x);
          current = null;
          draw(false);
          return { summary: `${primes.length} primes up to ${N}, using just ${primes.filter((q) => q * q <= N).length} rounds of sieving. Starting at p² and stopping at √N is what makes the sieve O(n log log n).` };
        },
      },
    ],
  });

  // ── 31 Geometry ──────────────────────────────────────────────────────────
  const cross = (o, a, b) => (a.x - o.x) * (b.y - o.y) - (a.y - o.y) * (b.x - o.x);

  T.topic({
    id: "geometry", n: 31, stage: STAGE,
    title: "Computational geometry",
    idea: "One integer formula decides almost everything: the sign of a cross product says whether o → a → b turns left, turns right, or goes straight. The convex hull keeps only left turns: sweep the points in x order, and whenever the newest point makes the chain turn right (or go straight), the middle point is inside and gets popped.",
    signals: "Points, segments and polygons: \"does it cross\", \"is it inside\", \"area\", \"smallest fence around\", \"most points on a line\".",
    invariant: "The chain built so far turns left at every corner.",
    drills: [
      {
        id: "hull", name: "Monotone chain",
        blurb: "Build the bottom half of the convex hull. For each new point, decide whether the chain still turns left. If not, pop.",
        *play(ctx) {
          const n = T.rand(7, 9);
          const xs = T.sample(T.range(13), n).sort((a, b) => a - b);
          const pts = xs.map((x, i) => ({ id: T.letters[i], x, y: T.rand(0, 8) }));
          const g = {
            nodes: pts.map((p) => ({ id: p.id, x: p.x / 12, y: 1 - p.y / 8 })),
            edges: [],
          };
          const chain = [];
          let pops = 0;
          const draw = (hot, tail) => {
            g.edges = [];
            for (let i = 0; i + 1 < chain.length; i++) g.edges.push({ a: chain[i].id, b: chain[i + 1].id });
            if (tail) g.edges.push({ a: chain[chain.length - 1].id, b: hot.id });
            ctx.draw(
              V.graph(g, { W: 520, H: 260, directed: true, ncls: (id) => (hot && id === hot.id ? "hot" : chain.some((c) => c.id === id) ? "ok" : "dim"),
                ecls: (e) => (tail && e.b === hot.id ? "hot" : "on") }),
              V.line("chain: ", h("strong", {}, chain.map((c) => c.id).join(" → ") || "empty"), "   (points are taken left to right)"));
          };
          for (const p of pts) {
            while (chain.length >= 2) {
              const a = chain[chain.length - 2], b = chain[chain.length - 1];
              const c = cross(a, b, p);
              const want = c > 0 ? "left" : c < 0 ? "right" : "straight";
              draw(p, true);
              yield T.choose(`Going ${a.id} → ${b.id} → ${p.id}: which way does it turn?`, [["left", "Left"], ["right", "Right"], ["straight", "Straight"]], want,
                `cross = (${b.x}−${a.x})(${p.y}−${a.y}) − (${b.y}−${a.y})(${p.x}−${a.x}) = ${c}. ${c > 0 ? "Positive means left." : c < 0 ? "Negative means right." : "Zero means straight."}`,
                c > 0 ? `Left turn: ${b.id} stays a corner.` : `Not a left turn, so ${b.id} lies inside or on the hull's edge. Pop it.`);
              if (c > 0) break;
              chain.pop();
              pops++;
            }
            chain.push(p);
          }
          draw(null, false);
          yield T.choose(`Lower hull done: ${chain.map((c) => c.id).join(" → ")}. How many times did each point get pushed at most?`, [["1", "Once"], ["n", "Up to n times"]], "1",
            "Every point is pushed once and popped at most once, so the sweep is O(n) after sorting.");
          return { summary: `${pops} pop${pops === 1 ? "" : "s"} along the way. Run the same sweep right to left for the top half, and the two chains together are the hull.` };
        },
      },
    ],
  });

  // ── 32 Advanced trees ────────────────────────────────────────────────────
  T.topic({
    id: "advanced-trees", n: 32, stage: STAGE,
    title: "Advanced tree techniques",
    idea: "Binary lifting stores, for every node, its ancestors 1, 2, 4, 8, … levels up. Any jump of k levels is then the jumps for the set bits of k, so a query costs O(log n) instead of walking k steps.",
    signals: "Many questions about ancestors, lowest common ancestors or distances in one tree, or \"for every node\" answers that rerooting can update edge by edge.",
    invariant: "up[j][v] is the 2^j-th ancestor of v, so up[j][v] = up[j−1][ up[j−1][v] ].",
    drills: [
      {
        id: "lift", name: "Jump by powers of two",
        blurb: "Split k into powers of two, then make the jumps on the tree, one per set bit.",
        *play(ctx) {
          const n = T.rand(13, 16);
          const parent = [-1];
          for (let v = 1; v < n; v++) parent.push(T.rand(Math.max(0, v - 3), v - 1));
          const depth = parent.map(() => 0);
          for (let v = 1; v < n; v++) depth[v] = depth[parent[v]] + 1;
          const nodes = T.range(n).map((id) => ({ id, kids: [] }));
          for (let v = 1; v < n; v++) nodes[parent[v]].kids.push(nodes[v]);
          const anc = (v, k) => { while (k-- > 0 && v !== -1) v = parent[v]; return v; };
          let deepest = 0;
          for (let v = 0; v < n; v++) if (depth[v] > depth[deepest]) deepest = v;
          const start = deepest;
          const k = T.rand(Math.max(3, depth[start] - 3), depth[start]);
          const bits = [];
          for (let j = 4; j >= 0; j--) if (k >> j & 1) bits.push(1 << j);
          let at = start;
          const visited = [start];
          const draw = (pick) => ctx.draw(
            V.ntree([nodes[0]], { kids: (nd) => nd.kids, label: (nd) => nd.id, key: (nd) => String(nd.id), pick: () => pick,
              cls: (nd) => (nd.id === at ? "hot" : visited.includes(nd.id) ? "pa" : ""), badge: (nd) => (nd.id === start ? "start" : null) }),
            V.line(`k-th ancestor of ${start}, with k = ${k}  (binary ${k.toString(2)})`));
          draw(false);
          const combos = new Set([bits.join(" + ")]);
          for (const alt of [`${k - 1} + 1`, `${k}`, Array(Math.min(k, 5)).fill(1).join(" + ") + (k > 5 ? " + …" : "")]) {
            if (alt !== bits.join(" + ") && combos.size < 4 && !(alt === `${k}` && bits.length === 1)) combos.add(alt);
          }
          for (let guard = 0; combos.size < 4 && guard < 60; guard++) {
            const fake = [];
            let left = k;
            for (let j = 4; j >= 0 && left; j--) if ((1 << j) <= left && Math.random() < 0.7) { fake.push(1 << j); left -= 1 << j; }
            if (left) fake.push(left);
            if (fake.length) combos.add(fake.join(" + "));
          }
          yield T.choose(`Which jumps does binary lifting make for k = ${k}?`, T.shuffle([...combos]), bits.join(" + "),
            "One jump per 1-bit of k, each a power of two. Any other split needs more jumps or isn't stored.",
            `${k} = ${bits.join(" + ")}: just ${bits.length} jump${bits.length > 1 ? "s" : ""}.`);
          for (const b of bits) {
            const to = anc(at, b);
            draw(true);
            yield T.click(`Jump ${b} level${b > 1 ? "s" : ""} up from ${at}. Click where you land.`, String(to),
              `up[${Math.log2(b)}][${at}] is the ancestor exactly ${b} level${b > 1 ? "s" : ""} up: follow parent links ${b} times.`,
              `up[${Math.log2(b)}][${at}] = ${to}`);
            at = to;
            visited.push(at);
          }
          draw(false);
          return { summary: `${bits.length} table lookups instead of ${k} parent steps. With n nodes, any k needs at most log₂ n of them.` };
        },
      },
    ],
  });

  // ── 33 Network flow ──────────────────────────────────────────────────────
  const FLOW_POS = { s: [0, 0.5], a: [0.33, 0.08], b: [0.33, 0.92], c: [0.67, 0.08], d: [0.67, 0.92], t: [1, 0.5] };

  T.topic({
    id: "network-flow", n: 33, stage: STAGE,
    title: "Network flow and matching",
    idea: "Push flow along any path that still has room, as much as its tightest edge allows. Pushing also opens a reverse edge, so later paths can undo earlier choices. When no path is left, the flow is maximum, and it equals the cheapest cut between s and t.",
    signals: "Assignments with limits on both sides (people to jobs, students to slots), disjoint routes, \"cheapest way to disconnect\".",
    invariant: "On every edge, 0 ≤ flow ≤ capacity, and every node except s and t passes on exactly what it receives.",
    drills: [
      {
        id: "augment", name: "Augmenting paths",
        blurb: "Each round, BFS finds the shortest path with spare room. Say how much it can carry, then watch the flow grow until nothing gets through.",
        *play(ctx) {
          const base = [["s", "a"], ["s", "b"], ["a", "c"], ["b", "d"], ["c", "t"], ["d", "t"]];
          const extra = T.sample([["a", "d"], ["b", "c"], ["a", "b"], ["c", "d"]], T.rand(1, 2));
          const edges = [...base, ...extra].map(([a, b]) => ({ a, b, cap: T.rand(2, 9), flow: 0 }));
          const g = { nodes: Object.entries(FLOW_POS).map(([id, [x, y]]) => ({ id, x, y })), edges: [] };
          let path = null, total = 0, round = 0;
          const draw = () => {
            g.edges = edges.map((e) => ({ a: e.a, b: e.b, w: `${e.flow}/${e.cap}`, ref: e }));
            ctx.draw(
              V.graph(g, { W: 520, H: 280, directed: true, ecls: (ge) => (path && path.some((st) => st.e === ge.ref) ? "hot" : ge.ref.flow === ge.ref.cap ? "dim" : "on"),
                ncls: (id) => (id === "s" || id === "t" ? "end" : path && path.some((st) => st.to === id) ? "pa" : "") }),
              V.line("edge labels show flow / capacity.   total flow so far: ", h("strong", {}, String(total))));
          };
          const bfs = () => {
            const prev = { s: null };
            const q = ["s"];
            while (q.length && !("t" in prev)) {
              const u = q.shift();
              for (const e of edges) {
                if (e.a === u && e.flow < e.cap && !(e.b in prev)) { prev[e.b] = { e, from: u, to: e.b, room: e.cap - e.flow, back: false }; q.push(e.b); }
                if (e.b === u && e.flow > 0 && !(e.a in prev)) { prev[e.a] = { e, from: u, to: e.a, room: e.flow, back: true }; q.push(e.a); }
              }
            }
            if (!("t" in prev)) return null;
            const steps = [];
            for (let v = "t"; v !== "s"; v = prev[v].from) steps.unshift(prev[v]);
            return steps;
          };
          while ((path = bfs())) {
            round++;
            const push = Math.min(...path.map((st) => st.room));
            draw();
            const desc = path.map((st) => `${st.from}→${st.to}: ${st.room}${st.back ? " (undoing flow)" : ""}`).join(", ");
            yield T.choose(`Round ${round}: BFS found ${["s", ...path.map((st) => st.to)].join(" → ")}. How much can it carry?`, T.numOptions(push, { spread: 3, min: 1, extra: [Math.max(...path.map((st) => st.room))] }), push,
              `The path carries as much as its tightest edge allows. Spare room: ${desc}.`, `Bottleneck ${push}. Push it along every edge of the path.`);
            for (const st of path) st.e.flow += st.back ? -push : push;
            total += push;
          }
          path = null;
          draw();
          const cutSide = new Set(["s"]);
          let grew = true;
          while (grew) {
            grew = false;
            for (const e of edges) {
              if (cutSide.has(e.a) && !cutSide.has(e.b) && e.flow < e.cap) { cutSide.add(e.b); grew = true; }
              if (cutSide.has(e.b) && !cutSide.has(e.a) && e.flow > 0) { cutSide.add(e.a); grew = true; }
            }
          }
          const cut = edges.filter((e) => cutSide.has(e.a) && !cutSide.has(e.b));
          yield T.choose("No path from s to t has room left. What is the maximum flow?", T.numOptions(total, { spread: 4, min: 0, extra: [edges.filter((e) => e.a === "s").reduce((x, e) => x + e.cap, 0)] }), total,
            "Add up the flow leaving s (or arriving at t).",
            `Max flow ${total}. The full edges ${cut.map((e) => `${e.a}→${e.b}`).join(", ")} form a cut with exactly that capacity, so no flow can be bigger.`);
          return { summary: `${round} augmenting path${round === 1 ? "" : "s"}. Max flow = min cut = ${total}.` };
        },
      },
    ],
  });

  // ── 34 Digit DP ──────────────────────────────────────────────────────────
  T.topic({
    id: "digit-dp", n: 34, stage: STAGE,
    title: "Digit DP and DP speed-ups",
    idea: "Count numbers up to N by building them left to right. While your prefix equals N's prefix you're \"tight\" and capped by N's next digit. The moment you choose a smaller digit you're free, and every remaining position takes any allowed digit. The count is a sum of those free branches.",
    signals: "\"How many numbers from 1 to N (N up to 10^18) have…\" any property you can track digit by digit.",
    invariant: "Along the tight path, every digit so far equals N's digit in that position.",
    drills: [
      {
        id: "tight", name: "Tight or free",
        blurb: "Count the numbers from 0 to N that never use one forbidden digit, one position at a time.",
        *play(ctx) {
          const L = T.rand(3, 4);
          const digits = [T.rand(2, 9), ...T.range(L - 1).map(() => T.rand(0, 9))];
          const bad = T.rand(1, 9);
          const N = Number(digits.join(""));
          const okDigits = 9;                     // 0-9 without the forbidden one
          let total = 0, i = 0, alive = true;
          const parts = [];
          const draw = () => ctx.draw(
            V.array(digits, { label: `N = ${N}, forbidden digit ${bad}`, idxText: (k) => `pos ${k}`, cls: (k) => (k < i ? (alive ? "ok" : "soft") : k === i && alive ? "hot" : "") }),
            V.line("counted so far: ", h("strong", {}, String(total)), parts.length ? `   (${parts.join(" + ")})` : ""));
          for (i = 0; i < L; i++) {
            const D = digits[i];
            const below = T.range(D).filter((x) => x !== bad).length;
            const rest = L - i - 1;
            draw();
            yield T.choose(`Still tight at position ${i}, where N has ${D}. How many allowed digits are smaller than ${D}?`, T.numOptions(below, { spread: 2, min: 0, extra: [D] }), below,
              `Digits 0..${D - 1}${D > bad ? `, minus the forbidden ${bad}` : ""}.`, `${below} choices that make the number smaller than N, so from here on it's free.`);
            const add = below * okDigits ** rest;
            if (rest > 0) {
              yield T.choose(`Each of those ${below} leaves ${rest} free position${rest > 1 ? "s" : ""} with ${okDigits} allowed digits each. How many numbers is that?`,
                T.numOptions(add, { spread: Math.max(3, Math.floor(add / 4)), min: 0, extra: [below * 10 ** rest, below + okDigits * rest] }), add,
                `${below} × ${okDigits}^${rest} = ${add}.`);
            }
            total += add;
            parts.push(String(add));
            draw();
            const canStay = D !== bad;
            yield T.choose(`Can the number stay tight, keeping ${D} here?`, [["yes", "Yes, continue to the next position"], ["no", `No: ${D} is forbidden, stop`]], canStay ? "yes" : "no",
              canStay ? `${D} isn't the forbidden digit, so the tight path continues.` : `${D} is the forbidden digit, so no number can match N here. Nothing tight survives.`);
            if (!canStay) { alive = false; break; }
          }
          if (alive) {
            total += 1;
            parts.push("1");
            i = L;
            draw();
            yield T.choose(`The tight path made it to the end: that's N = ${N} itself. Count it?`, [["yes", "Yes, add 1"], ["no", "No"]], "yes", `N uses no ${bad}, so it counts.`);
          }
          draw();
          let check = 0;
          for (let x = 0; x <= N; x++) if (!String(x).padStart(L, "0").includes(String(bad))) check++;
          return { summary: `${total} numbers from 0 to ${N} avoid ${bad} (a loop agrees: ${check}). It took ${L} steps instead of ${N + 1}, and that stays true for N = 10^18.` };
        },
      },
    ],
  });
})();
