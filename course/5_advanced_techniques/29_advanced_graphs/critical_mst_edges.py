"""
Critical and Pseudo-Critical Edges in an MST                                  [hard]

A connected undirected graph has nodes 0..n-1 and edges[i] = [a, b, weight].
An edge is CRITICAL if removing it makes every minimum spanning tree heavier
(or leaves the graph disconnected). It's PSEUDO-CRITICAL if it appears in some
MST but not all of them. Return [critical indices, pseudo-critical indices],
each sorted.

Example:
    critical_mst_edges(5, [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [0, 4, 3], [3, 4, 3], [1, 4, 6]])
        ->  [[0, 1], [2, 3, 4, 5]]
    critical_mst_edges(4, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 1]])
        ->  [[], [0, 1, 2, 3]]

Aim for:  O(E² α(n)): one Kruskal run per edge.
Hint:     Compute the MST weight W with Kruskal (sort by weight, union-find). Then for each edge i:
          - Run Kruskal WITHOUT edge i. If the result is heavier than W (or not spanning),
            i is critical.
          - Otherwise run Kruskal with edge i FORCED in first. If that still totals W, i belongs
            to some MST: it's pseudo-critical.
"""


def critical_mst_edges(n: int, edges: list[list[int]]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def _all_msts(n, edges):
    """Every spanning tree by brute force (tiny graphs only): which edges are in all / some MSTs."""
    from itertools import combinations
    best, trees = None, []
    for pick in combinations(range(len(edges)), n - 1):
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                x = parent[x]
            return x
        ok = True
        for i in pick:
            a, b = find(edges[i][0]), find(edges[i][1])
            if a == b:
                ok = False
                break
            parent[a] = b
        if not ok:
            continue
        w = sum(edges[i][2] for i in pick)
        if best is None or w < best:
            best, trees = w, [set(pick)]
        elif w == best:
            trees.append(set(pick))
    in_all = set.intersection(*trees)
    in_some = set.union(*trees) - in_all
    return [sorted(in_all), sorted(in_some)]


def _kruskal_answer(n, edges):
    order = sorted(range(len(edges)), key=lambda i: edges[i][2])

    def mst(skip=-1, force=-1):
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        total, used = 0, 0
        if force >= 0:
            a, b, w = edges[force]
            parent[find(a)] = find(b)
            total, used = w, 1
        for i in order:
            if i == skip:
                continue
            a, b = find(edges[i][0]), find(edges[i][1])
            if a != b:
                parent[a] = b
                total += edges[i][2]
                used += 1
        return total if used == n - 1 else float("inf")

    base = mst()
    crit, pseudo = [], []
    for i in range(len(edges)):
        if mst(skip=i) > base:
            crit.append(i)
        elif mst(force=i) == base:
            pseudo.append(i)
    return [crit, pseudo]


def _connected_graph(rng, n, extra, wmax):
    edges = [[rng.randrange(i), i, rng.randint(1, wmax)] for i in range(1, n)]
    for _ in range(extra):
        a, b = rng.sample(range(n), 2)
        edges.append([a, b, rng.randint(1, wmax)])
    rng.shuffle(edges)
    return edges


def _cases():
    import random
    rng = random.Random(1489)
    out = []
    for _ in range(8):
        n = rng.randint(2, 5)
        edges = _connected_graph(rng, n, rng.randint(0, 4), 3)
        out.append(((n, edges), _all_msts(n, edges)))
    n = 60
    edges = _connected_graph(rng, n, 140, 20)
    out.append(((n, edges), _kruskal_answer(n, edges)))
    return out


TESTS = [
    ((5, [[0, 1, 1], [1, 2, 1], [2, 3, 2], [0, 3, 2], [0, 4, 3], [3, 4, 3], [1, 4, 6]]), [[0, 1], [2, 3, 4, 5]]),
    ((4, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 1]]), [[], [0, 1, 2, 3]]),
    ((2, [[0, 1, 5]]), [[0], []]),
    ((3, [[0, 1, 1], [1, 2, 1], [0, 2, 3]]), [[0, 1], []]),
] + _cases()
