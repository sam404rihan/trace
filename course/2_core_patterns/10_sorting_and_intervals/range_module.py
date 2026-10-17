"""
Range Module                                                                  [hard]

Track which numbers are covered, using half-open ranges [left, right) (left is
included, right is not). Build a class:

    add_range(left, right)     cover every number in [left, right)
    remove_range(left, right)  uncover every number in [left, right)
    query_range(left, right)   True if EVERY number in [left, right) is covered

Example:
    rm = RangeModule()
    rm.add_range(10, 20)
    rm.remove_range(14, 16)
    rm.query_range(10, 14)   ->  True
    rm.query_range(13, 15)   ->  False      14 was removed
    rm.query_range(16, 17)   ->  True

Aim for:  O(log n + intervals touched) per call: a sorted list of disjoint intervals.
Hint:     Store the covered intervals sorted, non-overlapping and non-touching. With bisect, find
          the run of intervals that overlap [left, right). add_range replaces that run with one
          merged interval. remove_range replaces it with the leftover pieces on either side.
          query_range checks that one stored interval contains all of [left, right).
"""


class RangeModule:
    def __init__(self):
        raise NotImplementedError

    def add_range(self, left: int, right: int) -> None:
        raise NotImplementedError

    def remove_range(self, left: int, right: int) -> None:
        raise NotImplementedError

    def query_range(self, left: int, right: int) -> bool:
        raise NotImplementedError


CLASS = "RangeModule"


def _sim(ops):
    covered, out = set(), [None]
    for name, left, right in ops[1:]:
        span = set(range(left, right))
        if name == "add_range":
            covered |= span
            out.append(None)
        elif name == "remove_range":
            covered -= span
            out.append(None)
        else:
            out.append(span <= covered)
    return out


def _cases():
    import random
    rng = random.Random(715)
    out = []
    for _ in range(6):
        ops = [("RangeModule",)]
        for _ in range(40):
            left = rng.randint(0, 30)
            right = left + rng.randint(1, 8)
            ops.append((rng.choice(["add_range", "add_range", "remove_range", "query_range", "query_range"]),
                        left, right))
        out.append((ops, _sim(ops)))
    return out


def _big():
    """5,000 small ranges added, then queried and partly removed. A list of every covered
    number would hold billions of entries."""
    import random
    rng = random.Random(7150)
    ops, expect = [("RangeModule",)], [None]
    starts = sorted(rng.sample(range(0, 10**9, 1000), 5000))
    for s in starts:
        ops.append(("add_range", s, s + 500))
        expect.append(None)
    for s in starts[::2]:
        ops.append(("remove_range", s + 100, s + 200))
        expect.append(None)
    for i, s in enumerate(starts):
        ops.append(("query_range", s, s + 100))
        expect.append(True)
        ops.append(("query_range", s + 150, s + 160))
        expect.append(i % 2 == 1)
    ops.append(("add_range", 0, 10**9 + 1000))
    expect.append(None)
    ops.append(("query_range", 5, 10**9))
    expect.append(True)
    return ops, expect


USES = ["bsearch.first_true", "intervals.overlap", "intervals.merge"]

TESTS = [
    ([("RangeModule",), ("add_range", 10, 20), ("remove_range", 14, 16), ("query_range", 10, 14),
      ("query_range", 13, 15), ("query_range", 16, 17)],
     [None, None, None, True, False, True]),
    ([("RangeModule",), ("query_range", 1, 2), ("add_range", 1, 5), ("add_range", 5, 8), ("query_range", 1, 8),
      ("remove_range", 0, 100), ("query_range", 3, 4)],
     [None, False, None, None, True, None, False]),
    ([("RangeModule",), ("add_range", 6, 8), ("remove_range", 7, 8), ("remove_range", 8, 9), ("add_range", 8, 9),
      ("remove_range", 1, 3), ("add_range", 1, 8), ("query_range", 2, 4), ("query_range", 2, 9),
      ("query_range", 4, 6)],
     [None, None, None, None, None, None, None, True, True, True]),
] + _cases() + [_big()]
