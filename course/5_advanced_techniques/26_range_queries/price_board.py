"""
Live price board                                                               [build]

A trading dashboard tracks the latest price for each of n instruments and must
answer range questions instantly while prices keep changing. Build it on a
segment tree.

    b = PriceBoard([5, 3, 8, 6])
    b.max_in(0, 3)    ->  8              highest price in positions 0..3 (inclusive)
    b.sum_in(1, 2)    ->  11
    b.update(2, 1)
    b.max_in(0, 3)    ->  6
    b.argmax(0, 3)    ->  3              position of the highest price (smallest index on a tie)

Rules:
  - All ranges are inclusive, 0 <= l <= r < n.
  - argmax returns the smallest index holding the maximum.

Aim for:  O(log n) for every method. The last test has 100,000 operations on 50,000 prices.
Hint:     One segment tree whose nodes store (sum, max, index of max). Combining two children:
          sums add, and the max with its index comes from the larger side (the left one on a tie).
          The iterative bottom-up tree (size 2n) is short and fast in Python.
"""


class PriceBoard:
    def __init__(self, prices: list[int]):
        raise NotImplementedError

    def update(self, i: int, price: int) -> None:
        raise NotImplementedError

    def max_in(self, l: int, r: int) -> int:
        raise NotImplementedError

    def sum_in(self, l: int, r: int) -> int:
        raise NotImplementedError

    def argmax(self, l: int, r: int) -> int:
        raise NotImplementedError


CLASS = "PriceBoard"


def _sim(prices, ops):
    p, out = list(prices), [None]
    for op in ops:
        name, a, b = op
        if name == "update":
            p[a] = b; out.append(None)
        elif name == "max_in":
            out.append(max(p[a:b + 1]))
        elif name == "sum_in":
            out.append(sum(p[a:b + 1]))
        else:
            seg = p[a:b + 1]
            out.append(a + seg.index(max(seg)))
    return out


def _ops(rng, n, m):
    ops = []
    for _ in range(m):
        kind = rng.choice(["update", "max_in", "sum_in", "argmax"])
        if kind == "update":
            ops.append(("update", rng.randrange(n), rng.randint(1, 50)))
        else:
            l = rng.randrange(n)
            ops.append((kind, l, rng.randint(l, n - 1)))
    return ops


def _fast_sim(prices, ops):
    n = len(prices)
    size = 1
    while size < n:
        size *= 2
    NEG = (float("-inf"), 0)
    s = [0] * (2 * size)
    mx = [NEG] * (2 * size)
    for i, v in enumerate(prices):
        s[size + i], mx[size + i] = v, (v, -i)
    for i in range(size - 1, 0, -1):
        s[i] = s[2 * i] + s[2 * i + 1]
        mx[i] = max(mx[2 * i], mx[2 * i + 1])
    out = [None]
    for name, a, b in ops:
        if name == "update":
            i = size + a
            s[i], mx[i] = b, (b, -a)
            i //= 2
            while i:
                s[i] = s[2 * i] + s[2 * i + 1]
                mx[i] = max(mx[2 * i], mx[2 * i + 1])
                i //= 2
            out.append(None)
            continue
        lo, hi, tot, best = a + size, b + size + 1, 0, NEG
        while lo < hi:
            if lo & 1:
                tot += s[lo]; best = max(best, mx[lo]); lo += 1
            if hi & 1:
                hi -= 1; tot += s[hi]; best = max(best, mx[hi])
            lo //= 2; hi //= 2
        out.append(best[0] if name == "max_in" else tot if name == "sum_in" else -best[1])
    return out


def _cases():
    import random
    rng = random.Random(209)
    out = []
    for _ in range(4):
        n = rng.randint(1, 10)
        prices = [rng.randint(1, 50) for _ in range(n)]
        ops = _ops(rng, n, 25)
        out.append(([("PriceBoard", prices)] + ops, _sim(prices, ops)))
    n = 50_000
    prices = [rng.randint(1, 10**6) for _ in range(n)]
    ops = _ops(rng, n, 100_000)
    out.append(([("PriceBoard", prices)] + ops, _fast_sim(prices, ops)))
    return out


TESTS = [([("PriceBoard", [5, 3, 8, 6]), ("max_in", 0, 3), ("sum_in", 1, 2), ("update", 2, 1), ("max_in", 0, 3),
           ("argmax", 0, 3)], [None, 8, 11, None, 6, 3]),
         ([("PriceBoard", [4, 4, 4]), ("argmax", 0, 2), ("argmax", 1, 2), ("sum_in", 0, 0)], [None, 0, 1, 4])] + _cases()
