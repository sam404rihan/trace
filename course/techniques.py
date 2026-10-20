"""Every technique a problem may rely on. Each one is taught by exactly one basic problem (the one
that lists it in TEACHES), earlier in the course than any problem that lists it in USES.
`python server.py --check coverage` enforces this. Explanations: 2-4 sentences, inline `code` allowed.
A problem's USES lists every technique it uses directly, not just the newest one, so its Uses row
shows everything it relies on."""

TECHNIQUES = {
    "hash.set_lookup": {
        "name": "Set for fast lookups",
        "explain": "`x in some_list` scans the whole list, but `x in some_set` is one hash lookup. When a loop keeps "
                   "asking \"is x in there?\", build a set (or dict) once before the loop and the inner search "
                   "disappears: O(n * m) becomes O(n + m).",
    },
    "scan.best_so_far": {
        "name": "Best so far",
        "explain": "To find the best pair i < j, walk j once and remember the best i you've passed: the smallest "
                   "price, the largest value. Each j only needs that one number, so every pair is checked in O(n) "
                   "instead of O(n²).",
    },
    "pairs.split_by_index": {
        "name": "Separating i from j",
        "explain": "Rewrite a pair's score or condition so one part uses only i and the other only j: "
                   "`values[i] + values[j] + i - j` is `(values[i] + i) + (values[j] - j)`. Then each index has "
                   "its own number, and best so far or a dict of counts does the rest.",
    },
    "hash.count_pairs": {
        "name": "Counting pairs with a dict",
        "explain": "To count pairs i < j with equal values, walk once with a dict of how many times each value has "
                   "appeared so far. A new x pairs with every earlier x, so add `seen[x]` to the answer, then "
                   "increase `seen[x]`. One pass instead of checking every pair.",
    },
    "array.wrap_index": {
        "name": "Wrapping around with %",
        "explain": "`(i + k) % n` keeps an index inside 0..n - 1 however far it moves, and in Python it works for "
                   "negative k too. Use it for anything circular: rotating a list, a clock, a ring of seats. Doing "
                   "`k %= n` first also stops a huge k from going round extra times.",
    },
    "matrix.boundaries": {
        "name": "Shrinking boundaries",
        "explain": "Keep four edges: top, bottom, left and right. Walk along one edge, then move it inward by one, "
                   "and stop once top > bottom or left > right. Check those again before the third and fourth "
                   "sides, or a single row or column gets read twice.",
    },
    "array.write_pointer": {
        "name": "Write pointer",
        "explain": "Keep an index `w` for where the next kept item goes. Walk the list, copy each item you keep to "
                   "`a[w]` and add 1 to `w`. Everything before `w` is the answer so far, built in place in one pass "
                   "with no extra list.",
    },
    "math.carry": {
        "name": "Carrying digits",
        "explain": "Add digit by digit from the right, as on paper. A column's total gives the digit `total % 10` "
                   "and carries `total // 10` into the next column to the left. A carry left over at the end "
                   "becomes a new leading digit.",
    },
    "array.left_right_passes": {
        "name": "Left and right passes",
        "explain": "When the answer at i depends on both sides of i, make one pass left to right that carries what "
                   "you know about everything before i, and one pass right to left for everything after it. "
                   "Combine the two at each i: two O(n) passes instead of searching both ways from every index.",
    },
    "hash.seen_set": {
        "name": "Seen set",
        "explain": "Walk once with an empty set. For each item, first ask `if x in seen`, and only then "
                   "`seen.add(x)`. The set answers \"have I met this before?\" in O(1), so a repeat or a loop "
                   "shows up the moment it happens.",
    },
    "hash.run_starts": {
        "name": "Starting runs at their first number",
        "explain": "To measure runs of consecutive numbers, put them in a set and only start counting at an x whose "
                   "x - 1 is missing: that x begins a run. Walk up x + 1, x + 2, ... while they're in the set. Each "
                   "number is looked at about twice, so it's O(n) without sorting.",
    },
    "hash.complement": {
        "name": "Complement lookup",
        "explain": "When two values must add up to a target, x's partner is `target - x`. Keep a dict of the values "
                   "you've passed (value → index) and look the partner up before you add x, so x can't pair with "
                   "itself. One pass instead of trying every pair.",
    },
    "hash.group_key": {
        "name": "Grouping by a computed key",
        "explain": "When items belong together because they share something you can compute (first and last letter, "
                   "sorted letters, `r - c` for a diagonal), use that as a dict key: "
                   "`groups.setdefault(key(x), []).append(x)`. The skill is choosing the key.",
    },
    "recursion.trust": {
        "name": "Base case and a smaller call",
        "explain": "Answer the smallest input directly: that's the base case. For anything bigger, call the function "
                   "on a smaller piece, trust it to be right, and build your answer from it. Every call must move "
                   "toward the base case.",
    },
    "recursion.memo": {
        "name": "Memoisation",
        "explain": "When a recursive function is called again and again with the same arguments, remember each "
                   "answer: put `@cache` above it, or keep a dict. Each distinct call is then worked out once, which "
                   "can turn exponential time into the number of distinct calls.",
    },
    "recursion.parse": {
        "name": "Parsing with recursion",
        "explain": "Write `parse(i)` that reads the piece of text starting at index i and returns (its value, the "
                   "index just after it). When it meets an opening bracket, it calls itself for the inside and "
                   "carries on from the index that call returns.",
    },
    "pointers.opposite_ends": {
        "name": "Pointers at both ends",
        "explain": "Put `left` at the start and `right` at the end, and move them towards each other. On a sorted "
                   "list, a pair sum that's too small means nums[left] can't work with anything left, so move left "
                   "up; too big means move right down. Each step rules out one item for good: O(n) instead of "
                   "trying every pair.",
    },
    "pointers.two_sequences": {
        "name": "One pointer per list",
        "explain": "To walk two sequences together, keep an index into each. Each step compares `a[i]` with `b[j]` "
                   "and moves one of them on, or both: merging takes the smaller, and matching a subsequence moves "
                   "j only on a match. Neither pointer ever goes back, so it's O(len(a) + len(b)).",
    },
    "window.fixed": {
        "name": "Fixed-size window",
        "explain": "When a window of k items slides one step right, one item enters (`nums[right]`) and one leaves "
                   "(`nums[right - k]`). Update the sum or the counts with just those two: O(1) per step instead "
                   "of O(k).",
    },
    "window.variable": {
        "name": "Growing and shrinking a window",
        "explain": "Move `right` one step at a time to grow the window. Whenever it breaks the rule (too many kinds, "
                   "too big a sum), move `left` forward until it's fine again, undoing what leaves. Each index "
                   "enters once and leaves once, so it's O(n). For the longest good window, record its size after "
                   "shrinking.",
    },
    "window.shortest": {
        "name": "Shortest window",
        "explain": "For the SHORTEST window that works, grow `right` until the window is good. Then, while it's "
                   "still good, record its length and shrink from the left. The longest-window version shrinks "
                   "while the window is broken; this one shrinks while it works.",
    },
    "window.count": {
        "name": "Counting with a window",
        "explain": "To count windows instead of finding the best one: once [left, right] is good, every start from "
                   "left to right is good for this end too, so add `right - left + 1`. \"Exactly k\" can't be "
                   "shrunk towards this way, but \"at most k\" can, so exactly(k) = at_most(k) - at_most(k - 1).",
    },
    "prefix.sums": {
        "name": "Prefix sums",
        "explain": "Build P with `P[0] = 0` and `P[k + 1] = P[k] + nums[k]`, so P[k] is the sum of the first k "
                   "numbers. Then the sum of nums[i..j] is `P[j + 1] - P[i]`: one subtraction instead of a loop.",
    },
    "prefix.count_dict": {
        "name": "Counting earlier prefix sums",
        "explain": "nums[i:j] adds up to k exactly when P[j] - P[i] == k. So walk once with a running total and a "
                   "dict counting the totals seen so far, starting with `{0: 1}` for the empty start, and at each "
                   "step add how many earlier totals equal `total - k`. Unlike a sliding window, this works with "
                   "negative numbers.",
    },
    "prefix.difference": {
        "name": "Difference array",
        "explain": "To add v to every index from l to r, touch only the ends: `diff[l] += v` and "
                   "`diff[r + 1] -= v`. After all the updates, a running total of diff gives each index's value. "
                   "Each update is O(1), and one pass at the end does the rest.",
    },
    "bsearch.first_true": {
        "name": "Binary search for the first yes",
        "explain": "Binary search keeps a range that must hold the answer and halves it each step, so it's O(log n). "
                   "The most reusable form finds the first index where a yes/no question turns yes, such as the "
                   "first `nums[i] >= x`: `lo, hi = 0, len(nums)`, then while lo < hi, set `hi = mid` on yes and "
                   "`lo = mid + 1` on no.",
    },
    "bsearch.on_answer": {
        "name": "Binary search on the answer",
        "explain": "When the answer is a number and \"does c work?\" flips from no to yes once as c grows, binary "
                   "search over c itself, between the smallest and the largest possible answer. Write the check as "
                   "its own function. It's often one greedy pass, such as filling each day until the next item "
                   "won't fit.",
    },
    "intervals.overlap": {
        "name": "Do two intervals overlap?",
        "explain": "[a, b] and [c, d] overlap when `a <= d and c <= b`. It's easier to see the other way round: "
                   "they don't overlap when one ends before the other starts. Use `<` instead of `<=` when "
                   "touching shouldn't count.",
    },
    "intervals.merge": {
        "name": "Absorbing an overlap",
        "explain": "When an interval overlaps the one you're building, swallow it: `start = min(start, s)` and "
                   "`end = max(end, e)`. The max matters, because [1, 10] swallows [2, 3]. Intervals that don't "
                   "overlap are copied as they are.",
    },
    "intervals.sort_by_start": {
        "name": "Sort by start, then compare neighbours",
        "explain": "Once intervals are sorted by start, each one can only overlap its neighbours. One pass then "
                   "compares each interval with the one before it, or with the last one you kept, instead of "
                   "every pair: O(n log n) for the sort and O(n) for the pass.",
    },
    "intervals.earliest_end": {
        "name": "Earliest end first",
        "explain": "To keep the most intervals that don't overlap, sort by END and keep each one that starts at or "
                   "after the last kept end. The interval that ends first leaves the most room for the rest, so "
                   "taking it is never a mistake.",
    },
    "greedy.kadane": {
        "name": "Extend or restart",
        "explain": "Walking left to right, the best run ending at x either continues the run before it or starts "
                   "fresh at x: `cur = max(x, cur + x)`. A run with a negative total only drags down whatever "
                   "follows, so drop it and restart. This is Kadane's algorithm: O(n) time, O(1) space.",
    },
    "greedy.farthest_reach": {
        "name": "Farthest reach",
        "explain": "Walk left to right keeping `far`, the farthest index you can reach so far: "
                   "`far = max(far, i + nums[i])`. If i ever passes far, you're stuck. To count jumps, treat each "
                   "jump as a level: when i reaches the end of the current level, jump once, and the next level "
                   "ends at far.",
    },
    "brackets.balance": {
        "name": "Counting open brackets",
        "explain": "With one kind of bracket, a counter does a stack's job. Walk once keeping `open`, the number of "
                   "\"(\" not closed yet: add 1 for \"(\" and take 1 off for \")\". If it would drop below 0, that "
                   "\")\" has nothing to close; if it ends above 0, some \"(\" were never closed.",
    },
    "greedy.forced_first": {
        "name": "The forced first move",
        "explain": "Go left to right. Often the first thing that's still wrong can only be fixed one way: a flip "
                   "must start there, or the smallest card must start a group. Make that forced move and carry "
                   "on. There's no choice to search, so it's one pass.",
    },
    "stack.lifo": {
        "name": "Stack: last in, first out",
        "explain": "A Python list is a stack: `append` puts an item on top and `pop` takes the top off, both O(1). "
                   "Use one whenever the most recent unfinished thing must be dealt with first: the last opened "
                   "bracket, the folder you just went into, the last edit to undo.",
    },
    "stack.monotonic": {
        "name": "Monotonic stack",
        "explain": "Keep a stack of indexes whose values only go down. When a new value is bigger than the top, "
                   "pop until it isn't: each popped index has just found its next bigger value, the new one. Every "
                   "index is pushed and popped once, so the scan is O(n). Flip the comparison for the next smaller.",
    },
    "deque.monotonic": {
        "name": "Monotonic deque",
        "explain": "For the maximum of a sliding window, keep a deque of indexes whose values go down from front to "
                   "back. Before adding a new index, pop smaller values off the back: they can never be the max "
                   "again. Pop the front once it slides out of the window. The front is always the window's max.",
    },
    "grid.neighbors": {
        "name": "Grid neighbours",
        "explain": "A cell (r, c) has up to four neighbours: (r - 1, c), (r + 1, c), (r, c - 1) and (r, c + 1). "
                   "Check `0 <= nr < rows and 0 <= nc < cols` before you look at one, and skip walls.",
    },
    "bfs.shortest": {
        "name": "BFS for fewest steps",
        "explain": "Put the start in a queue at distance 0. Pop a cell and give each unvisited neighbour distance + 1 "
                   "before queueing it. The queue hands out cells in order of distance, so the first time you reach "
                   "a cell is along a shortest path.",
    },
    "bfs.multi_source": {
        "name": "Multi-source BFS",
        "explain": "When there are several starts, put all of them in the queue at distance 0 before the loop. The "
                   "search then spreads from every start at once, and each cell gets its distance to the nearest start.",
    },
    "dfs.flood_fill": {
        "name": "Flood fill",
        "explain": "From one cell, visit every connected cell that matches (same colour, open floor), marking each "
                   "one as you reach it so it's never visited twice. A stack (DFS) or a queue (BFS) both cover the "
                   "whole region.",
    },
    "graph.components": {
        "name": "Counting connected regions",
        "explain": "Scan every cell (or node). Each time you find one you haven't visited, that's a new region: "
                   "count it, then flood fill the whole region so none of its cells starts a region again.",
    },
    "graph.adjacency": {
        "name": "Walking a graph from its edges",
        "explain": "When a graph comes as a list of edges, first build an adjacency list: for an undirected edge "
                   "(a, b), add b to a's list and a to b's. Then BFS or DFS with a `seen` set. The same walk works "
                   "when nodes link to their neighbours directly, like `node.neighbors`.",
    },
    "graph.groups": {
        "name": "BFS over groups",
        "explain": "When nodes belong to groups (stops and buses, people and clubs), index each node to its groups and "
                   "let a whole group count as one step. Mark a group used the first time you expand it, so its "
                   "members are scanned once, not once per member.",
    },
    "flood.from_targets": {
        "name": "Searching back from the targets",
        "explain": 'Instead of asking "can this cell reach the edge?" once per cell, search once FROM the targets '
                   "(often the border cells) and mark everything they reach. One flood from many starts replaces "
                   "one search per cell.",
    },
    "bfs.implicit": {
        "name": "BFS with generated neighbours",
        "explain": "Sometimes nobody lists the neighbours: you work them out from the current state, such as a "
                   "number's x + 1, x - 1 and x * 2, or a word with one letter changed. Generate them inside the "
                   "BFS loop and keep a `seen` set of states.",
    },
    "bfs.state": {
        "name": "BFS over a richer state",
        "explain": "When the same cell can matter twice (before and after picking up a key, say), put the extra "
                   "information into the state: (row, col, has_key). The `seen` set holds whole states, so you "
                   "may stand on a cell once per state.",
    },
    "bfs.path": {
        "name": "Rebuilding the path",
        "explain": "BFS finds distances, not routes. Record each cell's parent (the cell you reached it from) the "
                   "first time you see it. When you reach the goal, follow the parents back to the start and reverse.",
    },
}
