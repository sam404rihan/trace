"""
Range Sum with Updates                                                       [guided]

Build a class over an array of integers:

    NumArray(nums)
    update(i, val)       set nums[i] = val
    sum_range(l, r)      the sum of nums[l..r], both ends included

Example:
    a = NumArray([1, 3, 5])
    a.sum_range(0, 2)   ->  9
    a.update(1, 2)
    a.sum_range(0, 2)   ->  8
"""


class NumArray:
    def __init__(self, nums: list[int]):
        raise NotImplementedError

    def update(self, i: int, val: int) -> None:
        raise NotImplementedError

    def sum_range(self, l: int, r: int) -> int:
        raise NotImplementedError


CLASS = "NumArray"


def _sim(nums, ops):
    a, out = list(nums), [None]
    for op in ops:
        if op[0] == "update":
            a[op[1]] = op[2]
            out.append(None)
        else:
            out.append(sum(a[op[1]:op[2] + 1]))
    return out


def _random(rng, n, m):
    nums = [rng.randint(-100, 100) for _ in range(n)]
    ops = []
    for _ in range(m):
        if rng.random() < 0.5:
            ops.append(("update", rng.randrange(n), rng.randint(-100, 100)))
        else:
            l = rng.randrange(n)
            ops.append(("sum_range", l, rng.randint(l, n - 1)))
    return [("NumArray", nums)] + ops, nums, ops


def _big():
    import random
    rng = random.Random(202)
    n = 100_000
    nums = [rng.randint(-1000, 1000) for _ in range(n)]
    ops, out, tree = [("NumArray", nums)], [None], [0] * (n + 1)
    vals = list(nums)
    for k, x in enumerate(nums, 1):
        while k <= n:
            tree[k] += x
            k += k & -k

    def pref(i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & -i
        return s
    for _ in range(60_000):
        if rng.random() < 0.5:
            i, v = rng.randrange(n), rng.randint(-1000, 1000)
            ops.append(("update", i, v))
            d, vals[i], k = v - vals[i], v, i + 1
            while k <= n:
                tree[k] += d
                k += k & -k
            out.append(None)
        else:
            l = rng.randrange(n)
            r = rng.randint(l, n - 1)
            ops.append(("sum_range", l, r))
            out.append(pref(r + 1) - pref(l))
    return ops, out


def _cases(seed, count, n, m):
    import random
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        calls, nums, ops = _random(rng, n, m)
        out.append((calls, _sim(nums, ops)))
    return out


_BIG = _big()

TEACHES = ["fenwick.update"]
USES = ["fenwick.prefix"]

STEPS = [
    {
        "title": "Make it work",
        "text": "Store the list. update assigns, and sum_range adds up the slice. That's correct and fine for small inputs.",
        "hint": "sum(self.nums[l:r + 1])",
        "tests": [([("NumArray", [1, 3, 5]), ("sum_range", 0, 2), ("update", 1, 2), ("sum_range", 0, 2)], [None, 9, None, 8])]
                 + _cases(203, 3, 8, 12),
    },
    {
        "title": "Edges",
        "text": "One element, ranges of length 1, negative values, the same index updated many times.",
        "hint": "Nothing new to write if step 1 is right. These guard the next step's rewrite.",
        "tests": [([("NumArray", [-4]), ("sum_range", 0, 0), ("update", 0, 9), ("update", 0, -2), ("sum_range", 0, 0)],
                   [None, -4, None, None, -2])] + _cases(204, 3, 3, 15),
    },
    {
        "title": "Make it fast: a Fenwick tree",
        "text": "100,000 numbers and 60,000 mixed operations: summing slices is O(n) per query, billions of steps "
                "in total. Store a Fenwick tree instead. update adds the DIFFERENCE (val - old) along i, i + lowbit(i), … "
                "and sum_range(l, r) = prefix(r + 1) - prefix(l). Both are O(log n).",
        "hint": "Keep the raw values in a list, so update knows the old value. Fenwick indexes are 1-based: element i "
                "lives at index i + 1. Build by calling add for each element (O(n log n) is fine).",
        "tests": [_BIG],
    },
]
