"use strict";
(function () {
  const T = window.Trace;
  const { h, V } = T;

  const P = {
    hash: "Hash map / set", two: "Two pointers", window: "Sliding window", prefix: "Prefix sums + hash map",
    bs: "Binary search", bsAns: "Binary search on the answer", sort: "Sort, then sweep", greedy: "Greedy",
    stack: "Monotonic stack", stackPlain: "Stack", heap: "Heap", bfs: "BFS", dfs: "DFS / flood fill", topo: "Topological sort",
    uf: "Union-find", dijkstra: "Dijkstra", back: "Backtracking", dp: "Dynamic programming", trie: "Trie", bits: "Bit trick",
    fastslow: "Fast and slow pointers", deque: "Monotonic deque",
  };
  const Q = [
    ["Given an unsorted array, return the indexes of two numbers that add up to a target.", "hash", "Unsorted plus a pair: store what you've seen and look up the complement."],
    ["Given a sorted array, return two numbers that add up to a target, using O(1) extra space.", "two", "Sorted plus a pair plus O(1) space: pointers at both ends."],
    ["Find the length of the longest substring with at most k distinct characters.", "window", "Contiguous, longest, at most k: grow and shrink a window."],
    ["Count the subarrays whose sum equals k. The array contains negative numbers.", "prefix", "Negatives break windows. Running sums plus a map of counts works."],
    ["Find the minimum eating speed that finishes all piles within h hours.", "bsAns", "\"Minimum value such that a monotonic check passes\" means binary searching the value."],
    ["Merge all overlapping meeting intervals.", "sort", "Sort by start, then each interval only touches the previous block."],
    ["For each day, find how many days until a warmer temperature.", "stack", "Next greater element: a stack of days still waiting."],
    ["Return the k most frequent elements.", "heap", "Top k of something: count, then keep a heap of size k (or bucket sort)."],
    ["Find the minimum number of moves for a knight to reach a square on an empty board.", "bfs", "Minimum moves with every move costing the same: BFS."],
    ["Count the islands of 1s in a grid of 0s and 1s.", "dfs", "Connected regions: flood each one."],
    ["Given course prerequisites, decide whether every course can be finished.", "topo", "Dependencies and \"can we finish\" means detecting a cycle with topological sort."],
    ["Edges arrive one by one. Report the first edge that creates a cycle.", "uf", "Connectivity as edges arrive: union-find. The first union whose ends are already connected is the answer."],
    ["Find the fastest time for a signal to reach every node, given edge travel times.", "dijkstra", "Weighted shortest paths with positive weights."],
    ["Return every possible subset of a list of distinct numbers.", "back", "\"Every possible\" with small n: build choices and undo them."],
    ["Find the fewest coins that add up to an amount.", "dp", "Minimum over choices with overlapping subproblems. Greedy fails on some coin sets."],
    ["Implement autocomplete: return all dictionary words starting with a typed prefix.", "trie", "Prefixes shared across many words: a trie."],
    ["Every element appears twice except one. Find it in O(1) extra space.", "bits", "Pairs cancel under XOR."],
    ["Decide whether a linked list has a cycle, using O(1) memory.", "fastslow", "Two speeds always meet inside a cycle."],
    ["Return the maximum of every window of size k.", "deque", "Window max: a deque of candidates, decreasing from front to back."],
    ["Check whether a string of brackets is properly nested.", "stackPlain", "Nesting: the most recent opener must close first."],
    ["Return the length of the longest increasing subsequence.", "dp", "A subsequence (not contiguous) with an optimal choice per element. Classic DP (or patience sorting with binary search)."],
    ["Find the longest common subsequence of two strings.", "dp", "Two strings and an optimum: a 2D table over prefixes."],
    ["Find the kth largest element in a stream of numbers.", "heap", "A min-heap of size k; its top is the answer."],
    ["Find the first and last position of a target in a sorted array.", "bs", "Sorted: two binary searches (lower and upper bound)."],
    ["Find the maximum area of water held between two vertical lines.", "two", "Start wide and move the shorter wall inward."],
    ["Find the minimum number of meeting rooms needed.", "heap", "Sort by start, then a min-heap of end times. (A sweep over start and end points also works.)"],
    ["Can you reach the last index if each value is your maximum jump length?", "greedy", "Track the farthest reachable index. No need to try every path."],
    ["Return all ways to place n queens on an n×n board so that no two attack.", "back", "Place row by row and undo when stuck."],
    ["Shortest path in a grid where some cells are walls, moving in 4 directions.", "bfs", "Unweighted grid shortest path: BFS rings."],
    ["Count the connected groups in a network of friendships, given as a list of pairs.", "uf", "Groups from pairs: union them and count the roots (DFS also works)."],
    ["Find the smallest subarray length with a sum ≥ target. All numbers are positive.", "window", "Positive numbers and a shortest contiguous range: shrink while it's valid."],
    ["Answer many queries for the sum of nums[i..j] on a fixed array.", "prefix", "Fixed array, many range sums: precompute running totals."],
    ["Count the 1 bits in every number from 0 to n.", "bits", "bits[i] = bits[i >> 1] + (i & 1): a bit trick plus DP."],
    ["Find the minimum in a rotated sorted array.", "bs", "One half is always sorted, so binary search for the drop."],
    ["Find the number of distinct ways to climb n stairs, taking 1 or 2 steps.", "dp", "Last move was 1 or 2: ways[n] = ways[n−1] + ways[n−2]."],
    ["Design a structure that returns the median as numbers stream in.", "heap", "Two heaps: a max-heap for the low half and a min-heap for the high half."],
  ];
  const ALL = Object.keys(P);

  T.topic({
    id: "spot-pattern", n: 99, stage: "Review",
    title: "Spot the pattern",
    idea: "In an interview, the hard part is recognising which tool the problem wants. The wording almost always gives it away: sorted, contiguous, minimum such that, every possible, dependencies.",
    signals: "Use this after a few topics are solid, and come back to it often. It mixes everything.",
    invariant: "Read the constraints and the shape of the answer before you think about code.",
    drills: [
      {
        id: "spot", name: "Name it",
        blurb: "Read the problem and pick the technique you'd reach for first.",
        *play(ctx) {
          const qs = T.sample(Q, 8);
          for (const [i, [text, ans, why]] of qs.entries()) {
            ctx.draw(V.label(`Problem ${i + 1} of ${qs.length}`), h("p", { class: "line", style: "font-size:19px;font-weight:600;max-width:60ch" }, text));
            const opts = T.shuffle([ans, ...T.sample(ALL.filter((k) => k !== ans && P[k] !== P[ans]), 3)]);
            yield T.choose("Which pattern?", opts.map((k) => [k, P[k]]), ans, (v) => `Not ${P[v].toLowerCase()}. ${why}`, why);
          }
          return { summary: "If you missed some, go back to those topics. Recognising the pattern comes from having run it by hand." };
        },
      },
    ],
  });
})();
