"""
Convex Hull                                                                   [guided]

Given points (x, y) with integer coordinates, return the corners of the smallest
convex polygon containing them all, in counterclockwise order. Any corner may come
first.

  - Only corners: a point in the middle of a hull edge is not included.
  - Points may repeat. If every point is the same, return just that point.
  - If all points are on one line, return its two end points.

Example:
    convex_hull([(0, 0), (4, 0), (4, 3), (0, 3), (2, 1), (2, 3)])
        ->  [(0, 0), (4, 0), (4, 3), (0, 3)]          (2, 1) is inside, (2, 3) is on an edge
"""


def convex_hull(points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected):
    """Any rotation of the expected corner list, as tuples or lists."""
    try:
        got = [tuple(p) for p in got]
    except TypeError:
        return False
    if len(got) != len(expected):
        return False
    if not expected:
        return True
    try:
        k = got.index(tuple(expected[0]))
    except ValueError:
        return False
    return got[k:] + got[:k] == [tuple(p) for p in expected]


def _hull(points):
    pts = sorted(set(map(tuple, points)))
    if len(pts) <= 2:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _random(seed, count, n, span):
    import random
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        pts = [(rng.randint(-span, span), rng.randint(-span, span)) for _ in range(rng.randint(3, n))]
        out.append(((pts,), _hull(pts)))
    return out


def _bowl():
    """20,001 points on the parabola y = x², all of them corners, hidden among 20,000 points above it."""
    import random
    rng = random.Random(3102)
    a = 10_000
    rim = [(x, x * x) for x in range(-a, a + 1)]
    inner = []
    while len(inner) < 20_000:
        x = rng.randint(-a + 1, a - 1)
        inner.append((x, rng.randint(x * x + 1, a * a - 1)))
    pts = rim + inner
    rng.shuffle(pts)
    return ((pts,), rim)                       # left to right along the bottom is counterclockwise


TEACHES = ["geo.hull"]
USES = ["geo.cross"]

STEPS = [
    {
        "title": "Make it work",
        "text": "Gift wrapping (Jarvis march): start at the lowest-then-leftmost point, which must be a corner. From the "
                "current corner, pick the next point so that every other point is on its left, i.e. never make a right "
                "turn. Repeat until you are back at the start.",
        "hint": "cross(o, a, b) = (a.x - o.x)(b.y - o.y) - (a.y - o.y)(b.x - o.x). From corner c, start with any "
                "candidate q != c. For each point r: if cross(c, q, r) < 0 (r is to the right), r becomes q. If it is 0, "
                "keep whichever of q and r is FARTHER from c, so collinear middle points are skipped.",
        "tests": [((([(0, 0), (4, 0), (4, 3), (0, 3), (2, 1), (2, 3)]),), [(0, 0), (4, 0), (4, 3), (0, 3)]),
                  (([(0, 0), (1, 1), (2, 0), (1, -1)],), [(1, -1), (2, 0), (1, 1), (0, 0)])] + _random(3103, 6, 30, 20),
    },
    {
        "title": "Edges",
        "text": "Repeated points, all points identical, every point on one line, exactly three points, and points "
                "lying in the middle of hull edges.",
        "hint": "Deduplicate first (set). With 1 distinct point return it, and with all collinear return the two "
                "extremes. Ties in the 'farther' rule are what keep edge midpoints out.",
        "tests": [(([(5, 5), (5, 5), (5, 5)],), [(5, 5)]), (([(0, 0), (2, 2), (1, 1), (3, 3), (2, 2)],), [(0, 0), (3, 3)]),
                  (([(0, 0), (3, 0), (0, 3)],), [(0, 0), (3, 0), (0, 3)]),
                  (([(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (0, 1), (1, 1)],), [(0, 0), (2, 0), (2, 2), (0, 2)]),
                  (([(1, 1), (1, 1), (4, 1)],), [(1, 1), (4, 1)])] + _random(3104, 4, 12, 2),
    },
    {
        "title": "Make it fast: monotone chain",
        "text": "40,000 points, and half of them are corners. Gift wrapping costs O(n) per corner: 20,000 × 40,000 steps. "
                "Andrew's monotone chain sorts once, then sweeps left to right building the lower hull, and right to left "
                "for the upper one. Each point is pushed and popped at most once, so after the sort it is O(n).",
        "hint": "pts = sorted(set(points)). For each p: while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0: "
                "lower.pop(); then lower.append(p). Same over reversed(pts) for upper. "
                "Answer: lower[:-1] + upper[:-1] (each chain ends where the other starts).",
        "tests": [_bowl()],
    },
]
