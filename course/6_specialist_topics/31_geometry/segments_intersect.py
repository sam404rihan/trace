"""
Do the segments touch?                                                        [medium]

Segment one runs from a to b, segment two from c to d (integer (x, y) points; a
segment may be a single point when its ends are equal). Return True if they share
at least one point. Touching at an end and overlapping along a line both count.

Example:
    segments_intersect((0, 0), (4, 4), (0, 4), (4, 0))  ->  True       an X
    segments_intersect((0, 0), (2, 2), (3, 3), (5, 5))  ->  False      same line, a gap
    segments_intersect((0, 0), (2, 0), (2, 0), (2, 5))  ->  True       touching at (2, 0)
    segments_intersect((0, 0), (4, 0), (1, 1), (3, 1))  ->  False      parallel

Aim for:  O(1), integers only.
Hint:     With o(p, q, r) = the sign of the cross product: the general case is
          o(a,b,c) != o(a,b,d) and o(c,d,a) != o(c,d,b). Then four special cases: if o(a,b,c) == 0
          and c lies within the bounding box of a and b, they touch; the same for d, a and b.
"""


def segments_intersect(a: tuple[int, int], b: tuple[int, int], c: tuple[int, int], d: tuple[int, int]) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _o(p, q, r):
    v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (v > 0) - (v < 0)


def _on(p, q, r):
    return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])


def _ref(a, b, c, d):
    o1, o2, o3, o4 = _o(a, b, c), _o(a, b, d), _o(c, d, a), _o(c, d, b)
    if o1 != o2 and o3 != o4:
        return True
    return ((o1 == 0 and _on(a, b, c)) or (o2 == 0 and _on(a, b, d))
            or (o3 == 0 and _on(c, d, a)) or (o4 == 0 and _on(c, d, b)))


def _cases():
    import random
    rng = random.Random(3108)
    out = []
    for span, count in ((3, 40), (1000, 10)):
        for _ in range(count):
            pts = [(rng.randint(0, span), rng.randint(0, span)) for _ in range(4)]
            out.append((tuple(pts), _ref(*pts)))
    return out


USES = ["geo.cross"]

TESTS = [(((0, 0), (4, 4), (0, 4), (4, 0)), True), (((0, 0), (2, 2), (3, 3), (5, 5)), False),
         (((0, 0), (2, 0), (2, 0), (2, 5)), True), (((0, 0), (4, 0), (1, 1), (3, 1)), False),
         (((0, 0), (4, 0), (1, 0), (2, 0)), True), (((1, 1), (1, 1), (0, 0), (2, 2)), True),
         (((1, 1), (1, 1), (1, 1), (1, 1)), True), (((1, 1), (1, 1), (2, 2), (2, 2)), False),
         (((0, 0), (2, 2), (1, 1), (5, 0)), True), (((0, 0), (3, 3), (4, 4), (3, 3)), True),
         (((0, 0), (10, 1), (5, 0), (5, 0)), False)] + _cases()
