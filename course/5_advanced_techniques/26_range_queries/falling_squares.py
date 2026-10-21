"""
Falling Squares                                                               [hard]

Squares are dropped onto a number line one at a time. positions[i] =
[left, side]: a square with its left edge at x = left and side length `side`
falls straight down until it lands on the ground or on top of an earlier
square (touching only at an edge doesn't count as landing on it). It stays there.

After each drop, record the height of the tallest stack so far. Return the list.

Example:
    falling_squares([[1, 2], [2, 3], [6, 1]])   ->  [2, 5, 5]
        The second square overlaps the first on [2, 3) and lands at height 2: top at 5.
    falling_squares([[100, 100], [200, 100]])   ->  [100, 100]     they only touch at x = 200

Aim for:  O(n log n) with a segment tree (range max + range assign) over compressed x's.
          Comparing each square with every earlier one is O(n²). It scrapes through the big
          test (8,000 squares), but the segment tree is the version that scales.
Hint:     A square covers [left, left + side). Its landing height = max height over that range;
          its top = that + side; then every point in the range becomes top. Compress all the
          left and right edges to indices 0..m-1 (the cells between consecutive edges), and use
          a segment tree with lazy "set the whole range to h" plus "max over a range".
"""


def falling_squares(positions: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _quadratic(positions):
    tops, out, best = [], [], 0
    for left, side in positions:
        right = left + side
        base = max((h for l2, r2, h in tops if l2 < right and left < r2), default=0)
        tops.append((left, right, base + side))
        best = max(best, base + side)
        out.append(best)
    return out


def _segment_tree(positions):
    xs = sorted({x for left, side in positions for x in (left, left + side)})
    index = {x: i for i, x in enumerate(xs)}
    m = len(xs) - 1                                 # cells [xs[i], xs[i + 1])
    top, lazy = [0] * (4 * m), [None] * (4 * m)

    def push(node):
        if lazy[node] is not None:
            for child in (2 * node, 2 * node + 1):
                top[child] = lazy[child] = lazy[node]
            lazy[node] = None

    def query(node, lo, hi, a, b):
        if b < lo or hi < a:
            return 0
        if a <= lo and hi <= b:
            return top[node]
        push(node)
        mid = (lo + hi) // 2
        return max(query(2 * node, lo, mid, a, b), query(2 * node + 1, mid + 1, hi, a, b))

    def assign(node, lo, hi, a, b, h):
        if b < lo or hi < a:
            return
        if a <= lo and hi <= b:
            top[node] = lazy[node] = h
            return
        push(node)
        mid = (lo + hi) // 2
        assign(2 * node, lo, mid, a, b, h)
        assign(2 * node + 1, mid + 1, hi, a, b, h)
        top[node] = max(top[2 * node], top[2 * node + 1])

    out, best = [], 0
    for left, side in positions:
        a, b = index[left], index[left + side] - 1
        h = query(1, 0, m - 1, a, b) + side
        assign(1, 0, m - 1, a, b, h)
        best = max(best, h)
        out.append(best)
    return out


def _cases():
    import random
    rng = random.Random(699)
    out = []
    for _ in range(10):
        pos = [[rng.randint(0, 15), rng.randint(1, 5)] for _ in range(rng.randint(1, 10))]
        out.append(((pos,), _quadratic(pos)))
    big = [[rng.randint(0, 10**8), rng.randint(1, 10**6)] for _ in range(8_000)]
    out.append(((big,), _segment_tree(big)))
    return out


USES = ["segtree.basic", "array.rank_compress"]

TESTS = [
    (([[1, 2], [2, 3], [6, 1]],), [2, 5, 5]),
    (([[100, 100], [200, 100]],), [100, 100]),
    (([[1, 5], [2, 2], [7, 5]],), [5, 7, 7]),
    (([[4, 1], [4, 1], [4, 1]],), [1, 2, 3]),
    (([[1, 1], [2, 1], [3, 1]],), [1, 1, 1]),
] + _cases()
