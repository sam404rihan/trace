"""
An ordered set, from scratch                                                  [build]

Build a set that keeps its values in order, backed by a binary search tree
that you write yourself (no sorted lists or bisect).

    s = TreeSet()
    s.add(50); s.add(30); s.add(70); s.add(60)
    s.contains(60)    ->  True
    s.floor(65)       ->  60       the biggest value <= 65
    s.ceiling(65)     ->  70       the smallest value >= 65
    s.floor(10)       ->  None
    s.to_list()       ->  [30, 50, 60, 70]
    s.size()          ->  4

Rules:
  - add(x) returns True if x was new, False if it was already there.
  - floor / ceiling return None when there's no such value.
  - to_list() returns all values in increasing order.

Aim for:  O(height) for add, contains, floor and ceiling. O(n) for to_list.
Hint:     floor(x): walk down from the root. When node.val <= x, it's a candidate.
          Remember it and go right to look for a bigger one. Otherwise go left.
          ceiling is the mirror image.
"""


class TreeSet:
    def __init__(self):
        raise NotImplementedError

    def add(self, x: int) -> bool:
        raise NotImplementedError

    def contains(self, x: int) -> bool:
        raise NotImplementedError

    def floor(self, x: int) -> int | None:
        raise NotImplementedError

    def ceiling(self, x: int) -> int | None:
        raise NotImplementedError

    def to_list(self) -> list[int]:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError


CLASS = "TreeSet"


def _big():
    import bisect
    import random
    rng = random.Random(18)
    calls, out, ref = [("TreeSet",)], [None], []
    for _ in range(20_000):
        x = rng.randint(0, 1_000_000)
        calls.append(("add", x))
        i = bisect.bisect_left(ref, x)
        new = i == len(ref) or ref[i] != x
        if new:
            ref.insert(i, x)
        out.append(new)
    for _ in range(20_000):
        x = rng.randint(-10, 1_000_010)
        if rng.random() < 0.5:
            calls.append(("floor", x))
            i = bisect.bisect_right(ref, x)
            out.append(ref[i - 1] if i else None)
        else:
            calls.append(("ceiling", x))
            i = bisect.bisect_left(ref, x)
            out.append(ref[i] if i < len(ref) else None)
    calls.append(("size",))
    out.append(len(ref))
    return calls, out


_CALLS, _OUT = _big()

TESTS = [
    ([("TreeSet",), ("add", 50), ("add", 30), ("add", 70), ("add", 60), ("contains", 60), ("floor", 65),
      ("ceiling", 65), ("floor", 10), ("to_list",), ("size",)],
     [None, True, True, True, True, True, 60, 70, None, [30, 50, 60, 70], 4]),
    ([("TreeSet",), ("add", 5), ("add", 5), ("size",), ("contains", 4), ("ceiling", 6), ("floor", 5), ("ceiling", 5)],
     [None, True, False, 1, False, None, 5, 5]),
    ([("TreeSet",), ("to_list",), ("floor", 0), ("size",)], [None, [], None, 0]),
    ([("TreeSet",), ("add", 1), ("add", 2), ("add", 3), ("add", 4), ("floor", 100), ("ceiling", -100), ("to_list",)],
     [None, True, True, True, True, 4, 1, [1, 2, 3, 4]]),
    (_CALLS, _OUT),
]
