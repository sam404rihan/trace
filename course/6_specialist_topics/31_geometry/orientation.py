"""
Which way does it turn?                                                      [snippet]

Walking from point p to q and then on to r, do you turn left, turn right, or keep
going straight? Return 1 for a left (counterclockwise) turn, -1 for a right
(clockwise) turn, and 0 if the three points are on one line.

Points are (x, y) pairs of integers.

Example:
    orientation((0, 0), (4, 0), (4, 3))  ->  1       left turn
    orientation((0, 0), (4, 0), (4, -3)) ->  -1
    orientation((0, 0), (1, 1), (5, 5))  ->  0

Hint:     cross = (q.x - p.x)·(r.y - p.y) - (q.y - p.y)·(r.x - p.x), then return its sign.
          Pure integer arithmetic, so it is exact. No angles needed.
"""


def orientation(p: tuple[int, int], q: tuple[int, int], r: tuple[int, int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _cases():
    import random
    rng = random.Random(3101)
    out = []
    for _ in range(10):
        p, q, r = [(rng.randint(-5, 5), rng.randint(-5, 5)) for _ in range(3)]
        c = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        out.append(((p, q, r), (c > 0) - (c < 0)))
    return out


TESTS = [(((0, 0), (4, 0), (4, 3)), 1), (((0, 0), (4, 0), (4, -3)), -1), (((0, 0), (1, 1), (5, 5)), 0),
         (((2, 2), (2, 2), (7, 1)), 0), (((10**9, 0), (0, 10**9), (-10**9, 0)), 1),
         (((0, 0), (10**9, 1), (10**9 - 1, 1)), 1)] + _cases()
