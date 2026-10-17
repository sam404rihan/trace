"""
Data Stream as Disjoint Intervals                                             [hard]

Non-negative integers arrive one at a time (repeats allowed). Build a class:

    add_num(value)      record value
    get_intervals()     the numbers seen so far as a sorted list of disjoint
                        [start, end] intervals (both ends included), with
                        neighbouring runs merged: 1, 2, 3 becomes [[1, 3]].
                        Return new lists, not ones you'll keep changing.

Example:
    sr = SummaryRanges()
    sr.add_num(1);  sr.get_intervals()   ->  [[1, 1]]
    sr.add_num(3);  sr.get_intervals()   ->  [[1, 1], [3, 3]]
    sr.add_num(7);  sr.get_intervals()   ->  [[1, 1], [3, 3], [7, 7]]
    sr.add_num(2);  sr.get_intervals()   ->  [[1, 3], [7, 7]]
    sr.add_num(6);  sr.get_intervals()   ->  [[1, 3], [6, 7]]

Aim for:  add_num in O(log n) to find the spot (plus list shifting), get_intervals in O(intervals),
          rather than re-sorting every number seen on each call.
Hint:     Keep the intervals in a sorted list. For a new value, bisect for the interval just
          before it. The cases: already inside one; it extends the one on the left; it extends
          the one on the right; it bridges both (merge them); or it's a new [value, value].
"""


class SummaryRanges:
    def __init__(self):
        raise NotImplementedError

    def add_num(self, value: int) -> None:
        raise NotImplementedError

    def get_intervals(self) -> list[list[int]]:
        raise NotImplementedError


CLASS = "SummaryRanges"


def _intervals(seen):
    out = []
    for v in sorted(seen):
        if out and out[-1][1] + 1 == v:
            out[-1][1] = v
        else:
            out.append([v, v])
    return out


def _sim(ops):
    seen, res = set(), [None]
    for op in ops[1:]:
        if op[0] == "add_num":
            seen.add(op[1])
            res.append(None)
        else:
            res.append(_intervals(seen))
    return res


def _cases():
    import random
    rng = random.Random(352)
    out = []
    for _ in range(6):
        ops = [("SummaryRanges",)]
        for _ in range(30):
            ops.append(("add_num", rng.randint(0, 25)) if rng.random() < 0.7 else ("get_intervals",))
        out.append((ops, _sim(ops)))
    return out


USES = ["bsearch.first_true", "intervals.merge"]

TESTS = [
    ([("SummaryRanges",), ("add_num", 1), ("get_intervals",), ("add_num", 3), ("get_intervals",), ("add_num", 7),
      ("get_intervals",), ("add_num", 2), ("get_intervals",), ("add_num", 6), ("get_intervals",)],
     [None, None, [[1, 1]], None, [[1, 1], [3, 3]], None, [[1, 1], [3, 3], [7, 7]], None, [[1, 3], [7, 7]], None,
      [[1, 3], [6, 7]]]),
    ([("SummaryRanges",), ("get_intervals",), ("add_num", 5), ("add_num", 5), ("add_num", 4), ("add_num", 6),
      ("get_intervals",)],
     [None, [], None, None, None, None, [[4, 6]]]),
] + _cases()
