"use strict";
(function () {
  const T = window.Trace;
  const { h, V } = T;
  const STAGE = "Foundations";

  // ── 01 What Python's operations cost ─────────────────────────────────────
  const C1 = "O(1)", CL = "O(log n)", CN = "O(n)", CNL = "O(n log n)";
  const COSTS = [
    ["# items: a list of n values\nx in items", CN, "A list has no index by value, so Python compares x with the items one by one."],
    ["# seen: a set of n values\nx in seen", C1, "A set hashes x and jumps straight to the one bucket it could be in."],
    ["# d: a dict with n keys\nd[key]", C1, "A dict lookup is one hash and one jump, however big the dict is."],
    ["# items: a list of n values\nitems.append(x)", C1, "Lists keep spare room at the end, so appending is O(1) on average."],
    ["# items: a list of n values\nitems.pop()", C1, "Removing the last item moves nothing else."],
    ["# items: a list of n values\nitems.pop(0)", CN, "Every remaining item shifts one slot left to close the gap at the front."],
    ["# items: a list of n values\nitems.insert(0, x)", CN, "Every item shifts one slot right to make room at the front."],
    ["# q: a collections.deque of n values\nq.popleft()", C1, "A deque is built to add and remove at both ends without shifting anything."],
    ["# q: a collections.deque of n values\nq.appendleft(x)", C1, "A deque is built to add and remove at both ends without shifting anything."],
    ["# items: a list of n values\nitems[i]", C1, "Index to memory address is one multiplication and one add."],
    ["# items: a list of n values\nrest = items[1:]", CN, "A slice is a copy. This one copies n − 1 items."],
    ["# items: a list of n values\nsorted(items)", CNL, "Sorting by comparisons needs about n log n of them."],
    ["# items: a list of n values (unsorted)\nmin(items)", CN, "Without order, the smallest could be anywhere, so every item gets checked."],
    ["# items: a list of n values\nlen(items)", C1, "The length is stored on the list. Nothing gets counted."],
    ["# heap: a list kept in heap order, n values\nheapq.heappush(heap, x)", CL, "The new item bubbles up one level at a time, and a heap has about log n levels."],
    ["# heap: a list kept in heap order, n values\nheapq.heappop(heap)", CL, "The last item moves to the top and sinks down at most log n levels."],
    ["# items: a list of n values\nheapq.heapify(items)", CN, "Surprising but true: building a heap bottom-up is O(n). Most nodes sit near the bottom and barely move."],
    ["# items: a sorted list of n values\nbisect.bisect_left(items, x)", CL, "Binary search halves the range every step."],
    ["# s: a string of length n\ns = s + ch", CN, "Strings can't change, so + builds a new one and copies all of s. Inside a loop that becomes O(n²)."],
    ["# parts: a list of n short strings\n''.join(parts)", CN, "join sizes the result once and copies each character once."],
    ["# items: a list of n values\nCounter(items)", CN, "One pass, with one O(1) dict update per item."],
    ["# items: a list of n values\nitems.index(x)", CN, "Same as x in items: scan until it turns up."],
    ["# items: a list of n values\nitems.remove(x)", CN, "Find x by scanning, then shift everything after it one slot left."],
    ["# seen: a set of n values\nseen.add(x)", C1, "One hash, one slot."],
    ["# d: a dict with n keys\ndel d[key]", C1, "One hash, one slot."],
    ["# d: a dict with n keys\nx in d.values()", CN, "Only keys are hashed. Values are scanned one by one."],
    ["# items: a list of n values\nitems.reverse()", CN, "Every item moves once."],
    ["# items: a list of n values\nitems[-1]", C1, "Negative indexes are just len(items) − 1. Still one jump."],
    ["# seen: a set of n values\nlist(seen)", CN, "Building a new list copies every item."],
    ["# d: a dict with n keys\nkey in d", C1, "Membership on a dict checks keys, which are hashed."],
  ];

  const TOOLS = ["list", "set", "dict", "Counter", "deque", "heapq", "defaultdict(list)", "bisect on a sorted list"];
  const SCENARIOS = [
    ["Answer \"have I seen this value before?\" for each item in a stream.", "set", "A set answers membership in O(1) and stores nothing else."],
    ["Count how many times each word appears.", "Counter", "Counter is a dict of counts with most_common() built in."],
    ["Remember the index where each value first appeared.", "dict", "You need value → index, which is exactly a dict."],
    ["Serve requests in the order they arrived: add at the back, take from the front.", "deque", "popleft() on a deque is O(1). On a list, pop(0) shifts everything."],
    ["Keep taking the smallest item while new items keep arriving.", "heapq", "A heap gives the minimum in O(1) and pops or pushes in O(log n)."],
    ["Group words by their first letter.", "defaultdict(list)", "defaultdict(list) lets you write groups[key].append(w) without checking for the key first."],
    ["Keep a sorted list and find where a new value would slot in.", "bisect on a sorted list", "bisect does the binary search for you in O(log n)."],
    ["Undo history, where the most recent action is undone first.", "list", "Last in, first out: append and pop at the end of a list are both O(1)."],
    ["Track the last k items of a stream, dropping the oldest each time.", "deque", "Append on the right and popleft the oldest, both O(1). deque(maxlen=k) can even drop for you."],
    ["Keep the k largest numbers seen so far in a long stream.", "heapq", "A min-heap of size k: its top is the smallest of your k largest, the one to kick out."],
    ["Mark grid cells (row, col) you have already visited in a search.", "set", "Tuples hash fine, so a set of (r, c) gives O(1) visited checks."],
    ["Find the 3 most common elements in a list.", "Counter", "Counter(items).most_common(3) counts and ranks in one line."],
    ["Find the next bigger value in a sorted list of prices, many times over.", "bisect on a sorted list", "Sorted data plus repeated searches means binary search: bisect_right."],
    ["Map each student to a list of their grades, filling it as records arrive.", "defaultdict(list)", "Each key collects many values, and missing keys start as an empty list."],
  ];

  T.topic({
    id: "python-costs", n: 1, stage: STAGE,
    title: "What Python operations cost",
    idea: "Most slow solutions aren't slow on paper. They hide an O(n) step inside a loop: a search through a list, a pop from the front, a string rebuilt every time.",
    signals: "Any time you write a loop, ask what each line inside it costs.",
    invariant: "Hashing and working at the end of a list are cheap. Searching a list or shifting its items costs O(n).",
    drills: [
      {
        id: "cost", name: "Call the cost",
        blurb: "Each card is one line of Python on a collection of n items. Say what it costs before you think about it too hard.",
        *play(ctx) {
          const cards = T.sample(COSTS, 6);
          for (const [i, [code, ans, why]] of cards.entries()) {
            ctx.draw(V.label(`Card ${i + 1} of ${cards.length}`), V.code(code));
            yield T.choose("What does this line cost?", [C1, CL, CN, CNL], ans, () => why, why);
          }
          return { summary: "The usual culprits are list membership, pop(0) and insert(0, x), and string + inside a loop." };
        },
      },
      {
        id: "tool", name: "Pick the tool",
        blurb: "Each job has one structure that makes it easy. Pick it.",
        *play(ctx) {
          const jobs = T.sample(SCENARIOS, 6);
          for (const [i, [job, ans, why]] of jobs.entries()) {
            ctx.draw(V.label(`Job ${i + 1} of ${jobs.length}`), h("p", { class: "line", style: "font-size:19px;font-weight:600" }, job));
            const opts = T.shuffle([ans, ...T.sample(TOOLS.filter((t) => t !== ans), 3)]);
            yield T.choose("Which structure fits best?", opts, ans, (v) => `Not ${v}. ${why}`, why);
          }
          return { summary: "Choosing the structure is usually most of the solution." };
        },
      },
    ],
  });

  // ── 02 Big-O in practice ─────────────────────────────────────────────────
  const BIGO = ["O(log n)", "O(√n)", "O(n)", "O(n log n)", "O(n²)", "O(2ⁿ)"];
  const LOOPS = [
    ["for i in range(n):\n    for j in range(n):\n        work(i, j)", "O(n²)", "n rounds of n steps each."],
    ["for i in range(n):\n    for j in range(i):\n        work(i, j)", "O(n²)", "0 + 1 + … + (n−1) = n(n−1)/2 steps. Halving n² is still n²."],
    ["i = n\nwhile i > 1:\n    i //= 2", "O(log n)", "Halving n until it reaches 1 takes log₂ n steps."],
    ["for i in range(n):\n    work(i)\nfor j in range(n):\n    work(j)", "O(n)", "Two loops one after another add up to 2n, not n². Only nesting multiplies."],
    ["for i in range(n):\n    j = 1\n    while j < n:\n        j *= 2", "O(n log n)", "The inner loop doubles j, so it runs log n times, once for each of the n outer rounds."],
    ["i = 1\nwhile i * i <= n:\n    i += 1", "O(√n)", "It stops once i passes √n."],
    ["def f(n):\n    if n <= 1:\n        return 1\n    return f(n - 1) + f(n - 1)", "O(2ⁿ)", "Every call makes two more, so the call tree doubles at each of n levels."],
    ["def f(n):\n    if n <= 1:\n        return 1\n    return f(n // 2) + 1", "O(log n)", "One call per level, and n halves each level."],
    ["items.sort()\nfor x in items:\n    bisect_left(items, x)", "O(n log n)", "The sort is n log n, then n binary searches at log n each. Still n log n."],
    ["seen = []\nfor x in items:\n    if x not in seen:\n        seen.append(x)", "O(n²)", "x not in seen scans a list that can grow to n items, once per item. Use a set to make it O(n)."],
    ["seen = set()\nfor x in items:\n    if x not in seen:\n        seen.add(x)", "O(n)", "Set membership is O(1), so the loop does n cheap steps."],
    ["for i in range(n):\n    for j in range(5):\n        work(i, j)", "O(n)", "The inner loop is a constant 5. 5n is O(n)."],
    ["left, right = 0, n - 1\nwhile left < right:\n    if check(left, right):\n        left += 1\n    else:\n        right -= 1", "O(n)", "Every step moves one pointer inward, and they can only close a gap of n."],
    ["s = \"\"\nfor i in range(n):\n    s = s + \"x\"", "O(n²)", "Each + copies the whole string built so far: 1 + 2 + … + n characters."],
    ["def f(n):\n    if n == 0:\n        return\n    f(n - 1)", "O(n)", "One call per level, with n levels."],
    ["def sort(a):\n    if len(a) <= 1:\n        return a\n    mid = len(a) // 2\n    return merge(sort(a[:mid]), sort(a[mid:]))", "O(n log n)", "There are log n levels of halving, and merging does n work per level."],
    ["left = 0\nfor right in range(n):\n    while too_big(left, right):\n        left += 1", "O(n)", "It looks nested, but left only moves forward. It can step at most n times in total, across the whole loop."],
    ["for i in range(n):\n    for j in range(i, n, i + 1):\n        work(i, j)", "O(n log n)", "Round i takes about n/(i+1) steps. n/1 + n/2 + n/3 + … ≈ n log n (the harmonic series)."],
  ];
  const LIMITS = [
    { ns: ["8", "10"], ans: "O(n!)", why: "10! is about 3.6 million orderings, so you can try them all." },
    { ns: ["16", "18", "20"], ans: "O(2ⁿ)", why: "2²⁰ is about a million subsets: try every subset, or use bitmask DP." },
    { ns: ["100", "200", "400"], ans: "O(n³)", why: "400³ is about 64 million, so three nested loops just fit." },
    { ns: ["1,000", "2,000", "5,000"], ans: "O(n²)", why: "5,000² = 25 million: every pair fits. n³ would be 10¹¹." },
    { ns: ["10⁵", "2·10⁵", "10⁶"], ans: "O(n log n)", why: "10⁵ × 17 ≈ 1.7 million steps, fine for sorting or a heap. n² would be 10¹⁰." },
    { ns: ["10⁷", "10⁸"], ans: "O(n)", why: "Only a single pass fits. Even n log n is borderline." },
    { ns: ["10¹²", "10¹⁸"], ans: "O(log n)", why: "You can't even count up to n. Halve the range, or find a formula." },
  ];

  T.topic({
    id: "big-o", n: 2, stage: STAGE,
    title: "Big-O in practice",
    idea: "Big-O asks one question: when the input gets 10× bigger, how much more work is there? Count how often the innermost line runs and drop the constants.",
    signals: "Before you code, read the input limit. It usually tells you which complexity the problem expects.",
    invariant: "Nested loops multiply, loops one after another add, halving gives log n, and two calls per level give 2ⁿ.",
    drills: [
      {
        id: "loops", name: "Read the loop",
        blurb: "Count how many times the innermost line runs as n grows. The answer is the shape, not the exact number.",
        *play(ctx) {
          const cards = T.sample(LOOPS, 6);
          for (const [i, [code, ans, why]] of cards.entries()) {
            ctx.draw(V.label(`Snippet ${i + 1} of ${cards.length}`), V.code(code));
            yield T.choose("How does the work grow with n?", BIGO, ans, (v) => (v === "O(n²)" && ans === "O(n)" ? "Looks nested, but count the total steps. " : "") + why, why);
          }
          return { summary: "Watch for the traps: a pointer that only moves forward is O(n) in total, and an `in` on a list inside a loop is O(n²)." };
        },
      },
      {
        id: "limits", name: "The limit gives it away",
        blurb: "Rule of thumb: about 10⁸ simple steps per second (closer to 10⁷ in Python). Problem setters pick n so that the intended complexity just fits.",
        *play(ctx) {
          const opts = ["O(n!)", "O(2ⁿ)", "O(n³)", "O(n²)", "O(n log n)", "O(n)", "O(log n)"];
          const rounds = T.shuffle(LIMITS).slice(0, 6);
          for (const [i, band] of rounds.entries()) {
            const n = T.pick(band.ns);
            ctx.draw(V.label(`Problem ${i + 1} of ${rounds.length}`),
              h("p", { class: "line", style: "font-size:26px;font-weight:800;font-family:var(--mono)" }, `1 ≤ n ≤ ${n}`));
            yield T.choose("What's the slowest approach that still runs in time?", opts, band.ans, (v) => {
              const a = opts.indexOf(v), b = opts.indexOf(band.ans);
              return (a < b ? `${v} is too slow here. ` : `${v} would fit, but the limit allows something slower, so a simpler idea is probably expected. `) + band.why;
            }, band.why);
          }
          return { summary: "n ≤ 20 means exponential, n ≤ 5,000 means pairs, n ≤ 10⁶ means sort-then-scan or better." };
        },
      },
    ],
  });

  // ── 03 Arrays and strings ────────────────────────────────────────────────
  T.topic({
    id: "arrays", n: 3, stage: STAGE,
    title: "Arrays and strings",
    idea: "An array is a row of numbered slots. Most array tricks come down to index arithmetic: where does i go, what lies to the left of i, and what lies to the right.",
    signals: "In-place edits, rotations, \"for every index, combine everything else\".",
    invariant: "Indexes run 0 to n − 1, and % n wraps any position back into range.",
    drills: [
      {
        id: "rotate", name: "Where does it land?",
        blurb: "Rotate the array, then find where the highlighted letter ends up. Click its new slot.",
        *play(ctx) {
          const n = T.rand(6, 9);
          const vals = T.letters.slice(0, n).split("");
          const rounds = 4;
          for (let r = 0; r < rounds; r++) {
            const dir = r === 0 ? "right" : T.pick(["right", "left"]);
            const k = r === 3 ? T.rand(n + 1, 2 * n + 1) : T.rand(1, n + 2);
            const i = T.rand(0, n - 1);
            const dest = dir === "right" ? (i + k) % n : (((i - k) % n) + n) % n;
            const after = Array(n).fill("");
            const draw = (fill) => ctx.draw(
              V.line(h("strong", {}, `Rotate ${dir} by k = ${k}`), `   (n = ${n})`),
              V.array(vals, { label: "Before", cls: (j) => (j === i ? "hot" : "") }),
              V.array(fill || after, { label: "After: click where it lands", pick: !fill, cls: (j) => (fill && j === dest ? "ok" : "") }));
            draw();
            yield T.click(`Where does ${vals[i]} (index ${i}) end up?`, String(dest),
              (v) => {
                const raw = dir === "right" ? i + k : i - k;
                if (Number(v) === raw) return "Close, but that index doesn't exist. Wrap it back into range with % n.";
                return `Moving ${dir} by ${k} means ${i} ${dir === "right" ? "+" : "−"} ${k}, then % ${n} to wrap around.` + (k >= n ? ` Rotating by ${k} is the same as rotating by ${k % n}: every ${n} steps bring it back to the start.` : "");
              },
              `(${i} ${dir === "right" ? "+" : "−"} ${k}) % ${n} = ${dest}`);
          }
          return { summary: "Rotate right by k sends index i to (i + k) % n. Reduce k with k % n before you do anything else." };
        },
      },
      {
        id: "product", name: "Everything except me",
        blurb: "answer[i] = product of all numbers except nums[i]. Instead of re-multiplying, build left[i] (everything before i) and right[i] (everything after i).",
        *play(ctx) {
          const n = T.rand(5, 6);
          const nums = Array.from({ length: n }, () => T.rand(1, 4));
          const left = [1], right = Array(n).fill(1);
          for (let i = 1; i < n; i++) left[i] = left[i - 1] * nums[i - 1];
          for (let i = n - 2; i >= 0; i--) right[i] = right[i + 1] * nums[i + 1];
          const answer = Array(n).fill("");
          const qs = T.sample(T.range(n), 3);
          for (const i of qs) {
            let picked = { L: null, R: null };
            const draw = (stage) => ctx.draw(
              V.array(nums, { label: "nums", cls: (j) => (j === i ? "hot" : j < i ? "pa" : "pb") }),
              V.array(left, { label: "left[j] = product of nums before j", pick: stage === "L", key: (j) => "L" + j, cls: (j) => (picked.L === j ? "ok" : "") }),
              V.array(right, { label: "right[j] = product of nums after j", pick: stage === "R", key: (j) => "R" + j, cls: (j) => (picked.R === j ? "ok" : "") }),
              V.array(answer, { label: "answer" }));
            draw("L");
            yield T.click(`answer[${i}] needs the product of everything left of index ${i}. Click that cell in the left row.`, "L" + i, (v) => {
              if (v[0] === "R") return "That's the right row. Start with the left side.";
              const j = Number(v.slice(1));
              if (j === i + 1) return `left[${i + 1}] includes nums[${i}] itself, the one number we must leave out.`;
              if (j < i) return `left[${j}] stops before index ${j}, so it misses nums[${j}..${i - 1}].`;
              return `left[${j}] covers nums[0..${j - 1}], which goes past index ${i}.`;
            }, `left[${i}] = ${left[i]}`);
            picked.L = i;
            draw("R");
            yield T.click(`Now the product of everything right of index ${i}. Click it in the right row.`, "R" + i, (v) => {
              if (v[0] === "L") return "That's the left row. Pick from the right row.";
              const j = Number(v.slice(1));
              if (j === i - 1) return `right[${i - 1}] includes nums[${i}] itself.`;
              return `right[${j}] covers nums[${j + 1}..${n - 1}]. You need nums[${i + 1}..${n - 1}].`;
            }, `right[${i}] = ${right[i]}`);
            picked.R = i;
            draw(null);
            const val = left[i] * right[i];
            yield T.choose(`So answer[${i}] is…`, T.numOptions(val, { spread: 4, min: 1, extra: [left[i] + right[i], val * nums[i]] }), val,
              (v) => (v === left[i] + right[i] ? "Multiply the two sides, don't add them." : v === val * nums[i] ? `That includes nums[${i}]. Leave it out.` : `left[${i}] × right[${i}] = ${left[i]} × ${right[i]}.`),
              `${left[i]} × ${right[i]} = ${val}`);
            answer[i] = val;
          }
          ctx.draw(V.array(nums, { label: "nums" }), V.array(left, { label: "left" }), V.array(right, { label: "right" }),
            V.array(left.map((l, i) => l * right[i]), { label: "answer = left × right", cls: (j) => (qs.includes(j) ? "ok" : "") }));
          return { summary: "Two passes, one from each end, replace n² re-multiplying. The same split shows up in prefix sums, trapping rain water and stock spans." };
        },
      },
    ],
  });

  // ── 04 Hashing ───────────────────────────────────────────────────────────
  function twoSumInstance() {
    for (;;) {
      const n = T.rand(6, 8);
      const a = Array.from({ length: n }, () => T.rand(1, 15));
      const i = T.rand(3, n - 1), j = T.rand(0, i - 1);
      const target = a[i] + a[j];
      let early = false;
      for (let q = 0; q <= i && !early; q++) for (let p = 0; p < q; p++) if (a[p] + a[q] === target && !(p === j && q === i)) early = true;
      if (early) continue;
      if (new Set(a.slice(0, i)).size < i) continue; // keep earlier values distinct so the map is unambiguous
      return { a, i, j, target };
    }
  }

  const fmtTuple = (arr) => `(${arr.join(", ")})`;
  const GROUPINGS = [
    {
      goal: "Group words that are anagrams of each other.",
      items: ["eat", "tea", "ate", "teat", "tate", "tan", "ant", "nat"],
      truth: (w) => w.split("").sort().join(""),
      keys: [
        ["''.join(sorted(w))", (w) => `"${w.split("").sort().join("")}"`, true],
        ["frozenset(w)", (w) => `{${[...new Set(w)].sort().join(", ")}}`],
        ["len(w)", (w) => String(w.length)],
        ["w[0]", (w) => `"${w[0]}"`],
      ],
    },
    {
      goal: "Group words that use the same letters, where repeats don't matter.",
      items: ["loop", "pool", "lop", "plop", "sat", "stats", "tsar"],
      truth: (w) => [...new Set(w)].sort().join(""),
      keys: [
        ["frozenset(w)", (w) => `{${[...new Set(w)].sort().join(", ")}}`, true],
        ["''.join(sorted(w))", (w) => `"${w.split("").sort().join("")}"`],
        ["len(w)", (w) => String(w.length)],
        ["w[0]", (w) => `"${w[0]}"`],
      ],
    },
    {
      goal: "Group grid cells (r, c) that sit on the same diagonal running down and to the right.",
      items: ["(0,0)", "(1,1)", "(2,2)", "(0,1)", "(1,2)", "(2,0)", "(3,1)"],
      truth: (p) => { const [r, c] = p.slice(1, -1).split(",").map(Number); return r - c; },
      keys: [
        ["r - c", (p) => { const [r, c] = p.slice(1, -1).split(",").map(Number); return String(r - c); }, true],
        ["r + c", (p) => { const [r, c] = p.slice(1, -1).split(",").map(Number); return String(r + c); }],
        ["r", (p) => p.slice(1, -1).split(",")[0]],
        ["c", (p) => p.slice(1, -1).split(",")[1]],
      ],
    },
    {
      goal: "Group numbers that leave the same remainder when divided by 4.",
      items: ["3", "7", "11", "4", "8", "9", "13", "2"],
      truth: (x) => Number(x) % 4,
      keys: [
        ["x % 4", (x) => String(Number(x) % 4), true],
        ["x // 4", (x) => String(Math.floor(Number(x) / 4))],
        ["x % 2", (x) => String(Number(x) % 2)],
        ["str(x)[-1]", (x) => `"${x.slice(-1)}"`],
      ],
    },
    {
      goal: "Group words with the same letter pattern: egg, add and too all go first letter, new letter, repeat.",
      items: ["egg", "add", "foo", "bar", "cat", "paper", "title", "apple"],
      truth: (w) => fmtTuple(w.split("").map((c) => w.indexOf(c))),
      keys: [
        ["tuple(w.index(c) for c in w)", (w) => fmtTuple(w.split("").map((c) => w.indexOf(c))), true],
        ["len(set(w))", (w) => String(new Set(w).size)],
        ["''.join(sorted(w))", (w) => `"${w.split("").sort().join("")}"`],
        ["len(w)", (w) => String(w.length)],
      ],
    },
  ];

  function groupBy(items, key) {
    const m = new Map();
    for (const it of items) {
      const k = key(it);
      if (!m.has(k)) m.set(k, []);
      m.get(k).push(it);
    }
    return m;
  }

  T.topic({
    id: "hashing", n: 4, stage: STAGE,
    title: "Hashing",
    idea: "A hash map turns \"search for it\" into \"look it up\". The hard part is deciding what to store, and under which key, so the question you'll ask later is a single lookup.",
    signals: "\"Have I seen…\", \"find the pair\", \"group by\", \"count\", or an O(n²) pair loop you want to make O(n).",
    invariant: "The map holds exactly what you've walked past, keyed by what you'll want to ask about later.",
    drills: [
      {
        id: "two-sum", name: "Two sum, one pass",
        blurb: "Walk left to right. For each x, ask the map for its partner (target − x). If it isn't there yet, remember x and its index.",
        *play(ctx) {
          const { a, i: hitAt, j, target } = twoSumInstance();
          const map = new Map();
          for (let i = 0; i <= hitAt; i++) {
            const x = a[i], need = target - x, has = map.has(need);
            ctx.draw(
              V.line(h("strong", {}, `target = ${target}`)),
              V.row(
                V.array(a, { ptr: { i }, cls: (k) => (k === i ? "hot" : k < i ? "dim" : "") }),
                V.kv([...map.entries()].map(([k, v]) => [k, `index ${v}`]), { label: "seen: value → index", empty: "empty so far" })));
            yield T.choose(`x = ${x}. Is its partner already in the map?`,
              [["yes", `Yes: found the pair`], ["no", `No: store ${x} → ${i}`]],
              has ? "yes" : "no",
              has ? `The partner is ${target} − ${x} = ${need}, and ${need} is a key in the map (index ${map.get(need)}).`
                : `The partner would be ${target} − ${x} = ${need}, and ${need} isn't a key yet.` + (need === x ? " x can't pair with itself: it isn't stored until after the check." : ""),
              has ? `${need} + ${x} = ${target}: indexes ${map.get(need)} and ${i}.` : `${need} not there, so remember ${x}.`);
            if (!has) map.set(x, i);
          }
          ctx.draw(V.line(h("strong", {}, `target = ${target}`)),
            V.row(V.array(a, { cls: (k) => (k === j || k === hitAt ? "ok" : "dim") }),
              V.kv([...map.entries()].map(([k, v]) => [k, `index ${v}`]), { label: "seen", cls: (k) => (k === a[j] ? "ok" : "") })));
          return { summary: "Check first, then store. That order is why x never pairs with itself." };
        },
      },
      {
        id: "keys", name: "Choose the key",
        blurb: "Grouping is just a dict from key to list. Everything depends on the key: equal keys must mean \"belongs together\".",
        *play(ctx) {
          for (const g of T.sample(GROUPINGS, 3)) {
            const truthGroups = groupBy(g.items, g.truth);
            ctx.draw(V.line(h("strong", {}, g.goal)), V.chips(g.items, { label: "items" }));
            const opts = T.shuffle(g.keys.map((k, i) => [i, k[0]]));
            const right = g.keys.findIndex((k) => k[2]);
            yield T.ask({
              prompt: "Which key puts exactly the right items together?",
              options: opts.map(([i, label]) => ({ value: i, label: h("code", {}, label) })),
              answer: right,
              why: (v) => {
                const key = g.keys[v][1];
                for (const a of g.items) for (const b of g.items) {
                  if (a >= b) continue;
                  const same = key(a) === key(b), should = g.truth(a) === g.truth(b);
                  if (same && !should) return `With ${g.keys[v][0]}, ${a} and ${b} both get the key ${key(a)}, but they don't belong together.`;
                }
                for (const a of g.items) for (const b of g.items) {
                  if (a >= b) continue;
                  if (key(a) !== key(b) && g.truth(a) === g.truth(b)) return `${a} and ${b} belong together, but ${g.keys[v][0]} gives them different keys: ${key(a)} and ${key(b)}.`;
                }
                return "That key doesn't match the grouping.";
              },
              note: `${truthGroups.size} groups, each in one lookup.`,
            });
            const key = g.keys[right][1];
            ctx.draw(V.line(h("strong", {}, g.goal)),
              V.kv([...groupBy(g.items, key).entries()].map(([k, list]) => [k, list.join("  ")]), { label: `groups by ${g.keys[right][0]}` }));
            yield T.choose("Groups built. Ready for the next one?", [["go", "Next set"]], "go");
          }
          return { summary: "Test a key by asking two questions: do items that belong together always get the same key, and do items that don't belong together ever share one?" };
        },
      },
    ],
  });

  // ── 05 Recursion ─────────────────────────────────────────────────────────
  function leapCase() {
    const kind = T.pick(["sum", "max", "rev", "pow", "digits", "count"]);
    if (kind === "sum") {
      const a = Array.from({ length: T.rand(4, 5) }, () => T.rand(1, 9));
      const rest = a.slice(1).reduce((x, y) => x + y, 0), ans = a[0] + rest;
      return { code: "def total(a):\n    if not a:\n        return 0\n    return a[0] + total(a[1:])", call: `total([${a}])`, trust: `total([${a.slice(1)}]) returns ${rest}`, ans,
        opts: T.numOptions(ans, { extra: [rest, a[0], rest + 2 * a[0]] }), why: `Add the head to what the smaller call returned: ${a[0]} + ${rest}.` };
    }
    if (kind === "max") {
      const a = Array.from({ length: T.rand(4, 5) }, () => T.rand(1, 20));
      const rest = Math.max(...a.slice(1)), ans = Math.max(a[0], rest);
      return { code: "def biggest(a):\n    if len(a) == 1:\n        return a[0]\n    return max(a[0], biggest(a[1:]))", call: `biggest([${a}])`, trust: `biggest([${a.slice(1)}]) returns ${rest}`, ans,
        opts: T.numOptions(ans, { spread: 5, extra: [rest, a[0], a[0] + rest] }), why: `Compare the head (${a[0]}) with the best of the rest (${rest}).` };
    }
    if (kind === "rev") {
      const s = T.sample(T.letters.slice(0, 12).split(""), T.rand(4, 5)).join("").toLowerCase();
      const rest = s.slice(1).split("").reverse().join(""), ans = rest + s[0];
      return { code: "def rev(s):\n    if s == '':\n        return ''\n    return rev(s[1:]) + s[0]", call: `rev("${s}")`, trust: `rev("${s.slice(1)}") returns "${rest}"`, ans: `"${ans}"`,
        opts: T.shuffle([`"${ans}"`, `"${s[0] + rest}"`, `"${rest}"`, `"${s}"`]), why: `The first letter goes to the end: "${rest}" + "${s[0]}".` };
    }
    if (kind === "pow") {
      const x = T.rand(2, 3), n = T.rand(5, 11), half = x ** Math.floor(n / 2), ans = x ** n;
      return { code: "def power(x, n):\n    if n == 0:\n        return 1\n    half = power(x, n // 2)\n    if n % 2 == 0:\n        return half * half\n    return half * half * x", call: `power(${x}, ${n})`, trust: `power(${x}, ${Math.floor(n / 2)}) returns ${half}`, ans,
        opts: T.shuffle([...new Set(n % 2 ? [ans, half * half, half * x, ans * x, half * 2] : [ans, half * half * x, half * x, half * 2, ans * x])].slice(0, 4)),
        why: n % 2 ? `${n} is odd, so n // 2 = ${Math.floor(n / 2)} leaves one x over: ${half} × ${half} × ${x}.` : `${n} is even: ${half} × ${half}.` };
    }
    if (kind === "digits") {
      const n = T.rand(100, 9999), rest = String(Math.floor(n / 10)).split("").reduce((s, d) => s + Number(d), 0), ans = rest + (n % 10);
      return { code: "def digit_sum(n):\n    if n < 10:\n        return n\n    return n % 10 + digit_sum(n // 10)", call: `digit_sum(${n})`, trust: `digit_sum(${Math.floor(n / 10)}) returns ${rest}`, ans,
        opts: T.numOptions(ans, { extra: [rest, rest + Math.floor(n / 10) % 10] }), why: `n % 10 is the last digit (${n % 10}). Add it to ${rest}.` };
    }
    const x = T.rand(1, 3), a = Array.from({ length: T.rand(5, 6) }, () => T.rand(1, 3));
    const rest = a.slice(1).filter((v) => v === x).length, ans = rest + (a[0] === x ? 1 : 0);
    return { code: "def count(a, x):\n    if not a:\n        return 0\n    return (a[0] == x) + count(a[1:], x)", call: `count([${a}], ${x})`, trust: `count([${a.slice(1)}], ${x}) returns ${rest}`, ans,
      opts: T.numOptions(ans, { spread: 2, extra: [rest + 1, rest] }), why: `Does the head equal ${x}? ${a[0] === x ? "Yes, so add 1" : "No, so add 0"} to ${rest}.` };
  }

  const BASES = [
    ["def fact(n):\n    return n * fact(n - 1)", "forever", "No base case at all. It counts down through 0 into the negatives until Python raises RecursionError."],
    ["def fact(n):\n    if n == 0:\n        return 0\n    return n * fact(n - 1)", "wrong", "The base case returns 0, and 0 times anything is 0. Every answer is 0. It should return 1."],
    ["def countdown(n):\n    if n == 0:\n        return\n    countdown(n - 2)\n\ncountdown(7)", "forever", "7, 5, 3, 1, −1… it steps right over 0. Use n <= 0."],
    ["def total(a):\n    if not a:\n        return 0\n    return a[0] + total(a[1:])\n\ntotal([4, 1, 6])", "works", "Each call shrinks the list by one, and the empty list returns 0."],
    ["def power(x, n):\n    if n == 0:\n        return 1\n    half = power(x, n // 2)\n    return half * half\n\npower(2, 5)", "wrong", "For odd n, n // 2 drops one x. power(2, 5) returns 16. The odd case needs an extra × x."],
    ["def length(a):\n    if len(a) == 1:\n        return 1\n    return 1 + length(a[1:])\n\nlength([])", "forever", "The base case expects one item, but [] has none. [][1:] is still [], so it never shrinks."],
    ["def fib(n):\n    if n <= 1:\n        return n\n    return fib(n - 1) + fib(n - 2)\n\nfib(10)", "works", "Both calls get smaller and n <= 1 catches both 0 and 1. It's slow, but correct."],
    ["def fib(n):\n    if n == 1:\n        return 1\n    return fib(n - 1) + fib(n - 2)\n\nfib(5)", "forever", "fib(2) calls fib(0), which misses the base case and keeps going negative. Both 0 and 1 need covering."],
    ["def to_binary(n):\n    if n == 0:\n        return ''\n    return to_binary(n // 2) + str(n % 2)\n\nto_binary(6)", "works", "6 → 3 → 1 → 0, building '110' on the way back up."],
    ["def has(a, x):\n    if a[0] == x:\n        return True\n    return has(a[1:], x)\n\nhas([3, 1], 9)", "forever", "With no empty-list case, it reaches has([], 9). a[0] raises IndexError: the recursion never had a way to say False."],
    ["def flat(a):\n    out = []\n    for x in a:\n        if isinstance(x, list):\n            out += flat(x)\n        else:\n            out.append(x)\n    return out\n\nflat([1, [2, [3]]])", "works", "The base case is hidden: a list with no sublists just loops and returns."],
    ["def gcd(a, b):\n    if b == 0:\n        return a\n    return gcd(b, a % b)\n\ngcd(48, 18)", "works", "a % b is always smaller than b, so b shrinks to 0. You get 6."],
  ];

  function fibTree(n) {
    const node = { arg: n, kids: [] };
    if (n > 1) node.kids = [fibTree(n - 1), fibTree(n - 2)];
    return node;
  }
  const calls = (n) => (n <= 1 ? 1 : 1 + calls(n - 1) + calls(n - 2));

  T.topic({
    id: "recursion", n: 5, stage: STAGE,
    title: "Recursion",
    idea: "Don't trace every call. Assume the smaller call already works (the leap of faith), write the one step that turns its answer into yours, and make sure the shrinking ends at a base case.",
    signals: "The input contains a smaller copy of itself: a list minus its head, a tree's subtrees, n − 1, n // 2.",
    invariant: "Every call gets strictly closer to a base case, and the base case returns the right answer for the smallest input.",
    drills: [
      {
        id: "leap", name: "Leap of faith",
        blurb: "You're handed the smaller call's answer. Trust it. What does this call return?",
        *play(ctx) {
          for (let r = 0; r < 5; r++) {
            const c = leapCase();
            ctx.draw(V.code(c.code), V.line("Calling ", V.k(c.call)), V.line("Trust this: ", V.k(c.trust)));
            yield T.choose(`So ${c.call} returns…`, c.opts, c.ans, () => c.why, c.why);
          }
          return { summary: "Each function is one line of real work plus a trusted call. That's the whole trick." };
        },
      },
      {
        id: "base", name: "Will it stop?",
        blurb: "Most recursion bugs live in the base case. Read each function and call it.",
        *play(ctx) {
          for (const [code, ans, why] of T.sample(BASES, 5)) {
            ctx.draw(V.code(code));
            yield T.choose("What happens?", [["works", "Works"], ["wrong", "Stops, wrong answer"], ["forever", "Never stops or crashes"]], ans, () => why, why);
          }
          return { summary: "Check two things: does every path hit a base case, and is the base case's value right?" };
        },
      },
      {
        id: "calls", name: "Count the calls",
        blurb: "Naive fib makes two calls per call. Guess how many calls that adds up to, then see where they repeat.",
        *play(ctx) {
          const n = T.rand(4, 6);
          const code = V.code("def fib(n):\n    if n <= 1:\n        return n\n    return fib(n - 1) + fib(n - 2)");
          ctx.draw(code, V.line("Calling ", V.k(`fib(${n})`)));
          const total = calls(n);
          yield T.choose(`How many calls happen in total, counting fib(${n}) itself?`, T.numOptions(total, { spread: 5, min: n, extra: [n + 1, 2 ** n] }), total,
            (v) => (v === n + 1 ? "That's the number of different arguments. But each one is computed many times." : v === 2 ** n ? "Close in spirit, but the right branch is shorter, so it's a bit less than 2ⁿ." : "Count it level by level: calls(n) = 1 + calls(n − 1) + calls(n − 2)."),
            `${total} calls.`);
          const tones = ["pa", "pb", "pc", "pd", "", "hot", "ok"];
          const tree = fibTree(n);
          ctx.draw(code, V.label(`Every call fib(${n}) makes. Same colour = same argument, recomputed.`),
            V.ntree([tree], { kids: (x) => x.kids, label: (x) => x.arg, cls: (x) => tones[x.arg % tones.length], gap: n >= 6 ? 32 : 38, dy: 50, r: 14 }));
          yield T.choose("With a memo (a cache of finished answers), how many calls do real work?", T.numOptions(n + 1, { spread: 3, min: 1, extra: [total, n] }), n + 1,
            (v) => (v === total ? "The memo returns repeats instantly, so only the first fib(k) for each k computes." : `There are only ${n + 1} different arguments: 0 to ${n}. Each is computed once.`),
            `Only fib(0) to fib(${n}): ${n + 1} calls do real work.`);
          yield T.choose("Without a memo, roughly how many calls does fib(30) make?",
            [["a", "about 31"], ["b", "about 900"], ["c", "about 2.7 million"], ["d", "about 10¹⁸"]], "c",
            "It grows by about 1.6× per step of n: 1.6³⁰ ≈ 2.7 million. With a memo it's 31.",
            "2,692,537 calls, against 31 with a memo. That's why memoising is the first step towards DP.");
          return { summary: "Repeated subproblems are what make naive recursion exponential, and a memo removes them." };
        },
      },
    ],
  });
})();
