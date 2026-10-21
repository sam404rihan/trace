"""
Minimum Cost to Reach Destination in Time                                     [hard]

Cities 0..n-1 are joined by two-way roads: edges[i] = [x, y, minutes]. There
can be several roads between the same two cities. Every time you pass through
a city (including the start and the end) you pay fees[city]. Travel from city 0
to city n - 1 in at most `max_time` minutes, paying as little as possible.
Return the lowest total fee, or -1 if you can't make it in time.

Example:
    min_cost_in_time(30, [[0, 1, 10], [1, 2, 10], [2, 5, 10], [0, 3, 1], [3, 4, 10], [4, 5, 15]],
                     [5, 1, 2, 20, 20, 3])  ->  11      0 → 1 → 2 → 5 takes 30 minutes
    min_cost_in_time(29, (same roads), (same fees))   ->  48      0 → 3 → 4 → 5 takes 26 minutes

Aim for:  O(max_time × edges) with DP over time, or Dijkstra on cost with a time check.
Hint:     Plain Dijkstra on cost isn't enough: a cheaper route may be too slow. One clean way:
          best[t][v] = cheapest way to stand at v having used exactly t minutes; fill it for
          t = 0..max_time, relaxing every edge. Or run Dijkstra on (cost, time, city), and only
          push a state if its time beats the best time recorded for that city so far
          (cheaper-but-slower states have already been beaten).
"""


def min_cost_in_time(max_time: int, edges: list[list[int]], fees: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _dp(max_time, edges, fees):
    n = len(fees)
    INF = float("inf")
    best = [[INF] * n for _ in range(max_time + 1)]
    best[0][0] = fees[0]
    for t in range(max_time + 1):
        for x, y, m in edges:
            if t + m > max_time:
                continue
            if best[t][x] + fees[y] < best[t + m][y]:
                best[t + m][y] = best[t][x] + fees[y]
            if best[t][y] + fees[x] < best[t + m][x]:
                best[t + m][x] = best[t][y] + fees[x]
    ans = min(best[t][n - 1] for t in range(max_time + 1))
    return -1 if ans == INF else ans


def _cases():
    import random
    rng = random.Random(1928)
    out = []
    for _ in range(10):
        n = rng.randint(2, 7)
        edges = [[*rng.sample(range(n), 2), rng.randint(1, 10)] for _ in range(rng.randint(1, 12))]
        fees = [rng.randint(1, 20) for _ in range(n)]
        t = rng.randint(1, 30)
        out.append(((t, edges, fees), _dp(t, edges, fees)))
    n = 200
    edges = [[i, i + 1, rng.randint(1, 3)] for i in range(n - 1)]
    edges += [[*rng.sample(range(n), 2), rng.randint(1, 50)] for _ in range(800)]
    fees = [rng.randint(1, 1000) for _ in range(n)]
    out.append(((250, edges, fees), _dp(250, edges, fees)))
    return out


_ROADS = [[0, 1, 10], [1, 2, 10], [2, 5, 10], [0, 3, 1], [3, 4, 10], [4, 5, 15]]
_FEES = [5, 1, 2, 20, 20, 3]

USES = ["bfs.state", "sp.dijkstra"]

TESTS = [
    ((30, _ROADS, _FEES), 11),
    ((29, _ROADS, _FEES), 48),
    ((25, _ROADS, _FEES), -1),
    ((5, [[0, 1, 5]], [3, 4]), 7),
    ((4, [[0, 1, 5]], [3, 4]), -1),
    ((10, [[0, 1, 2], [0, 1, 9], [1, 2, 3]], [1, 1, 1]), 3),
] + _cases()
