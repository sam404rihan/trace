"""
Shortest round trip                                                          [guided]

dist[i][j] is the cost of travelling from city i to city j (it may differ from
dist[j][i]). Start at city 0, visit every city exactly once, and return to 0.
Return the cheapest total cost. This is the travelling salesman problem.

Example:
    shortest_tour([[0, 10, 15, 20],
                   [10, 0, 35, 25],
                   [15, 35, 0, 30],
                   [20, 25, 30, 0]])   ->  80       0 → 1 → 3 → 2 → 0
"""


def shortest_tour(dist: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(dist):
    from itertools import permutations as perms
    n = len(dist)
    if n == 1:
        return 0
    best = float("inf")
    for order in perms(range(1, n)):
        route = (0,) + order + (0,)
        best = min(best, sum(dist[a][b] for a, b in zip(route, route[1:])))
    return best


def _held_karp(dist):
    n = len(dist)
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        row = dp[mask]
        for last in range(n):
            cost = row[last]
            if cost == INF:
                continue
            for nxt in range(n):
                if not mask >> nxt & 1:
                    new = mask | 1 << nxt
                    if cost + dist[last][nxt] < dp[new][nxt]:
                        dp[new][nxt] = cost + dist[last][nxt]
    return min(dp[(1 << n) - 1][last] + dist[last][0] for last in range(n)) if n > 1 else 0


def _rand(seed, count, lo, hi, sym=True):
    import random
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        n = rng.randint(lo, hi)
        d = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    d[i][j] = d[j][i] if sym and j < i else rng.randint(1, 50)
        out.append(d)
    return out


_BIG = _rand(303, 1, 13, 13, sym=False)[0]

USES = ["bits.shift_mask", "dp.bitmask"]

STEPS = [
    {
        "title": "Try every order",
        "text": "Try every ordering of cities 1..n-1 (itertools.permutations), add up each round trip, and keep the cheapest.",
        "hint": "route = (0,) + order + (0,), and the cost is the sum of dist[a][b] over consecutive pairs.",
        "tests": [(([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]],), 80)]
                 + [((d,), _brute(d)) for d in _rand(301, 4, 3, 6)],
    },
    {
        "title": "Edges",
        "text": "A single city costs 0. Two cities is there and back. One-way costs can differ from the way back.",
        "hint": "With n == 1 there's nothing to permute.",
        "tests": [(([[0]],), 0), (([[0, 3], [8, 0]],), 11)] + [((d,), _brute(d)) for d in _rand(302, 4, 3, 6, sym=False)],
    },
    {
        "title": "Make it fast: bitmask DP",
        "text": "13 cities means 12! = 479 million orderings. But the future of a partial tour only depends on WHICH cities "
                "you've visited and WHERE you are now. dp[mask][last] = the cheapest way to visit exactly the cities in mask, "
                "ending at last. That's 2^13 · 13 states, each tried with 13 next cities: about a million steps.",
        "hint": "dp[1][0] = 0. For each mask in increasing order, for each last with a finite cost, for each nxt not in mask: "
                "relax dp[mask | 1 << nxt][nxt]. Answer: min over last of dp[full][last] + dist[last][0].",
        "tests": [((d,), _brute(d)) for d in _rand(304, 2, 5, 7, sym=False)] + [((_BIG,), 60)],
    },
]
