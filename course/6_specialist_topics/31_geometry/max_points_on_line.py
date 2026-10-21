"""
Max Points on a Line                                                            [hard]

Given distinct points with integer coordinates, return the largest number of them
that lie on one straight line.

Example:
    max_points_on_line([(1, 1), (2, 2), (3, 3)])  ->  3
    max_points_on_line([(1, 1), (3, 2), (5, 3), (4, 1), (2, 3), (1, 4)])  ->  4

Aim for:  O(n²). The last test has 600 points.
Hint:     Fix an anchor point and group every other point by the direction from the anchor.
          Store the direction exactly, not as a float: (dx, dy) divided by gcd(|dx|, |dy|), with
          the sign fixed so (dx, dy) and (-dx, -dy) match (e.g. make dx > 0, or dx == 0 and dy > 0).
          The biggest group + 1 (the anchor) is the best line through that anchor.
"""


def max_points_on_line(points: list[tuple[int, int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(pts):
    from math import gcd
    if len(pts) <= 2:
        return len(pts)
    best = 0
    for i, (x1, y1) in enumerate(pts):
        seen = {}
        for x2, y2 in pts[i + 1:]:
            dx, dy = x2 - x1, y2 - y1
            g = gcd(dx, dy)
            dx, dy = dx // g, dy // g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            seen[(dx, dy)] = seen.get((dx, dy), 0) + 1
        if seen:
            best = max(best, max(seen.values()) + 1)
    return best


def _random(seed, n, span, planted):
    import random
    rng = random.Random(seed)
    pts = set()
    x0, y0, dx, dy = rng.randint(-50, 50), rng.randint(-50, 50), rng.choice([1, 2, 3, 7]), rng.choice([-5, -1, 2, 3])
    for k in range(planted):
        pts.add((x0 + k * dx, y0 + k * dy))
    while len(pts) < n:
        pts.add((rng.randint(-span, span), rng.randint(-span, span)))
    pts = list(pts)
    rng.shuffle(pts)
    return pts


_SMALL = [_random(3110 + k, 25, 6, 4) for k in range(5)]
_BIG = _random(3120, 600, 100_000, 31)

USES = ["hash.group_key"]

TESTS = [(([(1, 1), (2, 2), (3, 3)],), 3), (([(1, 1), (3, 2), (5, 3), (4, 1), (2, 3), (1, 4)],), 4),
         (([(0, 0)],), 1), (([(0, 0), (5, 9)],), 2), (([(0, 0), (0, 1), (0, 2), (1, 5)],), 3),
         (([(0, 0), (1, 1), (2, 0), (3, -1), (4, 4)],), 3), (([(0, 0), (94_911_151, 94_911_150), (94_911_152, 94_911_151)],), 2)] \
    + [((p,), _ref(p)) for p in _SMALL] + [((_BIG,), 31)]
