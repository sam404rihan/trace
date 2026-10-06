"""
Best Sightseeing Pair                                                         [hard]

values[i] is how good viewpoint i is. Visiting viewpoints i < j scores
values[i] + values[j] + i - j: the walk between them costs one point per step.
Return the best score of any pair. There are at least 2 viewpoints and up to
100,000, so trying every pair is too slow.

Example:
    best_sightseeing_pair([8, 1, 5, 2, 6])  ->  11      i = 0, j = 2:  8 + 5 + 0 - 2
    best_sightseeing_pair([1, 2])           ->  2

Aim for:  O(n) time, O(1) extra space.
Hint:     Split the score into a part that depends only on i and a part only on j:
          (values[i] + i) + (values[j] - j). Walking j left to right, keep the best
          values[i] + i seen so far.
"""


def best_sightseeing_pair(values: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(values):
    n = len(values)
    return max(values[i] + values[j] + i - j for i in range(n) for j in range(i + 1, n))


def _fast(values):
    best_i, best = values[0], float("-inf")
    for j in range(1, len(values)):
        best = max(best, best_i + values[j] - j)
        best_i = max(best_i, values[j] + j)
    return best


def _cases():
    import random
    rng = random.Random(1014)
    out = []
    for _ in range(7):
        values = [rng.randint(1, 30) for _ in range(rng.randint(2, 25))]
        out.append(((values,), _brute(values)))
    big = [rng.randint(1, 1000) for _ in range(100_000)]
    out.append(((big,), _fast(big)))
    return out


TESTS = [
    (([8, 1, 5, 2, 6],), 11),
    (([1, 2],), 2),
    (([1, 1, 1],), 1),
    (([1, 3, 5],), 7),
    (([10, 1, 1, 1, 1, 10],), 15),
] + _cases()
