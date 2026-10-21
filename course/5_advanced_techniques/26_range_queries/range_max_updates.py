"""
Range Max With Updates                                                        [easy]

Build a class over a list of numbers:

    MaxArray(nums)
    update(i, val)       set nums[i] = val
    max_range(l, r)      the largest of nums[l..r], both ends included

Example:
    m = MaxArray([2, 7, 1, 8, 3])
    m.max_range(0, 2)   ->  7
    m.update(1, 0)
    m.max_range(0, 2)   ->  2
    m.max_range(1, 4)   ->  8

Aim for:  O(log n) for both. The last test makes 60,000 calls on 50,000 numbers:
          max() over the range is O(n) per call and times out.
Hint:     A segment tree. Put the numbers in the leaves tree[size .. size + n - 1] of a
          list of length 2 * size, and give every node i the max of its children 2i and
          2i + 1. update: set the leaf, then walk up (i //= 2) recomputing each parent.
          max_range: start lo and hi at the two leaves and climb, taking any node that
          sticks out of the range on its side.
"""


class MaxArray:
    def __init__(self, nums: list[int]):
        raise NotImplementedError

    def update(self, i: int, val: int) -> None:
        raise NotImplementedError

    def max_range(self, l: int, r: int) -> int:
        raise NotImplementedError


CLASS = "MaxArray"


def _big():
    import random
    rng = random.Random(2602)
    n = 50_000
    nums = [rng.randint(0, 10**9) for _ in range(n)]
    size = 1
    while size < n:
        size *= 2
    tree = [0] * (2 * size)
    tree[size:size + n] = nums
    for i in range(size - 1, 0, -1):
        tree[i] = max(tree[2 * i], tree[2 * i + 1])
    ops, res = [("MaxArray", nums)], [None]
    for _ in range(60_000):
        if rng.random() < 0.5:
            i, v = rng.randrange(n), rng.randint(0, 10**9)
            k = size + i
            tree[k] = v
            k //= 2
            while k:
                tree[k] = max(tree[2 * k], tree[2 * k + 1])
                k //= 2
            ops.append(("update", i, v))
            res.append(None)
        else:
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            lo, hi, best = l + size, r + size + 1, 0
            while lo < hi:
                if lo & 1:
                    best = max(best, tree[lo])
                    lo += 1
                if hi & 1:
                    hi -= 1
                    best = max(best, tree[hi])
                lo //= 2
                hi //= 2
            ops.append(("max_range", l, r))
            res.append(best)
    return ops, res


TEACHES = ["segtree.basic"]
USES = []

TESTS = [
    ([("MaxArray", [2, 7, 1, 8, 3]), ("max_range", 0, 2), ("update", 1, 0), ("max_range", 0, 2), ("max_range", 1, 4)],
     [None, 7, None, 2, 8]),
    ([("MaxArray", [5]), ("max_range", 0, 0), ("update", 0, -3), ("max_range", 0, 0)], [None, 5, None, -3]),
    ([("MaxArray", [-1, -2, -3]), ("max_range", 1, 2), ("update", 2, 9), ("max_range", 0, 1), ("max_range", 0, 2)],
     [None, -2, None, -1, 9]),
    ([("MaxArray", [4, 4, 4, 4, 4, 4]), ("update", 3, 1), ("max_range", 3, 3), ("max_range", 2, 5)],
     [None, None, 1, 4]),
    _big(),
]
