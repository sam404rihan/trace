"""
Graph Valid Tree                                                              [medium]

Nodes are 0..n-1 and `edges` are undirected. Return True if they form a valid
tree: connected, with no cycles.

Example:
    graph_valid_tree(5, [[0, 1], [0, 2], [0, 3], [1, 4]])            ->  True
    graph_valid_tree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]])    ->  False

Aim for:  near O(n) with union-find (or a single DFS).
Hint:     A tree has exactly n - 1 edges. If that's true, it's a tree exactly when no edge joins
          two nodes that are already connected: union-find spots that instantly.
"""


def graph_valid_tree(n: int, edges: list[list[int]]) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(n, edges):
    if len(edges) != n - 1:
        return False
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen, stack = {0}, [0]
    while stack:
        for v in adj[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def _cases():
    import random
    rng = random.Random(89)
    out = []
    for _ in range(10):
        n = rng.randint(1, 8)
        edges = [[i, rng.randrange(i)] for i in range(1, n)]
        r = rng.random()
        if r < 0.3 and n > 2:
            a, b = rng.sample(range(n), 2)
            edges.append([a, b])
        elif r < 0.6 and edges:
            edges.pop(rng.randrange(len(edges)))
        rng.shuffle(edges)
        out.append(((n, edges), _brute(n, edges)))
    return out


TESTS = [((5, [[0, 1], [0, 2], [0, 3], [1, 4]]), True), ((5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]), False),
         ((1, []), True), ((4, [[0, 1], [2, 3]]), False), ((3, [[0, 1], [1, 0]]), False)] + _cases()
