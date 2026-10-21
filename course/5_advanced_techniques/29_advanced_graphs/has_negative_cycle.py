"""
Negative cycle detection                                                      [easy]

Directed edges [a, b, w] connect nodes 0..n-1, and weights can be negative.
Return True if the graph contains a cycle whose total weight is negative,
anywhere in the graph (not just one reachable from node 0).

Example:
    has_negative_cycle(3, [[0, 1, 1], [1, 2, -1], [2, 0, -1]])  ->  True      0 → 1 → 2 → 0 costs -1
    has_negative_cycle(3, [[0, 1, 1], [1, 2, -1], [2, 0, 1]])   ->  False

Aim for:  O(n · E) with Bellman–Ford. The last tests have 400 nodes and 4,000 edges:
          Floyd–Warshall's O(n³) times out on them.
Hint:     Start every distance at 0 (like a virtual source joined to all nodes), so every cycle is
          "reachable". Relax all edges n - 1 times. If ANY edge can still be relaxed after that, there's
          a negative cycle.
"""


def has_negative_cycle(n: int, edges: list[list[int]]) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(n, edges):
    INF = float("inf")
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for a, b, w in edges:
        d[a][b] = min(d[a][b], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    return any(d[i][i] < 0 for i in range(n))


def _cases():
    import random
    rng = random.Random(318)
    out = []
    for _ in range(12):
        n = rng.randint(1, 7)
        edges = [[rng.randrange(n), rng.randrange(n), rng.randint(-3, 8)] for _ in range(rng.randint(0, 2 * n))]
        out.append(((n, edges), _brute(n, edges)))
    return out


def _big():
    import random
    rng = random.Random(2901)
    n = 400
    edges = [[a, rng.randrange(a + 1, n), rng.randint(-10, 100)] for a in range(n - 1) for _ in range(10)]
    edges += [[rng.randrange(1, n), 0, 5_000] for _ in range(10)]     # back edges too dear for a negative loop
    rng.shuffle(edges)
    loop = edges + [[n - 1, n - 2, -10_000], [n - 2, n - 1, 0]]         # a loop of total -10,000
    return [((n, edges), False), ((n, loop), True)]


TEACHES = ["sp.negative_cycle"]
USES = ["sp.bellman_ford"]

TESTS = [((3, [[0, 1, 1], [1, 2, -1], [2, 0, -1]]), True), ((3, [[0, 1, 1], [1, 2, -1], [2, 0, 1]]), False),
         ((1, [[0, 0, -1]]), True), ((4, [[2, 3, -5], [3, 2, 4]]), True), ((2, [[0, 1, -10]]), False)] + _cases() + _big()
