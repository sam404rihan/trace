"use strict";
(function () {
  const T = window.Trace;
  const { h, s, V } = T;
  const STAGE = "Data structures";

  // ── 12 Stacks ────────────────────────────────────────────────────────────
  const PAIR = { ")": "(", "]": "[", "}": "{" };
  function bracketString() {
    const open = "([{", close = ")]}";
    const out = [], st = [];
    const len = T.rand(3, 5) * 2;
    while (out.length < len) {
      const remaining = len - out.length;
      if (st.length && (st.length >= remaining || Math.random() < 0.45)) out.push(close[open.indexOf(st.pop())]);
      else { const c = T.pick(open.split("")); out.push(c); st.push(c); }
    }
    const kind = T.pick(["ok", "ok", "swap", "extra-open", "extra-close"]);
    if (kind === "swap") {
      const idx = out.map((c, i) => (close.includes(c) ? i : -1)).filter((i) => i >= 0);
      const i = T.pick(idx);
      out[i] = T.pick(close.split("").filter((c) => c !== out[i]));
    } else if (kind === "extra-open") out.splice(T.rand(0, out.length), 0, T.pick(open.split("")));
    else if (kind === "extra-close") out.splice(T.rand(1, out.length), 0, T.pick(close.split("")));
    return out;
  }

  function rpnTokens() {
    const leaf = () => ({ v: T.rand(1, 9) });
    let nodes = [leaf(), leaf(), leaf(), leaf()];
    while (nodes.length > 1) {
      const i = T.rand(0, nodes.length - 2);
      const op = T.pick(["+", "-", "*", "-"]);
      nodes.splice(i, 2, { op, l: nodes[i], r: nodes[i + 1] });
    }
    const toks = [];
    (function post(n) { if (n.op) { post(n.l); post(n.r); toks.push(n.op); } else toks.push(String(n.v)); })(nodes[0]);
    return toks;
  }
  const applyOp = (a, op, b) => (op === "+" ? a + b : op === "-" ? a - b : a * b);

  T.topic({
    id: "stacks", n: 12, stage: STAGE,
    title: "Stacks",
    idea: "A stack remembers unfinished business, most recent first. Openers wait for their closer, operands wait for their operator, and in a monotonic stack each day waits for a warmer one.",
    signals: "Matching pairs, nesting, \"next greater/smaller element\", undo, evaluating expressions, or a DFS without recursion.",
    invariant: "The top of the stack is always the most recent thing still waiting to be resolved.",
    drills: [
      {
        id: "brackets", name: "Match the brackets",
        blurb: "Scan left to right. Openers go on the stack, and each closer must match the top.",
        *play(ctx) {
          const str = bracketString();
          const st = [];
          for (let i = 0; i < str.length; i++) {
            const c = str[i], top = st[st.length - 1];
            ctx.draw(V.array(str, { ptr: { i }, cls: (k) => (k === i ? "hot" : k < i ? "dim" : "") }),
              V.chips(st, { label: "stack (top on the right)", empty: "empty", cls: (k) => (k === st.length - 1 ? "pa" : "") }));
            const isOpen = !PAIR[c];
            const ans = isOpen ? "push" : top === PAIR[c] ? "pop" : "invalid";
            yield T.choose(`Next character: ${c}`, [["push", "Push it"], ["pop", "Pop: it matches the top"], ["invalid", "Invalid: stop here"]], ans, (v) => {
              if (isOpen) return v === "pop" ? `"${c}" opens something. Push it and wait for its closer.` : "An opener is always fine for now. It just needs a closer later.";
              if (v === "push") return `"${c}" is a closer. Closers never go on the stack: they resolve the top.`;
              if (ans === "invalid") return top ? `The top is "${top}", which "${c}" can't close.` : `The stack is empty, so there's nothing for "${c}" to close.`;
              return `"${c}" closes the "${top}" on top.`;
            });
            if (ans === "invalid") {
              ctx.draw(V.array(str, { cls: (k) => (k === i ? "bad" : k < i ? "dim" : "") }), V.chips(st, { label: "stack" }));
              return { summary: "A closer that doesn't match the top means the nesting crossed, like ( [ ) ]." };
            }
            if (ans === "push") st.push(c); else st.pop();
          }
          ctx.draw(V.array(str, { cls: () => "dim" }), V.chips(st, { label: "stack at the end", empty: "empty", cls: () => "hot" }));
          yield T.choose("End of string. Verdict?", [["valid", "Valid"], ["left", "Invalid: openers left over"]], st.length ? "left" : "valid",
            st.length ? `${st.join(" ")} never got closed.` : "Every opener was closed, and the stack is empty.");
          return { summary: "Valid means three things: every closer matched the top, nothing was closed from an empty stack, and the stack ended empty." };
        },
      },
      {
        id: "temps", name: "Wait for a warmer day",
        blurb: "For each day, how many days until it gets warmer? Days that are still waiting sit on a stack, coldest on top. A warm day resolves every colder day on top.",
        *play(ctx) {
          const n = 8;
          const t = Array.from({ length: n }, () => T.rand(60, 78));
          const wait = Array(n).fill("");
          const st = [];
          for (let i = 0; i < n; i++) {
            ctx.draw(
              V.array(t, { ptr: { i }, cls: (k) => (k === i ? "hot" : st.includes(k) ? "pa" : k < i ? "dim" : ""), label: "temperature" }),
              V.array(wait, { label: "days to wait", idx: false, cls: (k) => (wait[k] !== "" ? "ok" : "") }),
              V.chips(st.map((k) => `${t[k]} (day ${k})`), { label: "waiting stack (top on the right)", empty: "empty" }));
            let pops = 0;
            for (let j = st.length - 1; j >= 0 && t[st[j]] < t[i]; j--) pops++;
            const stopper = st.length > pops ? t[st[st.length - 1 - pops]] : null;
            yield T.choose(`Day ${i} is ${t[i]}°. How many waiting days get their answer now?`, T.numOptions(pops, { spread: 2 }), pops,
              `Pop while the top is colder than ${t[i]}. ${pops ? `${pops} day${pops > 1 ? "s are" : " is"} colder` : "The top isn't colder"}${stopper != null ? `, then ${stopper} stops it (not colder).` : st.length ? ", and that empties the stack." : ": the stack is empty."}`,
              pops ? `${pops} resolved: each one waited (${i} − its day) days.` : `Nothing is colder. Day ${i} joins the stack.`);
            for (let p = 0; p < pops; p++) { const k = st.pop(); wait[k] = i - k; }
            st.push(i);
          }
          for (const k of st) wait[k] = 0;
          ctx.draw(V.array(t, { label: "temperature" }), V.array(wait, { label: "days to wait (0 = never)", idx: false, cls: () => "ok" }));
          return { summary: "Each day is pushed once and popped at most once, so it's O(n). The stack always runs warm at the bottom to cold at the top." };
        },
      },
      {
        id: "rpn", name: "Evaluate postfix",
        blurb: "In postfix (reverse Polish) notation, numbers wait on a stack and each operator takes the top two. The order matters for − .",
        *play(ctx) {
          const toks = rpnTokens();
          const st = [];
          for (let i = 0; i < toks.length; i++) {
            const tk = toks[i];
            if (!"+-*".includes(tk)) { st.push(Number(tk)); continue; }
            const b = st[st.length - 1], a = st[st.length - 2];
            ctx.draw(V.array(toks, { ptr: { i }, cls: (k) => (k === i ? "hot" : k < i ? "dim" : "") }),
              V.chips(st.map(String), { label: "stack (top on the right)", cls: (k) => (k >= st.length - 2 ? "pa" : "") }));
            const val = applyOp(a, tk, b), flipped = applyOp(b, tk, a);
            const opts = new Set([val, flipped]);
            for (const x of T.numOptions(val, { spread: 4, min: -99 })) if (opts.size < 4) opts.add(x);
            yield T.choose(`Operator ${tk}: pop two. What gets pushed back?`, [...opts].sort((x, y) => x - y), val,
              (v) => (v === flipped && val !== flipped ? `Order matters: the top (${b}) is the right operand, and the one under it (${a}) is the left. ${a} ${tk} ${b}.` : `Take the top two, ${a} then ${b}, and compute ${a} ${tk} ${b}.`),
              `${a} ${tk} ${b} = ${val}`);
            st.pop(); st.pop(); st.push(val);
          }
          ctx.draw(V.array(toks, { cls: () => "dim" }), V.chips(st.map(String), { label: "result", cls: () => "ok" }));
          return { summary: "No parentheses and no precedence rules: the stack order handles all of it." };
        },
      },
    ],
  });

  // ── 13 Queues and deques ─────────────────────────────────────────────────
  T.topic({
    id: "queues", n: 13, stage: STAGE,
    title: "Queues and deques",
    idea: "A queue processes things in arrival order, and a deque lets you trim from either end. A monotonic deque keeps only the items that could still be the answer, best at the front.",
    signals: "BFS, \"in the last k\" or \"in the last T seconds\", sliding window max or min, or work done in order of arrival.",
    invariant: "Front = oldest still relevant. In a monotonic deque, values also decrease from front to back.",
    drills: [
      {
        id: "window-max", name: "Sliding window max",
        blurb: "Window size k = 3. The deque holds indexes whose values decrease from front to back. A newcomer evicts every smaller value at the back, because they can never be a max again.",
        *play(ctx) {
          const n = 9, k = 3;
          const a = T.distinct(n, 1, 20);
          const dq = [];
          const out = Array(n - k + 1).fill("");
          for (let i = 0; i < n; i++) {
            const lo = Math.max(0, i - k + 1);
            const draw = () => ctx.draw(
              V.array(a, { win: [lo, i - 1 >= lo ? i - 1 : lo], ptr: { i }, cls: (x) => (x === i ? "hot" : x < lo ? "dim" : "") }),
              V.chips(dq.map((j) => `${a[j]}`), { label: "deque (values, front on the left)", ends: ["front", "back"], empty: "empty" }),
              V.array(out, { label: "window max", small: true, idxText: (x) => `${x}..${x + k - 1}`, cls: (x) => (out[x] !== "" ? "ok" : "") }));
            draw();
            let pops = 0;
            for (let j = dq.length - 1; j >= 0 && a[dq[j]] < a[i]; j--) pops++;
            yield T.choose(`New value ${a[i]}. How many pop off the back?`, T.numOptions(pops, { spread: 2 }), pops,
              `Pop from the back while it's smaller than ${a[i]}. ${pops ? `That removes ${dq.slice(dq.length - pops).map((j) => a[j]).join(", ")}` : "Nothing at the back is smaller"}${dq.length > pops ? `, then ${a[dq[dq.length - 1 - pops]]} is bigger, so stop.` : "."}`,
              pops ? `Gone: they're older and smaller than ${a[i]}, so they can't win any future window.` : null);
            dq.splice(dq.length - pops, pops);
            dq.push(i);
            if (i >= k) {
              draw();
              const out1 = dq[0] <= i - k;
              yield T.choose(`The window is now ${i - k + 1}..${i}. Is the front (value ${a[dq[0]]}, index ${dq[0]}) out of the window?`, [["yes", "Yes: pop it from the front"], ["no", "No: keep it"]], out1 ? "yes" : "no",
                `The front came from index ${dq[0]}, and the window starts at ${i - k + 1}.`);
              if (out1) dq.shift();
            }
            if (i >= k - 1) out[i - k + 1] = a[dq[0]];
          }
          ctx.draw(V.array(a), V.array(out, { label: "window max", small: true, idxText: (x) => `${x}..${x + k - 1}`, cls: () => "ok" }));
          return { summary: "The front is always the max. Each index enters and leaves once, so it's O(n) instead of O(n·k)." };
        },
      },
      {
        id: "hits", name: "Hits in the last 10 seconds",
        blurb: "Count hits in the last 10 seconds: the window (t − 10, t]. Hits join the back of a queue and expire from the front.",
        *play(ctx) {
          const times = [];
          let t = T.rand(1, 4);
          for (let i = 0; i < 7; i++) { times.push(t); t += T.pick([1, 2, 3, 4, 6, 9]); }
          const q = [];
          for (const now of times) {
            ctx.draw(V.line(h("strong", {}, `hit at t = ${now}`)),
              V.chips(q.map(String), { label: "queue of hit times", ends: ["front", "back"], empty: "empty" }));
            let drop = 0;
            while (drop < q.length && q[drop] <= now - 10) drop++;
            yield T.choose("How many old hits expire from the front?", T.numOptions(drop, { spread: 2 }), drop,
              `Only hits after ${now - 10} still count. ${drop ? `${q.slice(0, drop).join(", ")} ${drop > 1 ? "are" : "is"} too old.` : "Everything in the queue is recent enough."}`);
            q.splice(0, drop);
            q.push(now);
          }
          ctx.draw(V.chips(q.map(String), { label: "final queue", cls: () => "ok", ends: ["front", "back"] }), V.line(`${q.length} hits in the last 10 seconds.`));
          return { summary: "Times only go up, so old hits are always at the front. Expiring is popleft in a loop." };
        },
      },
    ],
  });

  // ── 14 Linked lists ──────────────────────────────────────────────────────
  function llist(vals, next, o = {}) {
    const n = vals.length, gap = 112, bw = 64, bh = 38, x0 = 20, y0 = 24;
    const els = [];
    const cx = (i) => x0 + i * gap;
    for (let i = 0; i < n; i++) {
      const j = next[i];
      const sx = cx(i) + bw - 10, sy = y0 + bh / 2;
      if (j == null) {
        if (o.showNull !== false) els.push(s("text", { class: "lnull", x: cx(i) + bw - 10, y: y0 + bh + 16 }, "None"));
      } else if (j === i + 1) {
        els.push(s("path", { class: "larrow", d: `M${sx} ${sy} L${cx(j) - 4} ${sy}`, "marker-end": "url(#larr)" }));
      } else {
        const tx = cx(j) + bw / 2, dip = 36 + Math.abs(j - i) * 8;
        const below = j < i;
        const ty = below ? y0 + bh : y0;
        els.push(s("path", { class: "larrow", d: `M${sx} ${below ? y0 + bh : y0} C ${sx} ${below ? y0 + bh + dip : y0 - dip}, ${tx} ${below ? ty + dip : ty - dip}, ${tx} ${ty + (below ? 3 : -3)}`, "marker-end": "url(#larr)" }));
      }
    }
    for (let i = 0; i < n; i++) {
      const pickable = o.pick;
      els.push(s("g", { class: "lnode " + (o.cls ? o.cls(i) : "") + (pickable ? " pickable" : ""), "data-pick": pickable ? String(i) : null, tabindex: pickable ? "0" : null, role: pickable ? "button" : null },
        s("rect", { x: cx(i), y: y0, width: bw, height: bh, rx: 6 }),
        s("rect", { class: "nextbox", x: cx(i) + bw - 20, y: y0, width: 20, height: bh, rx: 0 }),
        s("text", { x: cx(i) + (bw - 20) / 2, y: y0 + bh / 2, dy: "0.35em" }, vals[i]),
        s("circle", { cx: cx(i) + bw - 10, cy: y0 + bh / 2, r: 3, fill: "currentColor" })));
    }
    const names = Object.keys(o.ptr || {});
    const tones = ["a", "b", "c", "d"];
    const stack = {};
    names.forEach((name, k) => {
      const i = o.ptr[name];
      if (i == null) return;
      stack[i] = (stack[i] || 0) + 1;
      els.push(s("text", { class: "lptr t-" + tones[k % 4], x: cx(i) + (bw - 20) / 2, y: y0 + bh + 58 + (stack[i] - 1) * 16 }, name));
    });
    const W = x0 * 2 + (n - 1) * gap + bw + 20, H = y0 + bh + 60 + names.length * 16;
    const defs = s("defs", {}, s("marker", { id: "larr", viewBox: "0 0 10 10", refX: "8", refY: "5", markerWidth: "7", markerHeight: "7", orient: "auto-start-reverse" }, s("path", { d: "M0,0 L10,5 L0,10 z", class: "arrowhead" })));
    return h("figure", { class: "svgfig llist" }, s("svg", { viewBox: `0 -40 ${W} ${H + 40}`, width: W }, defs, els));
  }

  T.topic({
    id: "linked-lists", n: 14, stage: STAGE,
    title: "Linked lists",
    idea: "A node only knows its next node. Every operation is pointer surgery: save what you're about to lose before you cut a link. Two pointers moving at different speeds find middles and cycles without counting.",
    signals: "Reversing, merging, removing the nth node from the end, finding the middle, or detecting a cycle.",
    invariant: "Every node you still need is reachable from some variable. Lose the only reference and that part of the list is gone.",
    drills: [
      {
        id: "reverse", name: "Reverse it",
        blurb: "Reverse the list in place with prev, curr and nxt. Each round runs four lines, and the order is the whole trick.",
        *play(ctx) {
          const n = T.rand(4, 5);
          const vals = T.distinct(n, 1, 9);
          const next = vals.map((_, i) => (i + 1 < n ? i + 1 : null));
          let prev = null, curr = 0, nxt = undefined;
          const OPS = [["save", "nxt = curr.next"], ["flip", "curr.next = prev"], ["prev", "prev = curr"], ["curr", "curr = nxt"], ["done", "return prev"]];
          const name = (i) => (i == null ? "None" : vals[i]);
          let phase = 0;
          for (;;) {
            ctx.draw(
              llist(vals, next, { ptr: { prev, curr, nxt: nxt === undefined ? null : nxt }, cls: (i) => (i === curr ? "hot" : "") }),
              V.line(`prev = ${name(prev)}   curr = ${name(curr)}   nxt = ${nxt === undefined ? "not set" : name(nxt)}`),
              V.code("while curr:\n    ?\n    ?\n    ?\n    ?\nreturn ?"));
            const want = curr == null ? "done" : OPS[phase][0];
            yield T.ask({
              prompt: curr == null ? "curr is None. What now?" : "Which line runs next?",
              options: OPS.map(([v, label]) => ({ value: v, label: h("code", {}, label) })),
              answer: want,
              why: (v) => {
                if (want === "done") return v === "flip" || v === "save" ? "curr is None. There's no node left to work on." : "The loop is over. prev points at the old tail, which is the new head.";
                if (v === "done") return "curr still points at a node, so there's more list to flip.";
                if (want === "save") {
                  if (v === "flip") return `If ${name(curr)}.next points back now, nothing points to ${name(next[curr])} any more and the rest of the list is lost. Save it first.`;
                  return "Moving a pointer now skips this node's flip. Save the next node first.";
                }
                if (want === "flip") {
                  if (v === "save") return "nxt is already saved.";
                  if (v === "prev") return "If prev moves to curr first, curr.next = prev would point the node at itself.";
                  return "curr would move on before its link is flipped.";
                }
                if (want === "prev") {
                  if (v === "curr") return "If curr moves first, you've lost the node prev is supposed to move to.";
                  return "This node is already saved and flipped. Advance the pointers: prev first.";
                }
                return "prev has moved. Now curr steps forward to the saved nxt.";
              },
            });
            if (want === "done") break;
            if (want === "save") nxt = next[curr];
            if (want === "flip") next[curr] = prev;
            if (want === "prev") prev = curr;
            if (want === "curr") { curr = nxt; nxt = undefined; }
            phase = (phase + 1) % 4;
          }
          ctx.draw(llist(vals, next, { ptr: { head: prev }, cls: () => "ok" }));
          return { summary: "Save, flip, advance, advance. Saving first is what keeps the rest of the list alive." };
        },
      },
      {
        id: "fast-slow", name: "Fast and slow",
        blurb: "slow moves 1 step, fast moves 2. Run them in your head, then click your prediction.",
        *play(ctx) {
          const n = T.rand(5, 9);
          const vals = T.range(n, 1);
          const next = vals.map((_, i) => (i + 1 < n ? i + 1 : null));
          const code = V.code("slow = fast = head\nwhile fast and fast.next:\n    slow = slow.next\n    fast = fast.next.next\nreturn slow");
          ctx.draw(llist(vals, next, { pick: true, ptr: { "slow, fast": 0 } }), code);
          const mid = n >> 1;
          yield T.click(`${n} nodes. Where is slow when the loop ends? Click it.`, String(mid),
            `fast covers twice the distance, so when it reaches the end, slow is halfway: index ${n} // 2.${n % 2 === 0 ? " With an even count, that's the second of the two middles." : ""}`,
            `slow stops at ${vals[mid]}.${n % 2 === 0 ? " Even count, so it's the second middle." : ""}`);

          const m = T.rand(5, 8), hasCycle = Math.random() < 0.75;
          const v2 = T.range(m, 1);
          const nx2 = v2.map((_, i) => (i + 1 < m ? i + 1 : null));
          const c = T.rand(0, m - 3);
          if (hasCycle) nx2[m - 1] = c;
          let sl = 0, fa = 0, meet = null;
          for (let guard = 0; guard < 100; guard++) {
            sl = nx2[sl];
            const f1 = nx2[fa];
            if (f1 == null || nx2[f1] == null) break;
            fa = nx2[f1];
            if (sl === fa) { meet = sl; break; }
          }
          ctx.draw(llist(v2, nx2, { pick: true, ptr: { "slow, fast": 0 } }),
            V.code("slow = fast = head\nwhile fast and fast.next:\n    slow = slow.next\n    fast = fast.next.next\n    if slow is fast:\n        return slow   # they met"));
          yield T.ask({
            prompt: "Now cycle detection. Click the node where they first meet, or…",
            picks: true, options: [["none", "They never meet"]],
            answer: meet == null ? "none" : String(meet),
            why: (v) => (meet == null ? "There's no cycle. fast runs off the end and the loop stops." : v === "none" ? "Follow the arrow from the last node: there's a loop, and in a loop fast gains one step on slow every round, so it must catch up." : "Step them one round at a time: slow +1, fast +2, and compare after each round."),
            note: meet == null ? "No cycle, so fast reaches None." : `They meet at ${v2[meet]}.`,
          });
          return { summary: "Inside a cycle, the gap between them shrinks by one each round, so they always meet, within one lap." };
        },
      },
    ],
  });

  // ── 15 Trees ─────────────────────────────────────────────────────────────
  function bstFrom(values) {
    let root = null, id = 0;
    const insert = (v) => {
      const node = { id: id++, val: v, left: null, right: null };
      if (!root) { root = node; return node; }
      let cur = root;
      for (;;) {
        const side = v < cur.val ? "left" : "right";
        if (!cur[side]) { cur[side] = node; return node; }
        cur = cur[side];
      }
    };
    values.forEach(insert);
    return { root, insert };
  }
  const nodesOf = (root) => { const out = []; (function w(n) { if (!n) return; out.push(n); w(n.left); w(n.right); })(root); return out; };
  const depthOf = (n) => (n ? 1 + Math.max(depthOf(n.left), depthOf(n.right)) : 0);
  function shapedTree(count) {
    for (;;) {
      const { root } = bstFrom(T.shuffle(T.range(count, 1)));
      const d = depthOf(root);
      if (d >= 3 && d <= 4) return root;
    }
  }
  function orderOf(root, mode) {
    const out = [];
    if (mode === "level") {
      const q = [root];
      while (q.length) { const n = q.shift(); out.push(n); if (n.left) q.push(n.left); if (n.right) q.push(n.right); }
      return out;
    }
    (function w(n) {
      if (!n) return;
      if (mode === "pre") out.push(n);
      w(n.left);
      if (mode === "in") out.push(n);
      w(n.right);
      if (mode === "post") out.push(n);
    })(root);
    return out;
  }
  const MODES = {
    pre: ["preorder", "Preorder: the node first, then its whole left subtree, then its whole right subtree."],
    in: ["inorder", "Inorder: the whole left subtree, then the node, then the right subtree. Go left as far as you can first."],
    post: ["postorder", "Postorder: a node comes only after both of its subtrees are completely done."],
    level: ["level order", "Level order: row by row from the top, left to right within each row."],
  };

  T.topic({
    id: "trees", n: 15, stage: STAGE,
    title: "Trees",
    idea: "Every tree problem is \"what do I need from my children, and what do I hand to my parent?\" Ask that and the recursion writes itself. Traversal order decides when a node does its work: before its children, between them, or after them.",
    signals: "Hierarchies, depth or height, paths from root to leaf, \"for every subtree\", or level-by-level questions.",
    invariant: "In a postorder computation, a node's answer is built only from its children's finished answers.",
    drills: [
      {
        id: "traverse", name: "Walk the order",
        blurb: "Click every node in the order the traversal visits it.",
        *play(ctx) {
          const root = shapedTree(T.rand(6, 8));
          const labels = T.shuffle(T.letters.slice(0, 8).split(""));
          nodesOf(root).forEach((n, i) => (n.label = labels[i]));
          const mode = T.pick(Object.keys(MODES));
          const seq = orderOf(root, mode);
          const pos = new Map();
          for (let k = 0; k < seq.length; k++) {
            ctx.draw(V.line(h("strong", {}, MODES[mode][0])),
              V.btree(root, { label: (n) => n.label, pick: (n) => !pos.has(n), cls: (n) => (pos.has(n) ? "ok" : ""), badge: (n) => (pos.has(n) ? pos.get(n) : null) }),
              V.line("so far: ", V.k(seq.slice(0, k).map((n) => n.label).join(" ") || "nothing")));
            yield T.click(k === 0 ? `Click the first node in ${MODES[mode][0]}.` : "Next node?", String(seq[k].id), MODES[mode][1]);
            pos.set(seq[k], k + 1);
          }
          ctx.draw(V.line(h("strong", {}, MODES[mode][0])), V.btree(root, { label: (n) => n.label, cls: () => "ok", badge: (n) => pos.get(n) }),
            V.line("order: ", V.k(seq.map((n) => n.label).join(" "))));
          return { summary: "Pre = act before the children, in = between them, post = after them. Level order uses a queue instead of recursion." };
        },
      },
      {
        id: "bottom-up", name: "Bottom-up answers",
        blurb: "Height of a node = 1 + the taller child's height (an empty child is 0). Fill in heights in postorder. Each answer only needs the children's.",
        *play(ctx) {
          const root = shapedTree(T.rand(6, 8));
          const labels = T.shuffle(T.letters.slice(0, 8).split(""));
          nodesOf(root).forEach((n, i) => (n.label = labels[i]));
          const ht = new Map();
          const post = orderOf(root, "post");
          const asked = post.filter((n) => n.left || n.right);
          for (const n of post) if (!n.left && !n.right) ht.set(n, 1);
          for (const n of asked) {
            ctx.draw(V.btree(root, { label: (x) => x.label, cls: (x) => (x === n ? "hot" : ht.has(x) ? "ok" : ""), badge: (x) => (ht.has(x) ? `h${ht.get(x)}` : null) }),
              V.line("Leaves are height 1. Badges show finished heights."));
            const hl = n.left ? ht.get(n.left) : 0, hr = n.right ? ht.get(n.right) : 0;
            const val = 1 + Math.max(hl, hr);
            yield T.choose(`Height of ${n.label}?`, T.numOptions(val, { spread: 2, min: 1, extra: [hl + hr + 1, Math.max(hl, hr)] }), val,
              `1 + max(left ${hl}, right ${hr}) = ${val}.`, null);
            ht.set(n, val);
          }
          const through = (x) => (x.left ? ht.get(x.left) : 0) + (x.right ? ht.get(x.right) : 0);
          const best = Math.max(...post.map(through));
          ctx.draw(V.btree(root, { label: (x) => x.label, pick: () => true, cls: () => "", badge: (x) => `h${ht.get(x)}` }),
            V.line("The longest path between any two nodes bends at one node: it runs down that node's left side and down its right side."));
          yield T.ask({
            prompt: "Click the node where the longest path bends.",
            picks: true,
            answer: post.filter((x) => through(x) === best).map((x) => String(x.id)),
            why: (v) => {
              const x = post.find((p) => String(p.id) === v);
              return `Through ${x.label}: left height ${x.left ? ht.get(x.left) : 0} + right height ${x.right ? ht.get(x.right) : 0} = ${through(x)} edges. Some node does better.`;
            },
            note: `Diameter = ${best} edges = the largest left height + right height at any node.`,
          });
          return { summary: "One postorder pass gives both: return the height to the parent, and keep the best left + right as you go." };
        },
      },
    ],
  });

  // ── 16 Binary search trees ───────────────────────────────────────────────
  function boundsOf(root, target) {
    let lo = -Infinity, hi = Infinity, cur = root;
    while (cur && cur !== target) {
      if (cur.left && nodesOf(cur.left).includes(target)) { hi = cur.val; cur = cur.left; }
      else { lo = cur.val; cur = cur.right; }
    }
    return [lo, hi];
  }
  function brokenBst() {
    for (let tries = 0; tries < 200; tries++) {
      const vals = T.distinct(T.rand(7, 9), 1, 60);
      const { root } = bstFrom(vals);
      if (depthOf(root) < 3 || depthOf(root) > 5) continue;
      if (Math.random() < 0.25) return { root, culprit: null };
      const all = nodesOf(root);
      const parentOf = new Map();
      for (const n of all) { if (n.left) parentOf.set(n.left, n); if (n.right) parentOf.set(n.right, n); }
      const leaves = T.shuffle(all.filter((n) => !n.left && !n.right && parentOf.has(n) && parentOf.has(parentOf.get(n))));
      for (const leaf of leaves) {
        const [lo, hi] = boundsOf(root, leaf);
        const isLeft = parentOf.get(leaf).left === leaf;
        let v = null;
        if (isLeft && lo > -Infinity) v = lo - T.rand(1, 4);
        if (!isLeft && hi < Infinity) v = hi + T.rand(1, 4);
        if (v == null || v < 1 || all.some((n) => n.val === v)) continue;
        leaf.val = v;
        return { root, culprit: leaf };
      }
    }
    return { root: bstFrom([30, 15, 45, 8, 20, 40, 50]).root, culprit: null };
  }

  T.topic({
    id: "bst", n: 16, stage: STAGE,
    title: "Binary search trees",
    idea: "Every node splits the world: smaller to the left, bigger to the right, all the way down. So a search is one comparison per level, and an inorder walk reads the values in sorted order.",
    signals: "Sorted data that changes (inserts and deletes), \"kth smallest\", floor or ceiling, validating structure, or range queries.",
    invariant: "Each node lives inside an interval set by all of its ancestors, not just its parent.",
    drills: [
      {
        id: "insert", name: "Insert by walking",
        blurb: "Insert each new value. At every node, go left or right until you fall off the tree. That's where it goes.",
        *play(ctx) {
          const { root, insert } = bstFrom(T.distinct(6, 10, 90));
          const pool = T.distinct(10, 1, 99).filter((v) => !nodesOf(root).some((n) => n.val === v));
          for (const v of pool.slice(0, 3)) {
            let cur = root;
            const path = [];
            for (;;) {
              ctx.draw(V.line("insert ", h("strong", {}, v)), V.btree(root, { cls: (n) => (n === cur ? "hot" : path.includes(n) ? "ok" : "") }));
              const dir = v < cur.val ? "left" : "right";
              yield T.choose(`At ${cur.val}. Which way?`, [["left", "Go left"], ["right", "Go right"]], dir,
                `${v} ${v < cur.val ? "<" : ">"} ${cur.val}, so it belongs in the ${dir} subtree.`,
                cur[dir] ? null : `${cur.val} has no ${dir} child, so ${v} goes there.`);
              path.push(cur);
              if (!cur[dir]) break;
              cur = cur[dir];
            }
            const added = insert(v);
            ctx.draw(V.line("insert ", h("strong", {}, v)), V.btree(root, { cls: (n) => (n === added ? "ok" : "") }));
          }
          return { summary: "Insertion is a failed search: walk as if looking for the value, and put it where the walk falls off." };
        },
      },
      {
        id: "broken", name: "Spot the broken tree",
        blurb: "Some of these trees break the BST rule. Usually the culprit looks fine next to its parent and only breaks a rule set further up.",
        *play(ctx) {
          for (let round = 0; round < 2; round++) {
            const { root, culprit } = brokenBst();
            ctx.draw(V.btree(root, { pick: () => true }));
            yield T.ask({
              prompt: "Click the node that breaks the BST rule, or…",
              picks: true, options: [["valid", "It's a valid BST"]],
              answer: culprit ? String(culprit.id) : "valid",
              why: (v) => {
                if (v === "valid") return "One node breaks a rule set by an ancestor further up, not by its parent.";
                const n = nodesOf(root).find((x) => String(x.id) === v);
                const [lo, hi] = boundsOf(root, n);
                return `${n.val} is fine: its ancestors only require ${lo === -Infinity ? "−∞" : lo} < ${n.val} < ${hi === Infinity ? "∞" : hi}.`;
              },
              note: () => {
                if (!culprit) return "Valid: every node sits within the bounds its ancestors set.";
                const [lo, hi] = boundsOf(root, culprit);
                return `${culprit.val} must be between ${lo === -Infinity ? "−∞" : lo} and ${hi === Infinity ? "∞" : hi}, because of an ancestor higher up.`;
              },
            });
            ctx.draw(V.btree(root, { cls: (n) => (n === culprit ? "bad" : "ok") }));
            if (round === 0) yield T.choose("Next tree?", [["go", "Next tree"]], "go");
          }
          return { summary: "Validate by passing down (low, high) bounds. Checking only parent and child misses the deep violations." };
        },
      },
      {
        id: "kth", name: "Kth smallest",
        blurb: "An inorder walk visits a BST in sorted order. Use that to find the kth smallest without sorting anything.",
        *play(ctx) {
          for (let round = 0; round < 2; round++) {
            const { root } = bstFrom(T.distinct(T.rand(7, 9), 1, 60));
            const sorted = orderOf(root, "in");
            const k = T.rand(2, sorted.length - 1);
            ctx.draw(V.btree(root, { pick: () => true }));
            yield T.click(`Click the ${k}${["th", "st", "nd", "rd"][k] || "th"} smallest value.`, String(sorted[k - 1].id),
              "Walk inorder (left subtree, node, right subtree) and count. Start at the leftmost node: that's 1st.",
              `${sorted[k - 1].val} is #${k}.`);
            ctx.draw(V.btree(root, { cls: (n) => (n === sorted[k - 1] ? "ok" : ""), badge: (n) => sorted.indexOf(n) + 1 }));
            if (round === 0) yield T.choose("Ranks shown. Next tree?", [["go", "Next tree"]], "go");
          }
          return { summary: "Iterative inorder with a stack can stop the moment it has counted k nodes." };
        },
      },
    ],
  });

  // ── 17 Heaps ─────────────────────────────────────────────────────────────
  function heapTree(a) {
    const nodes = a.map((v, i) => ({ id: i, val: v, left: null, right: null }));
    nodes.forEach((n, i) => { n.left = nodes[2 * i + 1] || null; n.right = nodes[2 * i + 2] || null; });
    return nodes[0] || null;
  }
  function heapify(a) {
    const sift = (i) => {
      for (;;) {
        const l = 2 * i + 1, r = l + 1;
        let m = i;
        if (l < a.length && a[l] < a[m]) m = l;
        if (r < a.length && a[r] < a[m]) m = r;
        if (m === i) return;
        [a[i], a[m]] = [a[m], a[i]];
        i = m;
      }
    };
    for (let i = (a.length >> 1) - 1; i >= 0; i--) sift(i);
    return a;
  }

  T.topic({
    id: "heaps", n: 17, stage: STAGE,
    title: "Heaps",
    idea: "A heap is only partly sorted: each parent is no bigger than its children, so the minimum sits on top. That's enough to get the next-best item in O(log n), which is all most problems need.",
    signals: "\"k largest\", \"k closest\", \"next smallest\", merging k sorted lists, scheduling by priority, or running medians.",
    invariant: "parent ≤ child, everywhere. Siblings can be in any order.",
    drills: [
      {
        id: "sift", name: "Push and pop",
        blurb: "Min-heap, stored as an array: the children of i sit at 2i+1 and 2i+2. A push bubbles up, and a pop moves the last item to the top and sinks it.",
        *play(ctx) {
          const a = heapify(T.distinct(6, 10, 60));
          const draw = (hot, extra) => ctx.draw(
            V.btree(heapTree(a), { cls: (n) => (n.id === hot ? "hot" : extra && extra(n.id) ? "pa" : ""), badge: (n) => n.id }),
            V.array(a, { small: true, cls: (i) => (i === hot ? "hot" : "") }));
          const pushes = T.distinct(2, 1, 40).filter((v) => !a.includes(v));
          for (const v of pushes) {
            a.push(v);
            let i = a.length - 1;
            for (;;) {
              const p = (i - 1) >> 1;
              draw(i, (id) => i > 0 && id === p);
              const ans = i > 0 && a[i] < a[p] ? "swap" : "stop";
              yield T.choose(`Pushing ${v}: it's at index ${i}.`, [["swap", "Swap with parent"], ["stop", "Stop here"]], ans,
                i === 0 ? "It's at the root. There's nothing above it." : ans === "swap" ? `${a[i]} < its parent ${a[p]}, and a parent must be ≤ its children.` : `${a[i]} ≥ its parent ${a[p]}, so heap order already holds.`);
              if (ans === "stop") break;
              [a[i], a[p]] = [a[p], a[i]];
              i = p;
            }
          }
          const min = a[0];
          a[0] = a.pop();
          let i = 0;
          for (;;) {
            const l = 2 * i + 1, r = l + 1;
            draw(i, (id) => id === l || id === r);
            let c = null;
            if (l < a.length) c = l;
            if (r < a.length && a[r] < a[l]) c = r;
            const ans = c != null && a[c] < a[i] ? (c === l ? "left" : "right") : "stop";
            yield T.choose(`Popped ${min}. The last item (${a[i]}) moved to the top and has to sink. At index ${i}:`,
              [["left", "Swap with left child"], ["right", "Swap with right child"], ["stop", "Stop here"]], ans, (v) => {
                if (v !== "stop" && (v === "left" ? l : r) >= a.length) return "There's no child there.";
                if (ans === "stop") return `${a[i]} is already ≤ its children.`;
                if (v === "stop") return `${a[i]} is bigger than its child ${a[c]}, which breaks parent ≤ child.`;
                const other = v === "left" ? r : l;
                return `Swapping with ${a[v === "left" ? l : r]} would put it above ${a[other]}, its new child, and break the order. Swap with the smaller child.`;
              });
            if (ans === "stop") break;
            [a[i], a[c]] = [a[c], a[i]];
            i = c;
          }
          draw(-1);
          return { summary: "At most one swap per level, and there are log n levels. Sinking always swaps with the smaller child." };
        },
      },
      {
        id: "top-k", name: "Keep the top 3",
        blurb: "A stream of numbers arrives. Keep the 3 largest so far, using a min-heap of size 3. Its top is the weakest member, the one to kick out.",
        *play(ctx) {
          const k = 3, stream = T.distinct(9, 1, 50);
          const heap = [];
          for (const x of stream) {
            const sorted = heap.slice().sort((p, q) => p - q);
            ctx.draw(V.line("next: ", h("strong", {}, x)),
              V.chips(sorted.map(String), { label: `min-heap (size ≤ ${k}), smallest marked`, cls: (i) => (i === 0 ? "hot" : ""), empty: "empty" }),
              V.chips(stream.slice(0, stream.indexOf(x)).map(String), { label: "seen so far", cls: () => "dim", empty: "none yet" }));
            const min = sorted[0];
            const ans = heap.length < k ? "push" : x > min ? "replace" : "ignore";
            yield T.choose("Your move:", [["push", `Push ${x}`], ["replace", `Push ${x}, pop the min`], ["ignore", `Ignore ${x}`]], ans, (v) => {
              if (ans === "push") return `Fewer than ${k} so far, so keep everything.`;
              if (v === "push") return `The heap already holds ${k}. Adding without removing would keep ${k + 1}.`;
              if (ans === "replace") return `${x} beats the weakest of your top ${k} (${min}). It belongs in, and ${min} goes out.`;
              return `${x} is smaller than everything in your top ${k}, so it can't be one of the ${k} largest.`;
            }, ans === "replace" ? `${min} drops out.` : null);
            if (ans === "push") heap.push(x);
            else if (ans === "replace") { heap.splice(heap.indexOf(min), 1); heap.push(x); }
          }
          const sorted = heap.slice().sort((p, q) => p - q);
          ctx.draw(V.chips(sorted.map(String), { label: "final heap", cls: (i) => (i === 0 ? "hot" : "ok") }));
          yield T.choose(`What's the ${k}rd largest of the whole stream?`, T.shuffle([...new Set([sorted[0], sorted[2], sorted[1], Math.max(...stream.filter((v) => !heap.includes(v)))])]), sorted[0],
            "The top of the min-heap: the smallest of the k largest is exactly the kth largest.");
          return { summary: "k largest needs a min-heap, and k smallest needs a max-heap. It feels backwards until you see the top as the bouncer." };
        },
      },
    ],
  });

  // ── 18 Tries ─────────────────────────────────────────────────────────────
  const WORDSETS = [
    ["car", "cat", "cart", "care", "do", "dog", "dot", "card"],
    ["tea", "ten", "team", "to", "toe", "top", "tent", "tip"],
    ["in", "ink", "inn", "tin", "tip", "tick", "it", "ion"],
    ["sun", "sum", "sunk", "see", "seed", "set", "sea", "sunny"],
  ];
  function makeTrie() {
    const root = { ch: "", path: "", kids: new Map(), end: false };
    const insert = (w) => {
      let cur = root, made = [];
      for (const c of w) {
        if (!cur.kids.has(c)) { const n = { ch: c, path: cur.path + c, kids: new Map(), end: false }; cur.kids.set(c, n); made.push(n); }
        cur = cur.kids.get(c);
      }
      cur.end = true;
      return made;
    };
    const depthHave = (w) => { let cur = root, d = 0; for (const c of w) { if (!cur.kids.has(c)) break; cur = cur.kids.get(c); d++; } return d; };
    const find = (p) => { let cur = root; for (const c of p) { cur = cur.kids.get(c); if (!cur) return null; } return cur; };
    return { root, insert, depthHave, find };
  }
  const trieKids = (n) => [...n.kids.values()].sort((a, b) => a.ch.localeCompare(b.ch));
  const countEnds = (n) => (n.end ? 1 : 0) + trieKids(n).reduce((s2, k) => s2 + countEnds(k), 0);
  const drawTrie = (tr, o = {}) => V.ntree([tr.root], {
    kids: trieKids, label: (n) => n.ch || "·", key: (n) => "t:" + n.path,
    pick: o.pick, cls: (n) => [n.end ? "end" : "", o.cls ? o.cls(n) : ""].join(" "), gap: 40, dy: 54, r: 15,
  });

  T.topic({
    id: "tries", n: 18, stage: STAGE,
    title: "Tries",
    idea: "A trie stores words letter by letter along shared paths. Words that share a prefix share nodes, so \"anything starting with ca?\" is just a walk down three edges.",
    signals: "Prefix queries, autocomplete, \"replace words by their root\", word search over a grid, or many lookups against one dictionary.",
    invariant: "The path from the root to any node spells a prefix. A word ends wherever a node is marked as an end (thick ring).",
    drills: [
      {
        id: "insert", name: "How many new nodes?",
        blurb: "Insert words one at a time. Predict how many nodes each insert creates: only the part beyond the longest prefix already in the trie.",
        *play(ctx) {
          const words = T.shuffle(T.pick(WORDSETS)).slice(0, 7);
          const tr = makeTrie();
          tr.insert(words[0]); tr.insert(words[1]);
          let fresh = [];
          for (const w of words.slice(2)) {
            ctx.draw(V.line("insert ", h("strong", {}, `"${w}"`)), drawTrie(tr, { cls: (n) => (fresh.includes(n) ? "ok" : "") }),
              V.line("words so far: ", V.k(words.slice(0, words.indexOf(w)).join(", "))));
            const have = tr.depthHave(w), need = w.length - have;
            yield T.choose(`How many new nodes does "${w}" need?`, T.numOptions(need, { spread: 2, extra: [w.length] }), need,
              have === w.length ? `The whole path "${w}" already exists. Inserting just marks its last node as a word end.` : `"${w.slice(0, have)}" already exists${have ? "" : " (nothing does)"}, so only "${w.slice(have)}" needs new nodes.`,
              have === w.length ? "Zero new nodes, just a new end mark." : null);
            fresh = tr.insert(w);
          }
          ctx.draw(drawTrie(tr, { cls: (n) => (fresh.includes(n) ? "ok" : "") }));
          return { summary: "Shared prefixes are stored once. That's where both the memory savings and the fast prefix queries come from." };
        },
      },
      {
        id: "prefix", name: "Count by prefix",
        blurb: "Find where a prefix ends, then count the words below it. Thick rings mark word ends.",
        *play(ctx) {
          const words = T.pick(WORDSETS);
          const tr = makeTrie();
          words.forEach(tr.insert);
          const prefixes = [];
          for (const w of T.shuffle(words)) {
            const p = w.slice(0, T.rand(1, Math.min(3, w.length)));
            if (!prefixes.includes(p)) prefixes.push(p);
            if (prefixes.length === 2) break;
          }
          for (const p of prefixes) {
            ctx.draw(V.line("prefix ", h("strong", {}, `"${p}"`)), drawTrie(tr, { pick: () => true }));
            yield T.click(`Click the node where "${p}" ends.`, "t:" + p, `Start at the root and follow the letters: ${p.split("").join(" → ")}.`);
            const node = tr.find(p), c = countEnds(node);
            const under = (n) => n.path.startsWith(p);
            ctx.draw(V.line("prefix ", h("strong", {}, `"${p}"`)), drawTrie(tr, { cls: (n) => (n === node ? "hot" : under(n) ? "pa" : "") }));
            yield T.choose(`How many words start with "${p}"?`, T.numOptions(c, { spread: 2, min: 1 }), c,
              `Count the thick rings at "${p}" and below it, including "${p}" itself if it's a word.`,
              `${words.filter((w) => w.startsWith(p)).join(", ")}`);
          }
          return { summary: "Store a counter on each node during insert, and \"how many words have this prefix\" becomes a walk plus one read." };
        },
      },
    ],
  });
})();
