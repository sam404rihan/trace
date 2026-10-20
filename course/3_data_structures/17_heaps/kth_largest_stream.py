"""
Kth Largest Element in a Stream                                                 [easy]

Build a class that is given k and some starting numbers. Each add(val) adds a
number and returns the kth largest number seen so far. You can assume at least
k numbers exist whenever add returns.

Example:
    kl = KthLargest(3, [4, 5, 8, 2])
    kl.add(3)   ->  4
    kl.add(5)   ->  5
    kl.add(10)  ->  5

Aim for:  O(log k) per add.
Hint:     Keep a min-heap of the k largest. Its top is the kth largest. After each push, pop if it
          holds more than k.
"""


class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        raise NotImplementedError

    def add(self, val: int) -> int:
        raise NotImplementedError


CLASS = "KthLargest"


def _cases():
    import random
    rng = random.Random(71)
    out = []
    for size in (30, 100_000):
        k = rng.randint(1, 8)
        start = [rng.randint(-100, 100) for _ in range(k)]
        ops, seen, res = [("KthLargest", k, start)], list(start), [None]
        import bisect as _b
        seen.sort()
        for _ in range(size):
            v = rng.randint(-10**6, 10**6)
            ops.append(("add", v))
            _b.insort(seen, v)
            res.append(seen[-k])
        out.append((ops, res))
    return out


USES = ["heap.top_k"]

TESTS = [([("KthLargest", 3, [4, 5, 8, 2]), ("add", 3), ("add", 5), ("add", 10), ("add", 9), ("add", 4)],
          [None, 4, 5, 5, 8, 8]),
         ([("KthLargest", 1, []), ("add", -3), ("add", -2), ("add", -4)], [None, -3, -2, -2])] + _cases()
