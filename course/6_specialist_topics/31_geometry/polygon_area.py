"""
Polygon Area                                                                    [easy]

points are the corners of a simple polygon (its edges don't cross), listed in order
around it, clockwise or counterclockwise. Return its area as a float.

Example:
    polygon_area([(0, 0), (4, 0), (4, 3), (0, 3)])  ->  12.0
    polygon_area([(0, 0), (2, 0), (0, 1)])          ->  1.0
    polygon_area([(0, 0), (0, 3), (3, 3), (3, 0), (2, 0), (2, 2), (1, 2), (1, 0)])  ->  7.0   a U shape

Aim for:  O(n).
Hint:     The shoelace formula: sum x[i]·y[i+1] - x[i+1]·y[i] over every edge (wrapping around to
          the first point), then take abs(total) / 2. Each term is the signed area of the
          triangle from the origin to that edge, and the parts outside the polygon cancel.
"""


def polygon_area(points: list[tuple[int, int]]) -> float:
    raise NotImplementedError  # replace this line with your solution


def _ref(pts):
    s = 0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2


def _star(seed, n):
    import math
    import random
    rng = random.Random(seed)
    pts = []
    for k in range(n):
        ang = 2 * math.pi * k / n
        r = rng.randint(10**6, 10**7) if n > 1000 else rng.randint(500, 1000)
        pts.append((round(r * math.cos(ang)), round(r * math.sin(ang))))
    return pts


TEACHES = ["geo.shoelace"]
USES = ["geo.cross"]

TESTS = [(([(0, 0), (4, 0), (4, 3), (0, 3)],), 12.0), (([(0, 0), (2, 0), (0, 1)],), 1.0),
         (([(0, 0), (0, 3), (3, 3), (3, 0), (2, 0), (2, 2), (1, 2), (1, 0)],), 7.0),
         (([(0, 0), (0, 3), (4, 3), (4, 0)],), 12.0), (([(-1, -1), (1, -1), (0, 2)],), 3.0),
         (([(0, 0), (1, 0), (1, 1)],), 0.5)] \
    + [((p,), _ref(p)) for p in (_star(3105, 12), _star(3106, 200), _star(3107, 100_000))]
