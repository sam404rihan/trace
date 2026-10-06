"""
Minimum Cost to Cut a Stick                                                   [hard]

A wooden stick runs from 0 to n. You must cut it at every position in `cuts`
(distinct, strictly between 0 and n), in any order you like. Each cut costs
the length of the piece being cut. Return the smallest total cost.

Example:
    min_cost_cut_stick(7, [1, 3, 4, 5])        ->  16
        Cut at 3 (7), then 5 (4), then 1 (3), then 4 (2).
    min_cost_cut_stick(9, [5, 6, 1, 4, 2])     ->  22

Aim for:  O(m³) interval DP, m = len(cuts) + 2.
Hint:     Sort the cuts and add the ends: points = [0] + sorted(cuts) + [n]. cost(i, j) = the
          cheapest way to make every cut strictly between points[i] and points[j]. Some cut k
          between them goes first and costs points[j] - points[i]; then the two sides are
          independent: cost(i, j) = (points[j] - points[i]) + min over k of cost(i, k) + cost(k, j).
          Fill it for growing gaps j - i.
"""


def min_cost_cut_stick(n: int, cuts: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(n, cuts):
    """Try every cutting order."""
    from itertools import permutations
    best = float("inf")
    for order in permutations(cuts):
        pieces, cost = [(0, n)], 0
        for c in order:
            for k, (a, b) in enumerate(pieces):
                if a < c < b:
                    cost += b - a
                    pieces[k:k + 1] = [(a, c), (c, b)]
                    break
        best = min(best, cost)
    return best


def _dp(n, cuts):
    pts = [0] + sorted(cuts) + [n]
    m = len(pts)
    cost = [[0] * m for _ in range(m)]
    for gap in range(2, m):
        for i in range(m - gap):
            j = i + gap
            cost[i][j] = pts[j] - pts[i] + min(cost[i][k] + cost[k][j] for k in range(i + 1, j))
    return cost[0][m - 1]


def _cases():
    import random
    rng = random.Random(1547)
    out = []
    for _ in range(8):
        n = rng.randint(2, 20)
        cuts = rng.sample(range(1, n), rng.randint(1, min(6, n - 1)))
        out.append(((n, cuts), _brute(n, cuts)))
    n = 10**6
    cuts = rng.sample(range(1, n), 80)
    out.append(((n, cuts), _dp(n, cuts)))
    return out


TESTS = [
    ((7, [1, 3, 4, 5]), 16),
    ((9, [5, 6, 1, 4, 2]), 22),
    ((2, [1]), 2),
    ((10, [5]), 10),
    ((4, [1, 2, 3]), 8),
] + _cases()
