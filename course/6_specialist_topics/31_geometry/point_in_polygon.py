"""
Inside, Outside, or On the Fence                                              [medium]

polygon lists the corners of a simple polygon in order (integer coordinates, either
direction). Return "inside", "outside", or "boundary" for the point.

Example:
    square = [(0, 0), (4, 0), (4, 4), (0, 4)]
    point_in_polygon(square, (2, 2))  ->  "inside"
    point_in_polygon(square, (4, 1))  ->  "boundary"
    point_in_polygon(square, (5, 2))  ->  "outside"

Aim for:  O(n), integers only.
Hint:     First check every edge: the point is on edge (p, q) when cross(p, q, pt) == 0 and it
          lies within the edge's bounding box. Otherwise cast a ray to the right and count edge
          crossings: odd means inside. Count edge (p, q) when (p.y > y) != (q.y > y) (this
          half-open rule handles rays through corners) and the crossing's x is right of the
          point. Compare with cross products instead of computing x with division.
"""


def point_in_polygon(polygon: list[tuple[int, int]], point: tuple[int, int]) -> str:
    raise NotImplementedError  # replace this line with your solution


def _ref(poly, pt):
    x, y = pt
    n = len(poly)
    inside = False
    for i in range(n):
        (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
        if ((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) == 0
                and min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)):
            return "boundary"
        if (y1 > y) != (y2 > y):
            # crossing x > x  <=>  (x2 - x1)(y - y1) / (y2 - y1) + x1 > x, sign-safe
            lhs = (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1)
            if (lhs > 0) == (y2 > y1):
                inside = not inside
    return "inside" if inside else "outside"


def _star(rng, n, r_lo, r_hi):
    import math
    pts = []
    for k in range(n):
        ang = 2 * math.pi * k / n
        r = rng.randint(r_lo, r_hi)
        p = (round(r * math.cos(ang)), round(r * math.sin(ang)))
        if not pts or pts[-1] != p:
            pts.append(p)
    return pts


def _cases():
    import random
    rng = random.Random(3109)
    out = []
    for _ in range(6):
        poly = _star(rng, rng.randint(5, 8), 3, 7)
        for _ in range(6):
            pt = (rng.randint(-7, 7), rng.randint(-7, 7))
            out.append(((poly, pt), _ref(poly, pt)))
    big = _star(rng, 50_000, 10**6, 10**7)
    for pt in ((0, 0), (999_999, 3), big[17], (15_000_000, 0)):
        out.append(((big, pt), _ref(big, pt)))
    return out


_SQ = [(0, 0), (4, 0), (4, 4), (0, 4)]
_U = [(0, 0), (0, 6), (6, 6), (6, 0), (4, 0), (4, 4), (2, 4), (2, 0)]
_DIAMOND = [(2, 0), (4, 2), (2, 4), (0, 2)]

TESTS = [((_SQ, (2, 2)), "inside"), ((_SQ, (4, 1)), "boundary"), ((_SQ, (5, 2)), "outside"), ((_SQ, (0, 0)), "boundary"),
         ((_SQ, (-1, 0)), "outside"), ((_SQ, (6, 4)), "outside"),
         ((_U, (3, 2)), "outside"), ((_U, (1, 2)), "inside"), ((_U, (2, 2)), "boundary"), ((_U, (3, 4)), "boundary"),
         ((_U, (3, 5)), "inside"), ((_U, (-1, 4)), "outside"), ((_U, (5, 0)), "boundary"), ((_U, (3, 0)), "outside"),
         ((_DIAMOND, (2, 2)), "inside"), ((_DIAMOND, (0, 0)), "outside"), ((_DIAMOND, (-3, 2)), "outside"),
         ((_DIAMOND, (3, 1)), "boundary"), ((list(reversed(_DIAMOND)), (2, 3)), "inside")] + _cases()
