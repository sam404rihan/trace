"""
City with the fewest reachable neighbours                                    [guided]

Cities 0..n-1 are joined by two-way roads [a, b, length]. For each city, count
how many OTHER cities are within `threshold` total distance. Return the city
with the smallest count. On a tie, return the one with the LARGEST number.

Example:
    city_fewest_reachable(4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4)  ->  3
        reachable within 4: city 0 → {1, 2}, 1 → {0, 2, 3}, 2 → {0, 1, 3}, 3 → {1, 2}
        0 and 3 tie with 2, so the larger one, 3, wins.
"""


def city_fewest_reachable(n: int, edges: list[list[int]], threshold: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(n, edges, threshold):
    INF = float("inf")
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for a, b, w in edges:
        d[a][b] = d[b][a] = min(d[a][b], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    counts = [sum(1 for j in range(n) if j != i and d[i][j] <= threshold) for i in range(n)]
    return max(i for i in range(n) if counts[i] == min(counts))


def _rand(seed, count, lo, hi):
    import random
    rng = random.Random(seed)
    out = []
    for _ in range(count):
        n = rng.randint(lo, hi)
        edges = []
        for _ in range(rng.randint(0, n * 2)):
            a, b = rng.sample(range(n), 2) if n > 1 else (0, 0)
            if a != b:
                edges.append([a, b, rng.randint(1, 9)])
        t = rng.randint(1, 15)
        out.append(((n, edges, t), _ref(n, edges, t)))
    return out


STEPS = [
    {
        "title": "All-pairs distances",
        "text": "Build an n×n distance matrix (0 on the diagonal, the road lengths, inf elsewhere) and run Floyd–Warshall: "
                "for k, for i, for j. Then count, for each city, the others within threshold.",
        "hint": "Two roads between the same pair can exist: keep the shorter one.",
        "tests": [((4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4), 3)] + _rand(312, 4, 3, 6),
    },
    {
        "title": "Ties go to the larger city",
        "text": "When several cities share the smallest count, return the largest number. Iterate in a way that "
                "lets later (bigger) cities win ties.",
        "hint": "Use `<=` when comparing counts while scanning cities from 0 to n-1.",
        "tests": [((5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2), 0),
                  ((3, [], 5), 2), ((2, [[0, 1, 1]], 1), 1)] + _rand(313, 4, 3, 7),
    },
    {
        "title": "Bigger maps",
        "text": "Up to 70 cities, some cut off from the rest. Floyd–Warshall is O(n³), a few hundred thousand steps here. "
                "Make sure unreachable cities stay at inf, and never count as within threshold.",
        "hint": "Skip k-rows quickly when d[i][k] is inf. It's a cheap speed-up in Python.",
        "tests": _rand(314, 3, 40, 70),
    },
]
