"""
Closest Pair of Points                                                        [hard]

Return the SQUARED distance between the two closest points in `points` (a list
of [x, y] with integer coordinates; at least 2 points, repeats allowed).
Squared, so the answer stays an integer.

Example:
    closest_pair([[0, 0], [5, 5], [1, 1], [9, 0]])   ->  2      (0, 0) and (1, 1)
    closest_pair([[3, 3], [3, 3]])                   ->  0

Aim for:  O(n log n). All pairs is O(n²): too slow for 20,000 points.
Hint:     Sort by x and sweep left to right, keeping the points within the best distance d so far
          to the left of the current one, ordered by y (a sorted list of (y, x) with bisect).
          For the new point, only the stored points with y in [y - d, y + d] can beat d: there
          are O(1) of them. Drop points from the left once x - their x > d.
          (The classic divide and conquer also works.)
"""


def closest_pair(points: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(points):
    return min((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2
               for i in range(len(points)) for j in range(i + 1, len(points)))


def _sweep(points):
    import bisect
    from math import isqrt
    pts = sorted(map(tuple, points))
    best, window, left = float("inf"), [], 0
    for x, y in pts:
        d = isqrt(best) + 1 if best != float("inf") else float("inf")
        while x - pts[left][0] > d:
            px, py = pts[left]
            window.pop(bisect.bisect_left(window, (py, px)))
            left += 1
        lo = bisect.bisect_left(window, (y - d, float("-inf")))
        hi = bisect.bisect_right(window, (y + d, float("inf")))
        for wy, wx in window[lo:hi]:
            best = min(best, (x - wx) ** 2 + (y - wy) ** 2)
        bisect.insort(window, (y, x))
    return best


def _cases():
    import random
    rng = random.Random(1975)
    out = []
    for _ in range(10):
        pts = [[rng.randint(-20, 20), rng.randint(-20, 20)] for _ in range(rng.randint(2, 15))]
        out.append(((pts,), _brute(pts)))
    pts = [[rng.randint(-10**7, 10**7), rng.randint(-10**7, 10**7)] for _ in range(20_000)]
    out.append(((pts,), _sweep(pts)))
    line = [[i * 1000, (i * 7919) % 1000] for i in range(20_000)]     # all on a thin strip
    out.append(((line,), _sweep(line)))
    return out


TESTS = [
    (([[0, 0], [5, 5], [1, 1], [9, 0]],), 2),
    (([[3, 3], [3, 3]],), 0),
    (([[0, 0], [10, 0]],), 100),
    (([[-5, -5], [5, 5], [6, 4], [100, 100]],), 2),
] + _cases()
