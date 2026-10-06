"""
Daily score board                                                             [build]

A game records one score per day. Build a board that answers questions about
any stretch of days instantly.

    board = ScoreBoard([3, 8, -2, 5, 7])
    board.total(1, 3)          ->  11        days 1..3 inclusive: 8 - 2 + 5
    board.average(0, 1)        ->  5.5
    board.best_stretch(2)      ->  12        best 2 days in a row: 5 + 7
    board.first_reaching(10)   ->  1         the earliest day where the running total reaches 10 (3 + 8)

Rules:
  - Days are 0-indexed. total and average include both ends.
  - average(i, j) is rounded to 2 decimals.
  - best_stretch(k) is the largest sum of k consecutive days (1 <= k <= number of days).
  - first_reaching(x) returns the first day d where total(0, d) >= x, or -1 if it never happens.

Aim for:  build a prefix array once in __init__. Then total/average are O(1),
          best_stretch is O(n) and first_reaching is O(n) (or O(log n) if scores are never negative).
"""


class ScoreBoard:
    def __init__(self, scores: list[int]):
        raise NotImplementedError

    def total(self, i: int, j: int) -> int:
        raise NotImplementedError

    def average(self, i: int, j: int) -> float:
        raise NotImplementedError

    def best_stretch(self, k: int) -> int:
        raise NotImplementedError

    def first_reaching(self, x: int) -> int:
        raise NotImplementedError


CLASS = "ScoreBoard"


def _big():
    import random
    rng = random.Random(14)
    scores = [rng.randint(-50, 100) for _ in range(50_000)]
    P = [0]
    for s in scores:
        P.append(P[-1] + s)
    calls, out = [("ScoreBoard", scores)], [None]
    for _ in range(50_000):
        i = rng.randint(0, len(scores) - 1)
        j = rng.randint(i, len(scores) - 1)
        calls.append(("total", i, j))
        out.append(P[j + 1] - P[i])
    return calls, out


_CALLS, _OUT = _big()

TESTS = [
    ([("ScoreBoard", [3, 8, -2, 5, 7]), ("total", 1, 3), ("average", 0, 1), ("best_stretch", 2), ("first_reaching", 10)],
     [None, 11, 5.5, 12, 1]),
    ([("ScoreBoard", [1, 2, 3]), ("total", 0, 2), ("average", 0, 2), ("best_stretch", 3), ("first_reaching", 100)],
     [None, 6, 2.0, 6, -1]),
    ([("ScoreBoard", [-5, 4, -1, 6]), ("best_stretch", 1), ("best_stretch", 3), ("first_reaching", 0), ("first_reaching", -5)],
     [None, 6, 9, 3, 0]),
    ([("ScoreBoard", [2, 2, 3]), ("average", 0, 2), ("average", 2, 2), ("total", 2, 2)],
     [None, 2.33, 3.0, 3]),
    (_CALLS, _OUT),
]
