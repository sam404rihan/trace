"""
Minimum Edge Reversals So Every Node Is Reachable                             [easy]

n nodes are joined by n - 1 DIRECTED edges [u, v] (u → v). Ignoring
directions, they form a tree. For every node i, find the fewest edges you'd
have to reverse so that i can reach every other node by following edge
directions. Return the answers as a list, answer[i] for node i.

Example:
    min_edge_reversals(4, [[2, 0], [2, 1], [1, 3]])   ->  [1, 1, 0, 2]
        From 2 everything is reachable already. From 0, reverse 2 → 0.
    min_edge_reversals(3, [[1, 2], [2, 0]])           ->  [2, 0, 1]

Aim for:  O(n) with rerooting: two passes over the tree.
Hint:     Store each edge both ways: (v, cost 0) from u, and (u, cost 1) from v (going against
          the arrow costs a reversal). First pass from node 0: answer[0] = total cost of all
          edges walked away from 0. Second pass: moving the root from u to its child v changes
          only the edge between them, so answer[v] = answer[u] - cost(u→v) + cost(v→u).
          Use an explicit stack: the big test is a 20,000-node path.
"""


def min_edge_reversals(n: int, edges: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _brute(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append((v, 0))
        adj[v].append((u, 1))
    out = []
    for root in range(n):
        total, seen, stack = 0, {root}, [root]
        while stack:
            u = stack.pop()
            for v, c in adj[u]:
                if v not in seen:
                    seen.add(v)
                    total += c
                    stack.append(v)
        out.append(total)
    return out


def _reroot(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append((v, 0))
        adj[v].append((u, 1))
    ans = [0] * n
    order, parent, stack = [], [-1] * n, [0]
    seen = [False] * n
    seen[0] = True
    while stack:
        u = stack.pop()
        order.append(u)
        for v, c in adj[u]:
            if not seen[v]:
                seen[v] = True
                parent[v] = u
                ans[0] += c
                stack.append(v)
    for u in order:
        for v, c in adj[u]:
            if parent[v] == u:
                ans[v] = ans[u] - c + (1 - c)
    return ans


def _random_tree(rng, n):
    edges = []
    for v in range(1, n):
        u = rng.randrange(v)
        edges.append([u, v] if rng.random() < 0.5 else [v, u])
    perm = list(range(n))
    rng.shuffle(perm)
    return [[perm[a], perm[b]] for a, b in edges]


def _cases():
    import random
    rng = random.Random(2858)
    out = []
    for _ in range(10):
        n = rng.randint(1, 12)
        edges = _random_tree(rng, n)
        out.append(((n, edges), _brute(n, edges)))
    n = 20_000
    path = [[i, i + 1] if rng.random() < 0.5 else [i + 1, i] for i in range(n - 1)]
    out.append(((n, path), _reroot(n, path)))
    edges = _random_tree(rng, n)
    out.append(((n, edges), _reroot(n, edges)))
    return out


TEACHES = ["tree.reroot"]
USES = ["tree.bfs_order"]

TESTS = [
    ((4, [[2, 0], [2, 1], [1, 3]]), [1, 1, 0, 2]),
    ((3, [[1, 2], [2, 0]]), [2, 0, 1]),
    ((1, []), [0]),
    ((2, [[0, 1]]), [0, 1]),
] + _cases()
