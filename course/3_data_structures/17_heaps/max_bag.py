"""
Max With Removals                                                             [easy]

Keep a bag of numbers (repeats allowed):

    add(x)      put x in the bag
    remove(x)   take one copy of x out (x is always in the bag)
    max()       the largest number in the bag, or None if it's empty

Example:
    b = MaxBag()
    b.add(5); b.add(9); b.add(9)
    b.max()       ->  9
    b.remove(9)
    b.max()       ->  9       one 9 is still there
    b.remove(9)
    b.max()       ->  5

Aim for:  O(log n) per call. The big tests make up to 390,000 calls on a bag of up to
          150,000 numbers: max() over a list, a sorted list, or rescanning for a new max
          each time the max is removed is O(n) per call and times out.
Hint:     A heap can't delete from the middle, so don't. Keep a max-heap (push -x)
          and a Counter of numbers waiting to be removed: remove(x) just counts x.
          In max(), pop the top while it's waiting to be removed (counting it off),
          then read the top.
"""


class MaxBag:
    def __init__(self):
        raise NotImplementedError

    def add(self, x: int) -> None:
        raise NotImplementedError

    def remove(self, x: int) -> None:
        raise NotImplementedError

    def max(self) -> int | None:
        raise NotImplementedError


CLASS = "MaxBag"


def _big():
    import heapq
    import random
    from collections import Counter
    rng = random.Random(1705)
    heap, gone, present = [], Counter(), []
    ops, res = [("MaxBag",)], [None]

    def top():
        while heap and gone[-heap[0]]:
            gone[-heap[0]] -= 1
            heapq.heappop(heap)
        return -heap[0] if heap else None

    for step in range(300_000):
        r = rng.random()
        if step < 150_000 or r < 1 / 3 or not present:
            x = rng.randint(-10**6, 10**6)
            heapq.heappush(heap, -x)
            present.append(x)
            ops.append(("add", x))
            res.append(None)
        elif r < 2 / 3:
            i = rng.randrange(len(present))
            present[i], present[-1] = present[-1], present[i]
            x = present.pop()
            gone[x] += 1
            ops.append(("remove", x))
            res.append(None)
        else:
            ops.append(("max",))
            res.append(top())
    return ops, res


def _falling():
    import random
    values = list(range(150_000))
    random.Random(1706).shuffle(values)
    ops, res = [("MaxBag",)] + [("add", x) for x in values], [None] * 150_001
    for top in range(149_999, 29_999, -1):      # remove the max, then ask for the new one
        ops += [("remove", top), ("max",)]
        res += [None, top - 1]
    return ops, res


TEACHES = ["heap.lazy_delete"]
USES = ["heap.max_negate"]

TESTS = [
    ([("MaxBag",), ("add", 5), ("add", 9), ("add", 9), ("max",), ("remove", 9), ("max",), ("remove", 9), ("max",)],
     [None, None, None, None, 9, None, 9, None, 5]),
    ([("MaxBag",), ("max",), ("add", -3), ("max",), ("remove", -3), ("max",)], [None, None, None, -3, None, None]),
    ([("MaxBag",), ("add", 1), ("add", 7), ("add", 4), ("remove", 4), ("max",), ("remove", 7), ("max",), ("add", 2),
      ("max",)],
     [None, None, None, None, None, 7, None, 1, None, 2]),
    _big(),
    _falling(),
]
