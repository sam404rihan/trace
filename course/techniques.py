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
    "stack.span": {
        "name": "Span between lower bars",
        "explain": "In a stack of indexes with rising heights, when bar i pops bar j, i is the first bar to j's right "
                   "that is lower, and the index left on top of the stack is the last lower bar to its left. So bar "
                   "j's full height spans the gap between them: width `i - stack[-1] - 1`, or `i` if the stack is empty.",
    },
    "deque.monotonic": {
        "name": "Monotonic deque",
        "explain": "For the maximum of a sliding window, keep a deque of indexes whose values go down from front to "
                   "back. Before adding a new index, pop smaller values off the back: they can never be the max "
                   "again. Pop the front once it slides out of the window. The front is always the window's max.",
    },
    "list.reverse": {
        "name": "Reversing links",
        "explain": "Walk the list with `prev`, `curr` and `nxt`: save `nxt = curr.next`, point `curr.next` back at "
                   "`prev`, then step both forward. When curr falls off the end, prev is the new head. Save the next "
                   "node before you overwrite the link, or the rest of the list is lost.",
    },
    "list.dummy": {
        "name": "Dummy head node",
        "explain": "Put a throwaway node in front of the head: `dummy = ListNode(0, head)`. Now every real node, the "
                   "first one included, has a node before it, so inserting or removing at the head needs no special "
                   "case. Return `dummy.next` at the end.",
    },
    "list.fast_slow": {
        "name": "Fast and slow pointers",
        "explain": "Move `slow` one node and `fast` two nodes per step. When fast reaches the end, slow is in the "
                   "middle. If the list loops, fast laps slow and they land on the same node. One pass, O(1) extra "
                   "space.",
    },
    "list.recency": {
        "name": "Recency order: dict plus linked list",
        "explain": "To keep keys ordered by when they were last used, pair a dict with a doubly linked list: the dict "
                   "finds a key's node in O(1), and the list moves it to the newest end or drops the oldest in O(1). "
                   "`collections.OrderedDict` is exactly this: `move_to_end(key)` and `popitem(last=False)`.",
    },
    "list.cycle_start": {
        "name": "Finding where a cycle starts",
        "explain": "Once fast and slow have met inside the loop, put one pointer back at the head and move both one "
                   "step at a time. They meet exactly where the loop begins: the head is as far from the loop's "
                   "start as the meeting point is, going round.",
    },
    "tree.recursion": {
        "name": "Tree recursion",
        "explain": "Answer for an empty tree (None) directly. For a real node, call the function on `node.left` and "
                   "`node.right`, trust both answers, and combine them with the node's own value: "
                   "`1 + count(node.left) + count(node.right)`. Most tree problems are this template.",
    },
    "tree.bfs_levels": {
        "name": "Level-by-level BFS",
        "explain": "Put the root in a deque. At the start of each round, `len(queue)` is the number of nodes on the "
                   "current level: pop exactly that many, handle them, and push their children. Each round is one "
                   "level, top to bottom.",
    },
    "tree.return_and_record": {
        "name": "Return one thing, record another",
        "explain": "Sometimes the parent needs one value (a height) but the answer is another (the longest path "
                   "through some node). Have the helper return what the parent needs and update a `best` variable "
                   "on the side, with `nonlocal`. One walk does both.",
    },
    "tree.carry_down": {
        "name": "Passing values down a path",
        "explain": "When a node's answer depends on what's above it (the sum so far, the biggest value above it, the "
                   "range it must fit in), pass that as an extra argument on the way down: "
                   "`walk(child, total + node.val)`. Each node then knows its whole path in O(1).",
    },
    "tree.inorder": {
        "name": "In-order traversal",
        "explain": "Visit the left subtree, then the node, then the right subtree (pre-order visits the node first, "
                   "post-order last). On a binary search tree in-order gives the values in increasing order. With "
                   "your own stack: go left as far as you can, pushing nodes; pop one, visit it, then do the same "
                   "from its right child.",
    },
    "bst.walk_down": {
        "name": "Walking down a BST",
        "explain": "In a binary search tree everything smaller sits to the left and everything bigger to the right. "
                   "So searching, inserting and many queries walk one path from the root: left if the target is "
                   "smaller, right if bigger. That's O(height), and whole subtrees get skipped.",
    },
    "heap.top_k": {
        "name": "Keeping the k largest",
        "explain": "To track the k largest values, keep a MIN-heap of at most k of them: push each new value, and pop "
                   "when the heap grows past k. The smallest of the k largest, the kth largest, sits on top at "
                   "`heap[0]`. O(log k) per value.",
    },
    "heap.max_negate": {
        "name": "Max-heap by negating",
        "explain": "`heapq` only ever gives you the smallest item. To get the largest, push `-x` and negate again when "
                   "you pop. With tuples, negate the field that should come out biggest first: `(-priority, ...)`.",
    },
    "heap.two_heaps": {
        "name": "Two heaps for the median",
        "explain": "Keep the smaller half of the numbers in a max-heap and the larger half in a min-heap, with every "
                   "value in the first no bigger than every value in the second, and the first one the same size or "
                   "one bigger. The median is the first heap's top, or the average of both tops.",
    },
    "heap.lazy_delete": {
        "name": "Lazy deletion",
        "explain": "A heap can't remove an item from the middle. Instead, mark it as gone (count it in a dict, or keep "
                   "a set of live entries) and leave it where it is. Whenever you look at the top, pop marked items "
                   "first. Each item is still pushed once and popped once.",
    },
    "heap.k_way_merge": {
        "name": "Merging sorted lists with a heap",
        "explain": "To take the smallest items from many sorted lists, put each list's first item in a min-heap "
                   "together with where it came from: `(value, which_list, position)`. Pop the smallest, then push "
                   "the next item from the same list. The heap holds at most one item per list.",
    },
    "trie.walk": {
        "name": "Walking a trie",
        "explain": "A trie stores words letter by letter in nested dicts: `node = node.setdefault(ch, {})` for each "
                   "letter, then mark the end, for example `node[\"$\"] = True`. Words that share a prefix share its "
                   "path, so looking up a word or a prefix takes O(its length).",
    },
    "uf.find": {
        "name": "Union-find: finding the root",
        "explain": "Union-find keeps groups as trees in a `parent` list: `parent[x] == x` means x is the root, the "
                   "group's name. To find x's group, follow parents up to the root. On the way, point the nodes you "
                   "passed straight at the root (path compression), so later finds are nearly instant.",
    },
    "graph.topo_kahn": {
        "name": "Topological order (Kahn's algorithm)",
        "explain": "To order tasks so every prerequisite comes first, count each task's unfinished prerequisites. "
                   "Start a queue with the tasks that have none. Pop one, add it to the order, and take 1 off each "
                   "task that waits on it, queueing any that reach 0. Tasks never reached are stuck in a cycle.",
    },
    "uf.union": {
        "name": "Union-find: merging groups",
        "explain": "To join the groups of a and b, find both roots. If they're the same, a and b were already "
                   "connected, so this link closes a cycle. Otherwise point one root at the other: two groups became "
                   "one. Counting the merges tells you how many groups are left.",
    },
    "sp.relax": {
        "name": "Relaxing an edge",
        "explain": "Keep `dist`, the best distance found so far to each node. For an edge u → v of weight w, if "
                   "`dist[u] + w` beats `dist[v]`, update dist[v]. Every shortest-path algorithm is this one step, "
                   "repeated in a clever order.",
    },
    "sp.dijkstra": {
        "name": "Dijkstra's algorithm",
        "explain": "With no negative weights, pop the closest unsettled node from a min-heap of `(distance, node)`; "
                   "its distance is now final. Relax its edges, pushing every improvement. Skip a popped entry whose "
                   "distance is worse than the one already recorded: it's out of date.",
    },
    "sp.bellman_ford": {
        "name": "Bellman-Ford",
        "explain": "When some edges are negative, Dijkstra can settle a node too early. Instead, relax EVERY edge, "
                   "and repeat that n - 1 times: a cheapest path uses at most n - 1 edges, and each round makes one "
                   "more of them final. Stop early when a round changes nothing. It's O(n · edges).",
    },
    "graph.mst": {
        "name": "Minimum spanning tree",
        "explain": "To connect every node as cheaply as possible, take the cheapest edges first and skip any edge "
                   "that joins two nodes already connected (Kruskal: sort the edges, check with union-find). Prim "
                   "does the same from one node outward with a heap. Either way, n - 1 edges connect n nodes.",
    },
    "graph.euler": {
        "name": "Using every edge once (Hierholzer)",
        "explain": "To find a route that uses every edge exactly once, keep a stack. While the node on top has an "
                   "unused edge, take it and push where it leads. When it has none, pop it onto the route. Reverse "
                   "the route at the end. Loops you would get stuck in are spliced in automatically.",
    },
    "bt.core": {
        "name": "Backtracking: choose, explore, un-choose",
        "explain": "Build a solution one choice at a time. At each step, loop over the choices: make one (append to "
                   "the path), recurse to fill in the rest, then undo it (pop) before trying the next. Record a "
                   "COPY of the path when it's complete, and stop early on branches that can't work.",
    },
    "bt.skip_duplicates": {
        "name": "Skipping duplicate branches",
        "explain": "When the input has repeated values, sort it first. In the loop at each depth, skip a value equal "
                   "to the one just tried at the SAME depth: `if i > start and nums[i] == nums[i - 1]: continue`. "
                   "The same value deeper down is still allowed, so no answer is lost and none is repeated.",
    },
    "dp.recurrence": {
        "name": "Building answers from smaller ones",
        "explain": "Write the answer for position i in terms of answers for smaller positions, like "
                   "`best[i] = max(best[i - 1], best[i - 2] + x)`. Fill them in from the smallest up, so each one is "
                   "ready when it's needed. If only the last two are ever used, two variables are enough.",
    },
    "dp.prefix": {
        "name": "DP over prefixes",
        "explain": "To count or check ways to build a string piece by piece, let `ways[i]` describe the first i "
                   "characters. Work it out from shorter prefixes by asking what the LAST piece could be: one digit, "
                   "two digits, a word ending at i. `ways[0]` is the empty start.",
    },
    "dp.amounts": {
        "name": "DP over amounts",
        "explain": "When you can use items again and again to make a total, let `best[x]` be the answer for the "
                   "amount x. Fill x from 0 upwards: `best[x]` comes from `best[x - c]` for each item c that fits, "
                   "plus one more c. Plain recursion recomputes the same amounts over and over.",
    },
    "dp.lis": {
        "name": "Longest increasing subsequence with tails",
        "explain": "Keep `tails`, where `tails[k]` is the smallest possible last value of an increasing subsequence "
                   "of length k + 1. It stays sorted, so for each x, binary search for the first tail >= x and "
                   "replace it with x, or append x if there's none. The answer is `len(tails)`: O(n log n).",
    },
    "palin.expand": {
        "name": "Expanding around a centre",
        "explain": "Every palindrome has a centre: a letter, or the gap between two letters, so a string of n letters "
                   "has 2n - 1 centres. From each centre, grow outwards while the letters on both ends match. Each "
                   "step that succeeds is one more palindrome.",
    },
    "dp.knapsack01": {
        "name": "0/1 knapsack: reachable sums",
        "explain": "To pick a subset that hits a total, keep which sums are reachable, starting with just 0. For each "
                   "item x, every reachable s makes s + x reachable too. In an array, loop s DOWNWARDS so x isn't "
                   "used twice in one round. It's O(items × total), not 2^items.",
    },
    "dp.two_strings": {
        "name": "A table over two prefixes",
        "explain": "For two strings, let `dp[i][j]` be the answer for the first i letters of a and the first j of b. "
                   "If `a[i - 1] == b[j - 1]`, the two letters can pair up: build on `dp[i - 1][j - 1]`. Otherwise "
                   "drop a letter from one string: `dp[i - 1][j]` or `dp[i][j - 1]`.",
    },
    "dp.grid": {
        "name": "DP on a grid",
        "explain": "When you only move right or down, a cell's answer comes from the cell above and the cell to its "
                   "left. Fill the grid row by row. One row is enough: before you update `row[c]` it still holds "
                   "the cell above, and `row[c - 1]` is the cell to the left.",
    },
    "dp.states": {
        "name": "A few states per step",
        "explain": "When each step can leave you in one of a few situations (holding a share, just sold, resting), "
                   "keep the best total for each state. Every day, work out today's states from yesterday's, all "
                   "at once. It's O(n), with a handful of variables.",
    },
    "dp.interval": {
        "name": "DP over intervals",
        "explain": "When the answer for a run i..j depends on how it splits, let `cost[i][j]` be the answer for that "
                   "run and try every split point k: the parts i..k and k+1..j are shorter runs. So fill the table "
                   "by length, shortest runs first. It's usually O(n³).",
    },
    "bits.shift_mask": {
        "name": "Shifts and masks",
        "explain": "Bit k of x is `(x >> k) & 1`. `1 << k` is a number with only bit k set: use `x | (1 << k)` to "
                   "set the bit, `x & ~(1 << k)` to clear it and `x & (1 << k)` to test it. A whole set of small "
                   "numbers fits in one int this way.",
    },
    "bits.clear_lowest": {
        "name": "Clearing the lowest set bit",
        "explain": "`n & (n - 1)` is n with its lowest 1 bit cleared, because subtracting 1 flips that bit and every "
                   "0 below it. Repeat it to visit only the set bits, or check `n & (n - 1) == 0` to see whether n "
                   "has exactly one bit set.",
    },
    "bits.xor_cancel": {
        "name": "XOR cancels pairs",
        "explain": "`x ^ x == 0` and `x ^ 0 == x`, and the order doesn't matter. So XOR-ing a list cancels every pair "
                   "and leaves whatever is unpaired. It also undoes itself: `a ^ b == c` exactly when `a ^ c == b`.",
    },
    "dp.bitmask": {
        "name": "DP over subsets as bitmasks",
        "explain": "When there are at most about 20 things, a set of them fits in an int: bit s is thing s. Then "
                   "`best[mask]` can be the answer for exactly that set, for all 2^n masks. Go through the masks in "
                   "increasing order, since adding a thing only adds bits: `best[mask | 1 << s]` builds on `best[mask]`.",
    },
    "sort.merge_count": {
        "name": "Merge sort, counting while merging",
        "explain": "Split the list in half, sort each half recursively, then merge them with one pointer per half. "
                   "While merging, when the right half's item goes first, it is smaller than every item still "
                   "waiting on the left, so `len(left) - i` pairs can be counted in one step. It's O(n log n).",
    },
    "fenwick.prefix": {
        "name": "Fenwick tree: prefix sums",
        "explain": "A Fenwick tree is a list where `tree[k]` holds the sum of the `k & -k` elements ending at "
                   "position k (counting from 1). To add up the first i elements, take `tree[i]` and strip i's "
                   "lowest set bit, `i -= i & -i`, until i is 0: at most log n steps.",
    },
    "fenwick.update": {
        "name": "Fenwick tree: updates",
        "explain": "To add delta to element k, add it to `tree[k]` and climb to the next block that covers k with "
                   "`k += k & -k`, until k passes n. Together with prefix sums, range sums over changing values "
                   "are O(log n) both ways. To set a value, add the difference from the old one.",
    },
    "segtree.basic": {
        "name": "Segment tree",
        "explain": "A segment tree keeps one value (a max, a sum) for blocks of the array that halve level by level. "
                   "In a list of length 2 · size, the leaves start at size and node i covers nodes 2i and 2i + 1. "
                   "Changing one element fixes the log n nodes above it; a range query combines about 2 log n blocks.",
    },
    "array.rank_compress": {
        "name": "Compressing values to ranks",
        "explain": "When values are huge or spread out but only their order matters, replace each with its rank: "
                   "`rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}`. Then the values can index small "
                   "arrays and trees directly, from 1 up to the number of distinct values.",
    },
    "str.prefix_function": {
        "name": "The prefix function",
        "explain": "`pi[i]` is the length of the longest proper prefix of `s[:i + 1]` that is also its suffix. Build "
                   "it left to right with k, the current border: while the next character doesn't extend it, fall "
                   "back with `k = pi[k - 1]`. All the fall-backs together are O(n).",
    },
    "str.kmp": {
        "name": "Matching with the prefix function (KMP)",
        "explain": "To find a pattern in a text, build the pattern's prefix function, then walk the text once keeping "
                   "k, how much of the pattern matches right now. On a mismatch, fall back with `k = pi[k - 1]` "
                   "instead of starting over. When k reaches the pattern's length, record a match, and fall back "
                   "the same way after a match too, so overlapping matches aren't missed. O(text + pattern).",
    },
    "sp.floyd": {
        "name": "Floyd–Warshall",
        "explain": "For the shortest path between every pair of nodes, allow each node k as a stopover in turn: for "
                   "every pair (i, j), `dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])`. Once every k has "
                   "had its turn, dist holds every shortest distance. It's O(n³).",
    },
    "sp.negative_cycle": {
        "name": "Detecting a negative cycle",
        "explain": "Start every distance at 0, as if one extra node had a free edge to every node, so every cycle is "
                   "reachable. Relax every edge n - 1 times, as in Bellman-Ford. If any edge can still be relaxed in "
                   "one more round, some cycle has a negative total: nothing else keeps getting cheaper.",
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
