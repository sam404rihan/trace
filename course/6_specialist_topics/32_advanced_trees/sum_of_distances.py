"""
Sum of Distances in Tree                                                        [hard]

A tree has n nodes and n - 1 undirected edges. For every node v, return the sum of
its distances to all the other nodes.

Example:
    sum_of_distances(6, [(0, 1), (0, 2), (2, 3), (2, 4), (2, 5)])  ->  [8, 12, 6, 10, 10, 10]

Aim for:  O(n). The last test has 50,000 nodes, so a BFS from every node (O(n²)) is too slow.
Hint:     Root at 0. One pass bottom-up gives size[v] (nodes in v's subtree) and ans[0] (the sum of
          all depths). Then rerooting top-down: moving the root from p to its child c brings the
          size[c] nodes under c one step closer and the other n - size[c] one step farther, so
          ans[c] = ans[p] - size[c] + (n - size[c]).
"""


def sum_of_distances(n: int, edges: list[tuple[int, int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _ref(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    par, order, depth = [-1] * n, [0], [0] * n
    seen = [False] * n
    seen[0] = True
    for v in order:
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True
                par[w] = v
                depth[w] = depth[v] + 1
                order.append(w)
    size = [1] * n
    for v in reversed(order[1:]):
        size[par[v]] += size[v]
    ans = [0] * n
    ans[0] = sum(depth)
    for v in order[1:]:
        ans[v] = ans[par[v]] - size[v] + (n - size[v])
    return ans


def _brute(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    out = []
    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        q = [s]
        for v in q:
            for w in adj[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    q.append(w)
        out.append(sum(dist))
    return out


def _cases():
    import random
    rng = random.Random(3210)
    out = []
    for n in (2, 3, 7, 25, 150):
        edges = [(rng.randrange(v), v) for v in range(1, n)]
        edges = [(b, a) if rng.random() < 0.5 else (a, b) for a, b in edges]
        out.append(((n, edges), _brute(n, edges)))
    n = 50_000
    edges = [(rng.randrange(max(0, v - 50), v), v) for v in range(1, n)]
    out.append(((n, edges), _ref(n, edges)))
    return out


USES = ["tree.bfs_order", "tree.reroot"]

TESTS = [((6, [(0, 1), (0, 2), (2, 3), (2, 4), (2, 5)]), [8, 12, 6, 10, 10, 10]), ((1, []), [0]), ((2, [(1, 0)]), [1, 1])] + _cases()
