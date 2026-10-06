"""
Subtree Sizes                                                                   [easy]

A tree has n nodes (0..n-1) joined by the n - 1 undirected edges in edges. Root it
at node 0 and return a list where entry v is the number of nodes in v's subtree
(v itself included).

Example:
    subtree_sizes(5, [(0, 1), (0, 2), (1, 3), (1, 4)])  ->  [5, 3, 1, 1, 1]

Aim for:  O(n). The last test is a path of 100,000 nodes, far deeper than Python's
          recursion limit, so use an explicit stack or a BFS order.
Hint:     BFS from 0, recording each node's parent and the visiting order. Then walk that order
          BACKWARDS (children always come after their parent) and add size[v] into size[parent[v]].
"""


def subtree_sizes(n: int, edges: list[tuple[int, int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _ref(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    par, order, seen = [-1] * n, [0], [False] * n
    seen[0] = True
    for v in order:
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True
                par[w] = v
                order.append(w)
    size = [1] * n
    for v in reversed(order[1:]):
        size[par[v]] += size[v]
    return size


def _cases():
    import random
    rng = random.Random(3206)
    out = []
    for n in (2, 3, 8, 30, 200):
        edges = [(rng.randrange(v), v) for v in range(1, n)]
        rng.shuffle(edges)
        edges = [(b, a) if rng.random() < 0.5 else (a, b) for a, b in edges]
        out.append(((n, edges), _ref(n, edges)))
    n = 100_000
    path = list(range(n))
    rng.shuffle(path)
    path.remove(0)
    path = [0] + path
    edges = [(path[i], path[i + 1]) for i in range(n - 1)]
    want = [0] * n
    for i, v in enumerate(path):
        want[v] = n - i
    out.append(((n, edges), want))
    return out


TESTS = [((5, [(0, 1), (0, 2), (1, 3), (1, 4)]), [5, 3, 1, 1, 1]), ((1, []), [1]), ((2, [(1, 0)]), [2, 1]),
         ((4, [(3, 2), (2, 1), (1, 0)]), [4, 3, 2, 1])] + _cases()
