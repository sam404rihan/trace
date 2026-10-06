"""
Detect Squares                                                                [medium]

Points on a grid arrive one at a time (duplicates allowed). Build a class:

    add(point)     store the point [x, y]
    count(point)   how many ways can you pick 3 stored points that, together with
                   `point`, form a square with sides parallel to the axes and
                   positive area? Duplicate stored points count as different picks.

Example:
    ds = DetectSquares()
    ds.add([3, 10]); ds.add([11, 2]); ds.add([3, 2])
    ds.count([11, 10])  ->  1
    ds.count([14, 8])   ->  0
    ds.add([11, 2])
    ds.count([11, 10])  ->  2        two copies of [11, 2]

Aim for:  count() looping over stored points that could be the opposite corner, not over triples.
Hint:     The opposite corner (x2, y2) must have |x2 - x| == |y2 - y| > 0. Then the other two corners
          are fixed: (x, y2) and (x2, y). Multiply their counts. Keep a Counter of points.
"""


class DetectSquares:
    def __init__(self):
        raise NotImplementedError

    def add(self, point: list[int]) -> None:
        raise NotImplementedError

    def count(self, point: list[int]) -> int:
        raise NotImplementedError


CLASS = "DetectSquares"


def _sim(ops):
    pts, out = [], [None]
    for op in ops[1:]:
        if op[0] == "add":
            pts.append(tuple(op[1]))
            out.append(None)
        else:
            qx, qy = op[1]
            total = 0
            for (px, py) in pts:
                if abs(px - qx) == abs(py - qy) != 0:
                    total += pts.count((qx, py)) * pts.count((px, qy))
            out.append(total)
    return out


def _cases():
    import random
    rng = random.Random(46)
    out = []
    for _ in range(4):
        ops = [("DetectSquares",)]
        for _ in range(40):
            p = [rng.randint(0, 6), rng.randint(0, 6)]
            ops.append(("add", p) if rng.random() < 0.7 else ("count", p))
        out.append((ops, _sim(ops)))
    return out


TESTS = [
    ([("DetectSquares",), ("add", [3, 10]), ("add", [11, 2]), ("add", [3, 2]), ("count", [11, 10]),
      ("count", [14, 8]), ("add", [11, 2]), ("count", [11, 10])],
     [None, None, None, None, 1, 0, None, 2]),
    ([("DetectSquares",), ("count", [0, 0]), ("add", [0, 0]), ("add", [0, 0]), ("count", [0, 0])],
     [None, 0, None, None, 0]),
] + _cases()
