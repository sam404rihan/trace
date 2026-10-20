"""
Max Value of Equation                                                         [hard]

`points` is a list of [x, y] sorted by x (all x different). Find the largest
value of  y_i + y_j + |x_i - x_j|  over pairs i < j with |x_i - x_j| <= k.
At least one pair is close enough.

Example:
    max_value_of_equation([[1, 3], [2, 0], [5, 10], [6, -10]], 1)  ->  4
        (1, 3) and (2, 0): 3 + 0 + 1.
    max_value_of_equation([[0, 0], [3, 0], [9, 2]], 3)             ->  3

Aim for:  O(n) with a monotonic deque.
Hint:     Since x_j > x_i, the value is (y_j + x_j) + (y_i - x_i). For each j you want the biggest
          y_i - x_i among earlier points with x_j - x_i <= k: a sliding-window maximum. Drop
          front points that are too far left, read the front, then pop back points whose
          y - x is <= the new one and push j.
"""


def max_value_of_equation(points: list[list[int]], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(points, k):
    return max(points[i][1] + points[j][1] + points[j][0] - points[i][0]
               for i in range(len(points)) for j in range(i + 1, len(points))
               if points[j][0] - points[i][0] <= k)


def _fast(points, k):
    from collections import deque
    dq, best = deque(), float("-inf")
    for x, y in points:
        while dq and x - dq[0][1] > k:
            dq.popleft()
        if dq:
            best = max(best, dq[0][0] + y + x)
        while dq and dq[-1][0] <= y - x:
            dq.pop()
        dq.append((y - x, x))
    return best


def _cases():
    import random
    rng = random.Random(1499)
    out = []
    for _ in range(10):
        xs = sorted(rng.sample(range(0, 30), rng.randint(2, 10)))
        k = max(xs[i + 1] - xs[i] for i in range(len(xs) - 1))
        pts = [[x, rng.randint(-10, 10)] for x in xs]
        out.append(((pts, k), _brute(pts, k)))
    xs = sorted(rng.sample(range(0, 5 * 10**6), 50_000))
    pts = [[x, rng.randint(-10**6, 10**6)] for x in xs]
    out.append(((pts, 50_000), _fast(pts, 50_000)))
    return out


USES = ["pairs.split_by_index", "window.variable", "deque.monotonic"]

TESTS = [
    (([[1, 3], [2, 0], [5, 10], [6, -10]], 1), 4),
    (([[0, 0], [3, 0], [9, 2]], 3), 3),
    (([[1, 1], [2, 2]], 5), 4),
    (([[-19, 9], [-15, -19], [-5, -8]], 10), -6),
] + _cases()
