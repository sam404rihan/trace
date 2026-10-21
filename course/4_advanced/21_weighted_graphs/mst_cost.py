"""
Connect Every City                                                            [easy]

Cities are 0 to n - 1. Each road [a, b, cost] could be built to join a and b
both ways. Return the smallest total cost of roads that connects every city to
every other (directly or through others), or -1 if that's impossible.

Example:
    mst_cost(4, [[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]])  ->  7
        roads 0-1, 1-2 and 2-3. The road 0-2 would only join cities that are already joined.

Aim for:  O(roads log roads).
Hint:     Kruskal: sort the roads by cost and walk through them with union-find. Build a
          road when its two cities are in different groups, and skip it when they're
          already joined. Every city is connected once you've built n - 1 roads.
"""


def mst_cost(n: int, roads: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _fast(n, roads):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = built = 0
    for a, b, c in sorted(roads, key=lambda r: r[2]):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            total += c
            built += 1
    return total if built == n - 1 else -1


def _big():
    import random
    rng = random.Random(2101)
    n = 20_000
    roads = [[i, rng.randrange(i), rng.randint(1, 10**6)] for i in range(1, n)]    # a tree: connected
    roads += [[rng.randrange(n), rng.randrange(n), rng.randint(1, 10**6)] for _ in range(80_000)]
    return (n, roads), _fast(n, roads)


TEACHES = ["graph.mst"]
USES = ["uf.find", "uf.union"]

TESTS = [
    ((4, [[0, 1, 1], [1, 2, 2], [0, 2, 3], [2, 3, 4], [1, 3, 5]]), 7),
    ((1, []), 0),
    ((2, []), -1),
    ((3, [[0, 1, 5], [0, 1, 2], [1, 2, 3]]), 5),
    ((4, [[0, 1, 1], [2, 3, 1]]), -1),
    ((5, [[0, 1, 4], [0, 2, 4], [1, 2, 2], [2, 3, 3], [2, 4, 2], [3, 4, 3]]), 11),
    _big(),
]
