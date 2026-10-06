"use strict";
(function () {
  const T = window.Trace;
  const { h, V } = T;
  const STAGE = "Core patterns";
  const sum = (a) => a.reduce((x, y) => x + y, 0);

  // ── 06 Two pointers ──────────────────────────────────────────────────────
  function pairInstance() {
    for (;;) {
      const n = T.rand(8, 10);
      const a = T.distinct(n, 1, 32).sort((x, y) => x - y);
      const p = T.rand(0, n - 3), q = T.rand(p + 1, n - 1);
      const t = a[p] + a[q];
      let pairs = 0;
      for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) if (a[i] + a[j] === t) pairs++;
      if (pairs === 1 && (p > 1 || q < n - 2)) return { a, t };
    }
  }

  T.topic({
    id: "two-pointers", n: 6, stage: STAGE,
    title: "Two pointers",
    idea: "With sorted data, one comparison tells you which end can never be part of the answer. Drop that end and you never need to look at it again, so n² pairs collapse into n steps.",
    signals: "Sorted input, pairs or triples with a target sum, \"in place\", or comparing from both ends (palindromes, containers).",
    invariant: "Everything outside [L, R] has been ruled out for good. The answer, if there is one, is still inside.",
    drills: [
      {
        id: "pair-sum", name: "Pair sum",
        blurb: "Find the two numbers that add up to the target. L starts at the smallest, R at the biggest. You decide which one to move.",
        *play(ctx) {
          const { a, t } = pairInstance();
          let l = 0, r = a.length - 1;
          for (;;) {
            const s = a[l] + a[r];
            ctx.draw(
              V.line(h("strong", {}, `target = ${t}`)),
              V.array(a, { ptr: { L: l, R: r }, cls: (k) => (k < l || k > r ? "dim" : k === l || k === r ? "hot" : "") }),
              V.line(`a[L] + a[R] = ${a[l]} + ${a[r]} = `, h("strong", {}, s)));
            const ans = s === t ? "found" : s < t ? "L" : "R";
            yield T.choose("Your move:", [["L", "Move L right"], ["R", "Move R left"], ["found", "Found it"]], ans, (v) => {
              if (s === t) return `${a[l]} + ${a[r]} is exactly ${t}.`;
              if (v === "found") return `${s} isn't ${t}.`;
              if (s < t) return `The sum is too small (${s} < ${t}). Moving R left picks a smaller number, so the sum can only shrink.`;
              return `The sum is too big (${s} > ${t}). Moving L right picks a bigger number, so the sum can only grow.`;
            }, s < t ? `${a[l]} is too small even with the biggest number left (${a[r]}), so no pair uses it. Drop it.`
              : s > t ? `${a[r]} is too big even with the smallest number left (${a[l]}), so no pair uses it. Drop it.` : null);
            if (s === t) break;
            if (s < t) l++; else r--;
          }
          ctx.draw(V.line(h("strong", {}, `target = ${t}`)), V.array(a, { ptr: { L: l, R: r }, cls: (k) => (k === l || k === r ? "ok" : "dim") }));
          return { summary: "Each step crossed out a whole row of pairs. That's why it takes n steps instead of n²." };
        },
      },
      {
        id: "water", name: "Most water",
        blurb: "Two walls hold water up to the shorter one: area = width × min(height). Start with the widest pair and move one wall inward each step.",
        *play(ctx) {
          const n = T.rand(8, 10);
          const a = Array.from({ length: n }, () => T.rand(1, 9));
          let l = 0, r = n - 1, best = 0, bestAt = null;
          while (l < r) {
            const lvl = Math.min(a[l], a[r]), area = lvl * (r - l);
            if (area > best) { best = area; bestAt = [l, r]; }
            ctx.draw(
              V.bars(a, { ptr: { L: l, R: r }, water: [l, r, lvl], cls: (i) => (i === l ? "pa" : i === r ? "pb" : i < l || i > r ? "dim" : "") }),
              V.line(`width ${r - l} × min(${a[l]}, ${a[r]}) = `, h("strong", {}, area), `   best so far: ${best}`));
            const ans = a[l] < a[r] ? "L" : a[l] > a[r] ? "R" : ["L", "R"];
            const short = Math.min(a[l], a[r]);
            yield T.choose("Which wall moves in?", [["L", "Move L right"], ["R", "Move R left"]], ans,
              `The water is capped by the shorter wall (${short}). Moving the taller wall makes the container narrower, and the cap stays at ${short} or drops, so every container that move leads to is worse. Move the shorter one.`,
              a[l] === a[r] ? "Equal walls: either can go, because neither can do better with a closer partner." : `The ${short}-high wall has had its widest possible container. Any partner closer in is narrower, so it's done.`);
            if (a[l] < a[r]) l++;
            else if (a[l] > a[r]) r--;
            else l++;
          }
          ctx.draw(V.bars(a, { water: [bestAt[0], bestAt[1], Math.min(a[bestAt[0]], a[bestAt[1]])], cls: (i) => (bestAt.includes(i) ? "pa" : "") }),
            V.line("Best container: ", h("strong", {}, best)));
          return { summary: `Best area ${best}. Moving the shorter wall is safe: it can never do better than the container you just measured.` };
        },
      },
    ],
  });

  // ── 07 Sliding window ────────────────────────────────────────────────────
  T.topic({
    id: "sliding-window", n: 7, stage: STAGE,
    title: "Sliding window",
    idea: "Keep a contiguous window and update it as it moves: add what enters on the right, remove what leaves on the left. Grow while the window is valid and shrink when it breaks.",
    signals: "\"Subarray\" or \"substring\" (contiguous!), plus longest, shortest, at most k, or without repeats.",
    invariant: "Both edges only ever move right, so the whole scan is O(n) even with a loop inside a loop.",
    drills: [
      {
        id: "no-repeat", name: "Longest without repeats",
        blurb: "Find the longest stretch with no repeated letter. Each step, either grow the window to take the next letter or shrink it from the left.",
        *play(ctx) {
          const n = T.rand(9, 11);
          const s = Array.from({ length: n }, () => T.pick("abcde".split("")));
          let l = 0, r = -1, best = 0, bestAt = [0, -1];
          while (r + 1 < n) {
            const c = s[r + 1];
            const win = s.slice(l, r + 1);
            const dup = win.indexOf(c);
            ctx.draw(
              V.array(s, { win: r >= l ? [l, r] : null, ptr: r >= l ? { L: l, R: r } : { L: l }, cls: (k) => (k === r + 1 ? "soft" : k < l ? "dim" : "") }),
              V.line(`window "${win.join("")}"   length ${win.length}   best ${best}`),
              V.line("next letter: ", V.k(c)));
            yield T.choose("Your move:", [["grow", `Grow: take "${c}"`], ["shrink", `Shrink: drop "${s[l] ?? ""}"`]], dup >= 0 ? "shrink" : "grow",
              dup >= 0 ? `"${c}" is already in the window (index ${l + dup}). Taking it now would create a repeat.` : `"${c}" isn't in the window, so it stays valid. Grow while you can.`,
              dup >= 0 ? `Dropped "${s[l]}".` + (s[l] === c ? " The old copy is gone, so the window is valid again." : ` "${c}" is still inside, so keep shrinking.`) : null);
            if (dup >= 0) l++;
            else {
              r++;
              if (r - l + 1 > best) { best = r - l + 1; bestAt = [l, r]; }
            }
          }
          ctx.draw(V.array(s, { win: bestAt, cls: (k) => (k >= bestAt[0] && k <= bestAt[1] ? "ok" : "") }), V.line("Longest: ", h("strong", {}, best)));
          return { summary: `Longest is ${best}. Speed-up: store each letter's last index and jump L straight past the old copy.` };
        },
      },
      {
        id: "min-len", name: "Shortest window reaching a sum",
        blurb: "All numbers are positive. Find the shortest window whose sum is at least the target. Grow until it's enough, then shrink while it stays enough.",
        *play(ctx) {
          const n = T.rand(8, 9);
          const a = Array.from({ length: n }, () => T.rand(1, 9));
          const t = T.rand(Math.max(...a) + 2, Math.max(Math.max(...a) + 3, Math.floor(sum(a) * 0.45)));
          let l = 0, r = -1, s = 0, best = Infinity, bestAt = null;
          for (;;) {
            if (s < t && r + 1 >= n) break;
            ctx.draw(
              V.line(h("strong", {}, `target = ${t}`)),
              V.array(a, { win: r >= l ? [l, r] : null, ptr: r >= l ? { L: l, R: r } : { L: l }, cls: (k) => (k < l ? "dim" : "") }),
              V.line(`window sum = ${s}   best length ${best === Infinity ? "none yet" : best}`));
            const ans = s >= t ? "shrink" : "grow";
            yield T.choose("Your move:", [["grow", "Grow right"], ["shrink", "Record, then shrink left"]], ans,
              ans === "shrink" ? `The sum (${s}) already reaches ${t}. Record this length, then shrink to look for something shorter.` : `${s} < ${t}. Dropping a number only makes it smaller. Grow first.`,
              ans === "shrink" ? `Length ${r - l + 1} works.` : null);
            if (ans === "shrink") {
              if (r - l + 1 < best) { best = r - l + 1; bestAt = [l, r]; }
              s -= a[l]; l++;
            } else { r++; s += a[r]; }
          }
          ctx.draw(V.line(h("strong", {}, `target = ${t}`)), V.array(a, { win: bestAt, cls: (k) => (bestAt && k >= bestAt[0] && k <= bestAt[1] ? "ok" : "") }),
            V.line("Shortest: ", h("strong", {}, best === Infinity ? "none" : best)));
          return { summary: "This only works because the numbers are positive. Growing always adds and shrinking always subtracts. With negatives, use prefix sums." };
        },
      },
    ],
  });

  // ── 08 Prefix sums ───────────────────────────────────────────────────────
  T.topic({
    id: "prefix-sums", n: 8, stage: STAGE,
    title: "Prefix sums",
    idea: "Store running totals once, and any range sum becomes one subtraction: sum(i..j) = P[j+1] − P[i]. Put the running totals in a hash map and you can count ranges with a target sum in one pass, even with negatives.",
    signals: "Many range-sum queries, \"subarray sums to k\", negatives that break sliding windows, or balancing left and right.",
    invariant: "P[k] is the sum of the first k numbers, nums[0..k−1]. P has n + 1 entries and P[0] = 0.",
    drills: [
      {
        id: "range", name: "Range sum in two lookups",
        blurb: "Answer each range query by subtracting two prefix cells. Click them in order.",
        *play(ctx) {
          const n = T.rand(7, 8);
          const a = Array.from({ length: n }, () => T.rand(-3, 9));
          const P = [0];
          for (const x of a) P.push(P[P.length - 1] + x);
          for (let q = 0; q < 3; q++) {
            const i = T.rand(q === 0 ? 1 : 0, n - 2), j = T.rand(i + 1, n - 1);
            const picked = [];
            const draw = (pick) => ctx.draw(
              V.line(h("strong", {}, `sum(nums[${i}..${j}])`), "   inclusive"),
              V.array(a, { label: "nums", cls: (k) => (k >= i && k <= j ? "hot" : "") }),
              V.array(P, { label: "P[k] = sum of the first k numbers", pick, key: (k) => "P" + k, cls: (k) => (picked.includes(k) ? "ok" : "") }));
            draw(true);
            yield T.click(`Click the prefix that covers everything up to and including index ${j}.`, "P" + (j + 1), (v) => {
              const k = Number(v.slice(1));
              if (k === j) return `P[${j}] is the sum of the first ${j} numbers, nums[0..${j - 1}]. It stops one short of nums[${j}].`;
              return `P[${k}] covers nums[0..${k - 1}]. You want everything up to nums[${j}].`;
            }, `P[${j + 1}] = ${P[j + 1]}`);
            picked.push(j + 1);
            draw(true);
            yield T.click(`Now click the prefix to subtract: everything before index ${i}.`, "P" + i, (v) => {
              const k = Number(v.slice(1));
              if (k === i + 1) return `P[${i + 1}] includes nums[${i}], which belongs inside the range.`;
              if (k === i - 1 && i > 0) return `P[${i - 1}] stops early, so nums[${i - 1}] would stay in the result even though it isn't in the range.`;
              return `You need the part before the range: nums[0..${i - 1}], which is P[${i}].`;
            }, `P[${j + 1}] − P[${i}] = ${P[j + 1]} − ${P[i]} = ${P[j + 1] - P[i]}`);
            picked.push(i);
            draw(false);
          }
          return { summary: "Off by one is the only danger. Read P[k] as \"the first k numbers\", then sum(i..j) = P[j+1] − P[i]." };
        },
      },
      {
        id: "count-k", name: "Count subarrays summing to k",
        blurb: "Walk with a running sum p. A subarray ending here sums to k exactly when some earlier running sum was p − k. A map counts how often each running sum has appeared.",
        *play(ctx) {
          let a, k, total;
          do {
            a = Array.from({ length: T.rand(7, 8) }, () => T.rand(-3, 5));
            k = T.rand(2, 6);
            total = 0;
            for (let i = 0; i < a.length; i++) { let s = 0; for (let j = i; j < a.length; j++) { s += a[j]; if (s === k) total++; } }
          } while (total < 1 || total > 4);
          const seen = new Map([[0, 1]]);
          let p = 0, found = 0;
          for (let i = 0; i < a.length; i++) {
            p += a[i];
            const need = p - k, c = seen.get(need) || 0;
            ctx.draw(
              V.line(h("strong", {}, `k = ${k}`), `   found so far: ${found}`),
              V.row(
                V.array(a, { ptr: { i }, cls: (x) => (x === i ? "hot" : x > i ? "" : "dim") }),
                V.kv([...seen.entries()].map(([s, t]) => [s, `seen ${t}×`]), { label: "running sum → times seen" })),
              V.line("running sum p = ", h("strong", {}, p)));
            if (i === 0) {
              yield T.choose("Which earlier running sum do you look up?", [["a", "p − k"], ["b", "k − p"], ["c", "p + k"], ["d", "k"]], "a",
                "If an earlier running sum q satisfies p − q = k, the numbers between sum to k. So q = p − k.", `Look up p − k = ${need}.`);
            }
            yield T.choose(`How many subarrays ending at index ${i} sum to ${k}?`, T.numOptions(c, { spread: 2 }), c,
              `Look up p − k = ${p} − ${k} = ${need}. The map says it's been seen ${c} time${c === 1 ? "" : "s"}, and each one is a start point.`,
              c ? `${need} was seen ${c}×, so ${c} subarray${c > 1 ? "s" : ""} end here.` : `${need} hasn't appeared, so none end here.`);
            found += c;
            seen.set(p, (seen.get(p) || 0) + 1);
          }
          return { summary: `${found} subarrays in one pass. Seed the map with {0: 1} so that subarrays starting at index 0 count too.` };
        },
      },
    ],
  });

  // ── 09 Binary search ─────────────────────────────────────────────────────
  T.topic({
    id: "binary-search", n: 9, stage: STAGE,
    title: "Binary search",
    idea: "Look at the middle and throw half away. It works on anything that flips from \"no\" to \"yes\" exactly once, not just sorted arrays: a speed fast enough, a capacity big enough, the first bad version.",
    signals: "Sorted data, \"minimum x such that…\", \"maximum x such that…\", huge ranges (10⁹), or a yes/no check that is monotonic.",
    invariant: "The answer is always inside [lo, hi]. Each step removes the half that provably can't contain it.",
    drills: [
      {
        id: "halve", name: "Halve the range",
        blurb: "Classic search in a sorted array. mid = (lo + hi) // 2. Decide which half survives.",
        *play(ctx) {
          const n = T.rand(12, 15);
          const a = T.distinct(n, 1, 60).sort((x, y) => x - y);
          const present = Math.random() < 0.7;
          let t = present ? T.pick(a) : T.pick(T.range(58, 2).filter((x) => !a.includes(x) && x > a[0] && x < a[n - 1]));
          let lo = 0, hi = n - 1;
          while (lo <= hi) {
            const mid = (lo + hi) >> 1, am = a[mid];
            ctx.draw(V.line(h("strong", {}, `target = ${t}`)),
              V.array(a, { ptr: { lo, mid, hi }, cls: (k) => (k < lo || k > hi ? "dim" : k === mid ? "hot" : "") }));
            const ans = am === t ? "found" : am < t ? "right" : "left";
            yield T.choose(`a[mid] = ${am}. Your move:`, [["left", "Go left (hi = mid − 1)"], ["right", "Go right (lo = mid + 1)"], ["found", "Found it"]], ans,
              am === t ? `a[mid] is ${t}.` : `a[mid] = ${am} ${am < t ? "<" : ">"} ${t}. In sorted order, ${t} can only be to the ${am < t ? "right" : "left"}.`,
              am === t ? null : `${am < t ? mid - lo + 1 : hi - mid + 1} items ruled out in one comparison.`);
            if (am === t) {
              ctx.draw(V.line(h("strong", {}, `target = ${t}`)), V.array(a, { cls: (k) => (k === mid ? "ok" : "dim") }));
              return { summary: `Found in a handful of steps. log₂ ${n} ≈ ${Math.ceil(Math.log2(n + 1))}, so it never takes more than that.` };
            }
            if (am < t) lo = mid + 1; else hi = mid - 1;
          }
          ctx.draw(V.line(h("strong", {}, `target = ${t}`), "   not in the array"),
            V.array([...a, ""], { pick: true, ptr: { lo, hi }, cls: (k) => (k === n ? "ghost" : "") }));
          yield T.click(`lo passed hi, so ${t} isn't here. Click the index where it would be inserted.`, String(lo),
            `When the loop ends, lo is the first index whose value is bigger than ${t}. That's the insertion point.`,
            `lo = ${lo}: everything before it is smaller, everything from it on is bigger.`);
          return { summary: "When the target is missing, lo lands on the insertion point. That's bisect_left." };
        },
      },
      {
        id: "on-answer", name: "Search the answer",
        blurb: "Koko eats bananas at k per hour, one pile at a time (a pile of p takes ceil(p / k) hours). Find the slowest k that finishes within h hours. Faster always works if slower works, so binary search on k.",
        *play(ctx) {
          let piles, hrs, max, best;
          const hoursAt = (k) => piles.reduce((s, p) => s + Math.ceil(p / k), 0);
          do {
            piles = Array.from({ length: T.rand(4, 5) }, () => T.rand(3, 14));
            hrs = piles.length + T.rand(1, 4);
            max = Math.max(...piles);
            best = T.range(max, 1).find((k) => hoursAt(k) <= hrs);
          } while (best < 3);
          let lo = 1, hi = max;
          const tried = new Map();
          const speeds = T.range(max, 1);
          while (lo < hi) {
            const mid = (lo + hi) >> 1, need = hoursAt(mid);
            ctx.draw(
              V.line(`piles ${piles.join(", ")}   limit `, h("strong", {}, `${hrs} hours`)),
              V.array(speeds, { small: true, idx: false, win: [lo - 1, hi - 1], ptr: { lo: lo - 1, mid: mid - 1, hi: hi - 1 }, cls: (k) => (tried.has(k + 1) ? (tried.get(k + 1) ? "ok" : "bad") : k + 1 === mid ? "hot" : ""), label: "speed k" }),
              V.line(`At k = ${mid}: ${piles.map((p) => Math.ceil(p / mid)).join(" + ")} = `, h("strong", {}, `${need} hours`)));
            const ok = need <= hrs;
            yield T.choose("So:", [["ok", "Fast enough: try slower (hi = mid)"], ["slow", "Too slow: go faster (lo = mid + 1)"]], ok ? "ok" : "slow",
              ok ? `${need} ≤ ${hrs}, so k = ${mid} works. The answer is ${mid} or something slower. Keep mid, since it might be the answer.` : `${need} > ${hrs}, so k = ${mid} is too slow, and so is everything below it.`,
              ok ? `k = ${mid} works, so every faster k works too.` : `Every k ≤ ${mid} fails.`);
            tried.set(mid, ok);
            if (ok) hi = mid; else lo = mid + 1;
          }
          ctx.draw(V.line(`piles ${piles.join(", ")}   limit `, h("strong", {}, `${hrs} hours`)),
            V.array(speeds, { small: true, idx: false, pick: true, ptr: { lo: lo - 1, hi: hi - 1 }, cls: (k) => (tried.has(k + 1) ? (tried.get(k + 1) ? "ok" : "bad") : ""), label: "speed k" }));
          yield T.click("lo met hi. Click the answer.", String(lo - 1), "Where lo and hi meet is the first speed that works.", `k = ${best}.`);
          return { summary: "No array to search, just a yes/no question that flips once. Binary search finds the flip point." };
        },
      },
      {
        id: "rotated", name: "Rotated array",
        blurb: "A sorted array was rotated, for example 4 5 6 7 1 2 3. One half around mid is always still sorted. Find that half, then ask whether the target is inside it.",
        *play(ctx) {
          const n = T.rand(9, 11);
          const sorted = T.distinct(n, 1, 40).sort((x, y) => x - y);
          const rot = T.rand(2, n - 2);
          const a = sorted.slice(rot).concat(sorted.slice(0, rot));
          const t = T.pick(a.filter((_, i) => i !== ((n - 1) >> 1)));
          let lo = 0, hi = n - 1;
          for (;;) {
            const mid = (lo + hi) >> 1;
            const draw = () => ctx.draw(V.line(h("strong", {}, `target = ${t}`)),
              V.array(a, { ptr: { lo, mid, hi }, cls: (k) => (k < lo || k > hi ? "dim" : k === mid ? "hot" : "") }));
            draw();
            if (a[mid] === t) {
              yield T.choose(`a[mid] = ${a[mid]}.`, [["found", "Found it"], ["left", "Go left"], ["right", "Go right"]], "found", `a[mid] is the target.`);
              ctx.draw(V.line(h("strong", {}, `target = ${t}`)), V.array(a, { cls: (k) => (k === mid ? "ok" : "dim") }));
              return { summary: "Every step, one side is guaranteed sorted, and a sorted range tells you instantly whether the target is in it." };
            }
            const leftSorted = a[lo] <= a[mid], rightSorted = a[mid] <= a[hi];
            yield T.choose(`a[lo] = ${a[lo]}, a[mid] = ${a[mid]}, a[hi] = ${a[hi]}. Which half is sorted?`,
              [["L", `Left: lo..mid`], ["R", `Right: mid..hi`]],
              [leftSorted && "L", rightSorted && "R"].filter(Boolean),
              (v) => (v === "L" ? `a[lo] = ${a[lo]} > a[mid] = ${a[mid]}: the drop happens inside the left half.` : `a[mid] = ${a[mid]} > a[hi] = ${a[hi]}: the drop happens inside the right half.`),
              leftSorted && rightSorted ? "Both are sorted: this stretch has no drop at all." : null);
            let goLeft;
            if (leftSorted) goLeft = a[lo] <= t && t < a[mid];
            else goLeft = !(a[mid] < t && t <= a[hi]);
            const range = leftSorted ? [a[lo], a[mid]] : [a[mid], a[hi]];
            const inside = leftSorted ? goLeft : !goLeft;
            yield T.choose(`The ${leftSorted ? "left" : "right"} half runs ${range[0]} to ${range[1]} in order. Where is ${t}?`,
              [["left", "Go left (hi = mid − 1)"], ["right", "Go right (lo = mid + 1)"]], goLeft ? "left" : "right",
              `${t} is ${inside ? "inside" : "outside"} ${range[0]}..${range[1]}, so it ${inside ? "must be in" : "can't be in"} the sorted ${leftSorted ? "left" : "right"} half.`);
            if (goLeft) hi = mid - 1; else lo = mid + 1;
          }
        },
      },
    ],
  });

  // ── 10 Sorting and intervals ─────────────────────────────────────────────
  function randomIntervals(k, span) {
    return Array.from({ length: k }, () => {
      const s = T.rand(0, span - 3);
      return { s, e: Math.min(span, s + T.rand(1, 4)) };
    });
  }
  const tones = ["pa", "pb", "pc", "pd"];

  T.topic({
    id: "intervals", n: 10, stage: STAGE,
    title: "Sorting and intervals",
    idea: "Unsorted intervals can overlap in any pattern. Sort them by start and every overlap becomes local: each interval can only touch the block just before it.",
    signals: "Meetings, bookings, ranges, \"merge\", \"overlap\", \"how many at once\", or a custom ordering rule.",
    invariant: "After sorting by start, the current block's end is the only number you need to remember.",
    drills: [
      {
        id: "merge", name: "Merge overlapping",
        blurb: "Merge every set of overlapping intervals. Intervals that just touch (one ends at 5, the next starts at 5) count as overlapping.",
        *play(ctx) {
          let iv = randomIntervals(T.rand(5, 6), 16);
          ctx.draw(V.timeline(iv.map((x) => ({ ...x })), { min: 0, max: 16 }));
          yield T.choose("First, sort them by…", [["s", "start"], ["e", "end"], ["len", "length"]], "s",
            (v) => (v === "e" ? "By end, a long early interval like [1, 10] would land after a short later one like [2, 3]. The merge step would miss that they overlap." : "Length says nothing about where an interval sits. Overlaps would come in random order."),
            "Sorted by start, an interval can only overlap the block right before it.");
          iv = iv.sort((x, y) => x.s - y.s || x.e - y.e);
          const block = [];
          let cur = { s: iv[0].s, e: iv[0].e };
          block[0] = 0;
          let b = 0;
          const merged = [];
          for (let i = 1; i < iv.length; i++) {
            const nx = iv[i];
            ctx.draw(
              V.timeline(iv.map((x, k) => ({ ...x, cls: k < i ? tones[block[k] % 4] : k === i ? "hot" : "" })), { min: 0, max: 16 }),
              V.line("current block ", V.k(`[${cur.s}, ${cur.e}]`), "   next ", V.k(`[${nx.s}, ${nx.e}]`)),
              merged.length ? V.chips(merged.map((m) => `[${m.s}, ${m.e}]`), { label: "finished blocks" }) : null);
            const ans = nx.s <= cur.e ? "merge" : "new";
            yield T.choose("Your move:", [["merge", "Merge into the current block"], ["new", "Close it and start a new block"]], ans,
              ans === "merge" ? `It starts at ${nx.s}, which is not after the block's end (${cur.e}), so they overlap.` : `It starts at ${nx.s}, after the block ends at ${cur.e}. There's a gap.`,
              ans === "merge" ? (nx.e <= cur.e ? `It sits entirely inside, so the end stays ${cur.e}. Always use max(end, new end).` : `The block now ends at ${nx.e}.`) : `[${cur.s}, ${cur.e}] is final.`);
            if (ans === "merge") cur.e = Math.max(cur.e, nx.e);
            else { merged.push(cur); cur = { s: nx.s, e: nx.e }; b++; }
            block[i] = b;
          }
          merged.push(cur);
          ctx.draw(V.timeline(iv.map((x, k) => ({ ...x, cls: tones[block[k] % 4] })), { min: 0, max: 16 }),
            V.chips(merged.map((m) => `[${m.s}, ${m.e}]`), { label: "merged" }));
          return { summary: `${merged.length} block${merged.length > 1 ? "s" : ""}. Sort by start, then each interval either extends the last block or starts a new one.` };
        },
      },
      {
        id: "rooms", name: "How many rooms?",
        blurb: "Meetings arrive in order of start time. Put each one in a room that's free by then, or open a new room. Use as few rooms as you can.",
        *play(ctx) {
          const iv = randomIntervals(6, 12).map((x) => ({ s: x.s, e: x.e + 1 })).sort((x, y) => x.s - y.s || x.e - y.e);
          const rooms = [];
          const placed = [];
          for (let i = 0; i < iv.length; i++) {
            const m = iv[i];
            ctx.draw(V.timeline([{ ...m, lane: 0, cls: "hot" }, ...placed.map((p) => ({ ...p, lane: p.room + 1, cls: tones[p.room % 4] }))],
              { min: 0, max: 14, lanes: rooms.length + 1, padL: 60, laneLabels: ["next", ...rooms.map((_, r) => `room ${r + 1}`)] }));
            const free = rooms.map((end, r) => (end <= m.s ? r : -1)).filter((r) => r >= 0);
            const opts = rooms.map((end, r) => [String(r), `Room ${r + 1} (busy until ${end})`]).concat([["new", "Open a new room"]]);
            const pick = yield T.ask({
              prompt: `Meeting [${m.s}, ${m.e}]. Where does it go?`,
              options: opts,
              answer: free.length ? free.map(String) : "new",
              why: (v) => (v === "new" ? `Room ${free[0] + 1} is free by ${m.s} (busy until ${rooms[free[0]]}). Reuse it.` : `Room ${Number(v) + 1} is busy until ${rooms[Number(v)]}, after this meeting starts at ${m.s}.`),
            });
            const r = pick === "new" ? rooms.length : Number(pick);
            rooms[r] = m.e;
            placed.push({ ...m, room: r });
          }
          ctx.draw(V.timeline(placed.map((p) => ({ ...p, lane: p.room, cls: tones[p.room % 4] })), { min: 0, max: 14, lanes: rooms.length, padL: 60, laneLabels: rooms.map((_, r) => `room ${r + 1}`) }));
          return { summary: `${rooms.length} room${rooms.length > 1 ? "s" : ""}: the most meetings running at the same moment. In code, a min-heap of end times tells you the room that frees up first.` };
        },
      },
      {
        id: "order", name: "Custom order",
        blurb: "Arrange numbers to form the biggest possible number, like [3, 30, 34] → 34330. The rule: a goes first if a + b beats b + a as strings.",
        *play(ctx) {
          const PAIRS = [[3, 30], [9, 90], [12, 121], [824, 8247], [10, 2], [43, 4], [5, 56], [34, 3], [20, 2], [7, 76], [1, 10], [97, 9], [59, 5], [0, 1]];
          for (const [x, y] of T.sample(PAIRS, 5).map((p) => T.shuffle(p))) {
            const xy = `${x}${y}`, yx = `${y}${x}`;
            ctx.draw(h("p", { class: "line", style: "font:600 30px var(--mono)" }, `${x}   ${y}`));
            const ans = xy > yx ? String(x) : String(y);
            yield T.choose("Which goes first?", [[String(x), `${x} first`], [String(y), `${y} first`]], ans,
              `Compare both glued orders: ${xy} vs ${yx}. ${xy > yx ? xy : yx} is bigger.`, `${xy > yx ? xy : yx} beats ${xy > yx ? yx : xy}.`);
          }
          return { summary: "Comparing digit by digit or by length both fail. Glue the two both ways and compare: sort with key=cmp_to_key(...)." };
        },
      },
    ],
  });

  // ── 11 Greedy ────────────────────────────────────────────────────────────
  T.topic({
    id: "greedy", n: 11, stage: STAGE,
    title: "Greedy",
    idea: "Make the locally best choice and never look back. It only works when you can argue that the greedy choice is never worse than any other, usually because it leaves the most room for the future.",
    signals: "\"Maximum number of…\", scheduling, reach or jump problems, or running sums where a bad prefix can be dropped.",
    invariant: "Some optimal answer agrees with every choice made so far.",
    drills: [
      {
        id: "kadane", name: "Extend or restart",
        blurb: "Maximum subarray sum. Carry the best run that ends here. Each new number either joins that run or starts a fresh one.",
        *play(ctx) {
          const n = T.rand(8, 10);
          const a = Array.from({ length: n }, () => (Math.random() < 0.42 ? -T.rand(1, 8) : T.rand(1, 7)));
          let cur = a[0], best = a[0], start = 0, bestAt = [0, 0];
          for (let i = 1; i < n; i++) {
            const x = a[i];
            ctx.draw(
              V.array(a, { win: [start, i - 1], ptr: { i }, cls: (k) => (k === i ? "hot" : k > i ? "" : k < start ? "dim" : "") }),
              V.line(`run so far = ${cur}   best = ${best}`),
              V.line("next number: ", V.k(x)));
            const ans = cur < 0 ? "restart" : cur > 0 ? "extend" : ["extend", "restart"];
            yield T.choose("Your move:", [["extend", `Extend: run + ${x}`], ["restart", `Restart at ${x}`]], ans,
              cur < 0 ? `The run so far sums to ${cur}, which is negative. It can only drag ${x} down: ${cur} + ${x} < ${x}.` : `The run so far is worth ${cur} > 0. Keeping it adds to ${x}.`,
              cur < 0 ? `Dropped a run worth ${cur}.` : cur === 0 ? "A zero run: either choice gives the same sum." : null);
            if (cur < 0) { cur = x; start = i; } else cur += x;
            if (cur > best) { best = cur; bestAt = [start, i]; }
          }
          ctx.draw(V.array(a, { win: bestAt, cls: (k) => (k >= bestAt[0] && k <= bestAt[1] ? "ok" : "dim") }), V.line("Best sum: ", h("strong", {}, best)));
          return { summary: "A prefix with a negative sum never helps whatever follows it. That one fact is all of Kadane's algorithm." };
        },
      },
      {
        id: "reach", name: "Farthest reach",
        blurb: "Each cell says how far you can jump from it. Walk left to right and keep the farthest index you can reach. Can you get to the last cell?",
        *play(ctx) {
          const n = T.rand(7, 9);
          const a = Array.from({ length: n }, () => T.pick([0, 1, 1, 2, 2, 3]));
          a[0] = Math.max(1, a[0]);
          let reach = 0;
          for (let i = 0; i < n; i++) {
            if (reach >= n - 1) break;
            ctx.draw(
              V.array(a, { pick: i <= reach, ptr: { i }, cls: (k) => (k === i ? "hot" : k <= reach ? "pa" : "") }),
              V.line(`reach so far: index ${reach}`));
            if (i > reach) {
              yield T.ask({ prompt: `Index ${i}. Click the new farthest reach, or…`, picks: true, options: [["stuck", "Can't get here: stuck"]], answer: "stuck",
                why: `Nothing before index ${i} reaches it: the farthest you could get was ${reach}.` });
              ctx.draw(V.array(a, { cls: (k) => (k <= reach ? "pa" : k === i ? "bad" : "dim") }), V.line(`Stuck at ${reach}.`));
              return { summary: "A 0 that nothing can jump over is a wall. Reach tells you exactly when you hit one." };
            }
            const nr = Math.min(n - 1, Math.max(reach, i + a[i]));
            yield T.ask({
              prompt: `Standing on index ${i} (jump up to ${a[i]}). Click the farthest index reachable now.`,
              picks: true, options: [["stuck", "Can't get here: stuck"]], answer: String(nr),
              why: (v) => {
                if (v === "stuck") return `Index ${i} is within reach (≤ ${reach}).`;
                const k = Number(v);
                if (k === i + a[i] && k < reach) return `From ${i} you get to ${k}, but you could already reach ${reach}. Reach only grows: max(old, i + a[i]).`;
                return `From index ${i}, a jump of up to ${a[i]} lands at most at ${Math.min(n - 1, i + a[i])}. Keep the larger of that and ${reach}.`;
              },
              note: nr > reach ? `Reach grows to ${nr}.` : "Reach stays the same.",
            });
            reach = nr;
          }
          ctx.draw(V.array(a, { cls: () => "ok" }), V.line("The last cell is reachable."));
          return { summary: "One number, the farthest reach, replaces trying every jump path." };
        },
      },
      {
        id: "schedule", name: "Most meetings",
        blurb: "Attend as many non-overlapping meetings as possible. Pick them one at a time.",
        *play(ctx) {
          const iv = randomIntervals(7, 14).map((x, i) => ({ ...x, id: i }));
          let lastEnd = -1;
          const taken = [];
          const overl = (m) => m.s < lastEnd && !taken.includes(m.id);
          for (;;) {
            const fits = iv.filter((m) => !taken.includes(m.id) && m.s >= lastEnd);
            const minE = fits.length ? Math.min(...fits.map((m) => m.e)) : null;
            ctx.draw(V.timeline(iv.map((m) => ({ ...m, cls: taken.includes(m.id) ? "ok" : overl(m) ? "dim" : "", pick: taken.includes(m.id) ? null : String(m.id) })), { min: 0, max: 14 }),
              V.line(`taken: ${taken.length}${lastEnd >= 0 ? `   free from time ${lastEnd}` : ""}`));
            const v = yield T.ask({
              prompt: taken.length ? "Click the next meeting to take, or…" : "Click the first meeting to take, or…",
              picks: true, options: [["done", "Nothing else fits"]],
              answer: fits.length ? fits.filter((m) => m.e === minE).map((m) => String(m.id)) : "done",
              why: (v) => {
                if (v === "done") return `[${fits[0].s}, ${fits[0].e}] still fits after ${lastEnd}.`;
                const m = iv[Number(v)];
                if (m.s < lastEnd) return "It overlaps a meeting you already took.";
                const better = fits.find((f) => f.e === minE);
                return `It ends at ${m.e}. [${better.s}, ${better.e}] ends earlier, at ${minE}, which leaves more room for everything after.`;
              },
            });
            if (!fits.length) break;
            const m = iv[Number(v)];
            taken.push(m.id);
            lastEnd = m.e;
          }
          return { summary: `${taken.length} meetings. Taking whatever ends first is never worse: any other choice would occupy the time at least as long.` };
        },
      },
    ],
  });
})();
