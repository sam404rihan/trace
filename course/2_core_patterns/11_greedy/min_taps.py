"""
Minimum Number of Taps to Water a Garden                                      [hard]

A garden runs along a line from 0 to n. There are n + 1 taps, at positions
0, 1, ..., n. Tap i with range r = ranges[i] waters [i - r, i + r] (ranges can
be 0). Return the fewest taps you need to open to water all of [0, n], or -1 if
it can't be done.

Example:
    min_taps(5, [3, 4, 1, 1, 0, 0])   ->  1      tap 1 waters [-3, 5]
    min_taps(3, [0, 0, 0, 0])         ->  -1
    min_taps(7, [1, 2, 1, 0, 2, 1, 0, 1])  ->  3

Aim for:  O(n), like the jump game.
Hint:     For each left point, record the farthest right any tap starting there reaches:
          reach[max(0, i - r)] = max(..., i + r). Then walk 0..n like "jump game II": keep the end
          of the current tap's coverage and the farthest reachable so far. When you pass the
          current end, open another tap (count += 1). If the farthest can't move past you, -1.
"""


def min_taps(n: int, ranges: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _dp(n, ranges):
    INF = float("inf")
    best = [INF] * (n + 1)                  # best[x]: taps needed to water [0, x]
    best[0] = 0
    taps = sorted((max(0, i - r), min(n, i + r)) for i, r in enumerate(ranges))
    for left, right in taps:
        if best[left] == INF:
            continue
        for x in range(left + 1, right + 1):
            best[x] = min(best[x], best[left] + 1)
    return best[n] if best[n] < INF else -1


def _cases():
    import random
    rng = random.Random(1326)
    out = []
    for _ in range(10):
        n = rng.randint(1, 12)
        ranges = [rng.choice([0, 0, 1, 1, 2, 3]) for _ in range(n + 1)]
        out.append(((n, ranges), _dp(n, ranges)))
    return out


USES = ["greedy.farthest_reach"]

TESTS = [
    ((5, [3, 4, 1, 1, 0, 0]), 1),
    ((3, [0, 0, 0, 0]), -1),
    ((7, [1, 2, 1, 0, 2, 1, 0, 1]), 3),
    ((8, [4, 0, 0, 0, 0, 0, 0, 0, 4]), 2),
    ((8, [4, 0, 0, 0, 4, 0, 0, 0, 4]), 1),
    ((1, [0, 0]), -1),
    ((1, [1, 0]), 1),
] + _cases()
