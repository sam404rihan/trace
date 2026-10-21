"""
Minimum Edge Weight Equilibrium Queries                                       [hard]

A tree has nodes 0..n-1 and edges [u, v, w] with weights w between 1 and 26.
For each query [a, b], how many edges on the path from a to b would you have to
change (each change sets one edge's weight to anything) so that every edge on
the path has the same weight? Queries are independent. Return the answers.

Example:
    path_weight_queries(7, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 2], [4, 5, 2], [5, 6, 2]],
                        [[0, 3], [3, 6], [2, 6], [0, 6]])
        ->  [0, 0, 1, 3]
        The path 2 → 6 has weights 1, 2, 2, 2: change the 1.

Aim for:  O((n + q) · log n · 26). Walking every path is O(n) per query: too slow for the big
          test (10,000 nodes, 10,000 queries).
Hint:     The answer is (path length) - (count of the most common weight on the path).
          Root the tree at 0 and store, for every node, count[node][w] = edges of weight w
          from the root down to node. With LCA l of a and b, the path's count of w is
          count[a][w] + count[b][w] - 2 * count[l][w], and its length is
          depth[a] + depth[b] - 2 * depth[l]. Find l with binary lifting.
"""


def path_weight_queries(n: int, edges: list[list[int]], queries: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _walk(n, edges, queries):
    """Find each path explicitly with parent pointers."""
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    parent, pw, depth = [-1] * n, [0] * n, [0] * n
    seen, stack = {0}, [0]
    while stack:
        u = stack.pop()
        for v, w in adj[u]:
            if v not in seen:
                seen.add(v)
                parent[v], pw[v], depth[v] = u, w, depth[u] + 1
                stack.append(v)
    out = []
    for a, b in queries:
        weights = []
        while a != b:
            if depth[a] < depth[b]:
                a, b = b, a
            weights.append(pw[a])
            a = parent[a]
        out.append(len(weights) - max((weights.count(w) for w in set(weights)), default=0))
    return out


def _fast(n, edges, queries):
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    LOG = max(1, n.bit_length())
    up = [[0] * n for _ in range(LOG)]
    depth, cnt = [0] * n, [None] * n
    cnt[0] = [0] * 27
    seen, stack = [False] * n, [0]
    seen[0] = True
    while stack:
        u = stack.pop()
        for v, w in adj[u]:
            if not seen[v]:
                seen[v] = True
                up[0][v], depth[v] = u, depth[u] + 1
                cnt[v] = cnt[u][:]
                cnt[v][w] += 1
                stack.append(v)
    for k in range(1, LOG):
        prev, cur = up[k - 1], up[k]
        for v in range(n):
            cur[v] = prev[prev[v]]

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        diff = depth[a] - depth[b]
        for k in range(LOG):
            if diff >> k & 1:
                a = up[k][a]
        if a == b:
            return a
        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a, b = up[k][a], up[k][b]
        return up[0][a]

    out = []
    for a, b in queries:
        l = lca(a, b)
        length = depth[a] + depth[b] - 2 * depth[l]
        most = max(cnt[a][w] + cnt[b][w] - 2 * cnt[l][w] for w in range(1, 27))
        out.append(length - most)
    return out


def _random_tree(rng, n, wmax):
    return [[rng.randrange(v), v, rng.randint(1, wmax)] for v in range(1, n)]


def _cases():
    import random
    rng = random.Random(2846)
    out = []
    for _ in range(8):
        n = rng.randint(1, 12)
        edges = _random_tree(rng, n, 3)
        queries = [[rng.randrange(n), rng.randrange(n)] for _ in range(6)]
        out.append(((n, edges, queries), _walk(n, edges, queries)))
    n = 10_000
    edges = [[v - 1 if rng.random() < 0.9 else rng.randrange(v), v, rng.randint(1, 26)] for v in range(1, n)]
    queries = [[rng.randrange(n), rng.randrange(n)] for _ in range(10_000)]
    out.append(((n, edges, queries), _fast(n, edges, queries)))
    return out


USES = ["prefix.sums", "tree.lift_jump", "tree.lift_table", "tree.bfs_order", "tree.lca"]

TESTS = [
    ((7, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 2], [4, 5, 2], [5, 6, 2]], [[0, 3], [3, 6], [2, 6], [0, 6]]),
     [0, 0, 1, 3]),
    ((8, [[1, 2, 6], [1, 3, 4], [2, 4, 6], [2, 5, 3], [3, 6, 6], [3, 0, 8], [7, 0, 2]], [[4, 6], [0, 4], [6, 5], [7, 4]]),
     [1, 2, 2, 3]),
    ((1, [], [[0, 0]]), [0]),
] + _cases()
