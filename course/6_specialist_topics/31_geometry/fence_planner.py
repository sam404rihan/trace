"""
Fence planner                                                                  [build]

A farmer keeps planting posts and wants to know, at any moment, what a fence around
all of them would look like. The fence is the convex hull of the posts.

    f = FencePlanner()
    f.add(0, 0); f.add(4, 0); f.add(4, 3)
    f.area()           ->  6.0
    f.perimeter()      ->  12.0              3 + 4 + 5
    f.add(0, 3)
    f.encloses(2, 1)   ->  True
    f.encloses(4, 2)   ->  True               on the fence counts
    f.encloses(5, 1)   ->  False

Rules:
  - add(x, y) plants a post (integers; the same spot may be planted twice).
  - area() and perimeter() describe the hull, as floats. With fewer than 3 corners the area
    is 0.0, and the perimeter of a hull that is a segment is twice its length (the fence goes
    out and back). One post, or none, gives 0.0 for both.
  - encloses(x, y) is True when the point is inside the fence or on it.

Aim for:  the last test plants 20,000 posts, then makes 3,000 rounds of "plant one more post,
          then ask a question". Recomputing the hull on every question is too slow.
Hint:     Cache the hull. A new post that the current fence already encloses can't change it,
          so only rebuild (monotone chain) when a post lands outside. encloses on a convex polygon
          is just "no right turn along any edge": cross(p[i], p[i+1], pt) >= 0 for all edges of a
          counterclockwise hull.
"""


class FencePlanner:
    def __init__(self):
        raise NotImplementedError

    def add(self, x: int, y: int) -> None:
        raise NotImplementedError

    def area(self) -> float:
        raise NotImplementedError

    def perimeter(self) -> float:
        raise NotImplementedError

    def encloses(self, x: int, y: int) -> bool:
        raise NotImplementedError


CLASS = "FencePlanner"


def FINISH(value):
    return round(value, 6) if isinstance(value, float) else value


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def _hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _answer(h, op, args):
    import math
    if op == "area":
        if len(h) < 3:
            return 0.0
        return round(abs(sum(_cross((0, 0), h[i], h[(i + 1) % len(h)]) for i in range(len(h)))) / 2, 6)
    if op == "perimeter":
        if len(h) < 2:
            return 0.0
        return round(sum(math.dist(h[i], h[(i + 1) % len(h)]) for i in range(len(h))), 6)
    pt = tuple(args)
    if not h:
        return False
    if len(h) == 1:
        return h[0] == pt
    if len(h) == 2:
        a, b = h
        return (_cross(a, b, pt) == 0 and min(a[0], b[0]) <= pt[0] <= max(a[0], b[0])
                and min(a[1], b[1]) <= pt[1] <= max(a[1], b[1]))
    return all(_cross(h[i], h[(i + 1) % len(h)], pt) >= 0 for i in range(len(h)))


def _sim(ops):
    pts, out, h, dirty = [], [None], [], False
    for op, *args in ops:
        if op == "add":
            pts.append(tuple(args)); out.append(None); dirty = True
            continue
        if dirty:
            h, dirty = _hull(pts), False
        out.append(_answer(h, op, args))
    return out


def _random_ops(rng, n, span):
    ops = []
    for _ in range(n):
        r = rng.random()
        if r < 0.45:
            ops.append(("add", rng.randint(-span, span), rng.randint(-span, span)))
        elif r < 0.6:
            ops.append(("area",))
        elif r < 0.75:
            ops.append(("perimeter",))
        else:
            ops.append(("encloses", rng.randint(-span - 1, span + 1), rng.randint(-span - 1, span + 1)))
    return ops


def _big():
    import math
    import random
    rng = random.Random(3130)
    ops = []
    for _ in range(20_000):
        a, r = rng.random() * 2 * math.pi, 1_000_000 * math.sqrt(rng.random())
        ops.append(("add", round(r * math.cos(a)), round(r * math.sin(a))))
    pts = [op[1:] for op in ops]
    h = _hull(pts)
    out = [None] * (len(ops) + 1)
    for _ in range(3_000):
        a, r = rng.random() * 2 * math.pi, 900_000 * math.sqrt(rng.random())   # well inside the existing fence
        ops.append(("add", round(r * math.cos(a)), round(r * math.sin(a))))
        out.append(None)
        pts.append(ops[-1][1:])
        if not _answer(h, "encloses", ops[-1][1:]):
            h = _hull(pts)
        q = rng.choice(["area", "perimeter", "encloses"])
        if q == "encloses":
            ops.append(("encloses", rng.randint(-1_100_000, 1_100_000), rng.randint(-1_100_000, 1_100_000)))
        else:
            ops.append((q,))
        out.append(_answer(h, ops[-1][0], ops[-1][1:]))
    return [("FencePlanner",)] + ops, out


def _cases():
    import random
    rng = random.Random(3131)
    out = []
    for span in (1, 2, 3, 6, 6, 40):
        ops = _random_ops(rng, 60, span)
        out.append(([("FencePlanner",)] + ops, _sim(ops)))
    return out


USES = ["geo.cross", "geo.hull", "geo.shoelace"]

TESTS = [([("FencePlanner",), ("add", 0, 0), ("add", 4, 0), ("add", 4, 3), ("area",), ("perimeter",), ("add", 0, 3),
           ("encloses", 2, 1), ("encloses", 4, 2), ("encloses", 5, 1)], [None, None, None, None, 6.0, 12.0, None, True, True, False]),
         ([("FencePlanner",), ("area",), ("perimeter",), ("encloses", 0, 0), ("add", 2, 2), ("perimeter",), ("encloses", 2, 2),
           ("add", 2, 2), ("add", 5, 6), ("area",), ("perimeter",), ("encloses", 5, 6), ("encloses", 8, 10)],
          [None, 0.0, 0.0, False, None, 0.0, True, None, None, 0.0, 10.0, True, False])] + _cases() + [_big()]
