"""
K Closest Points to Origin                                                  [medium]

`points` is a list of [x, y] points. Return the k points closest to (0, 0),
in any order. The answer is unique.

Example:
    k_closest([[3, 3], [5, -1], [-2, 4]], 2)  ->  [[3, 3], [-2, 4]]

Aim for:  O(n log k)
Hint:     Compare squared distances x*x + y*y (no square root needed).
          heapq.nsmallest(k, points, key=...) is one line. Then try the
          size-k max-heap version by hand: push (-dist, x, y).
"""


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected):
    """Any order is fine."""
    return sorted(map(list, got)) == sorted(expected)


USES = ["heap.top_k", "heap.max_negate"]

TESTS = [
    (([[1, 3], [-2, 2]], 1), [[-2, 2]]),
    (([[3, 3], [5, -1], [-2, 4]], 2), [[3, 3], [-2, 4]]),
    (([[0, 1], [1, 0]], 2), [[0, 1], [1, 0]]),
    (([[10, 10], [1, 1], [-5, 0], [2, -2]], 2), [[1, 1], [2, -2]]),
]
