"""
Strongly Connected Components                                                   [hard]

The graph is directed: edges are [a, b] meaning a → b, on nodes 0..n-1. A
strongly connected component is a largest group where every node can reach
every other. Return the number of components.

Example:
    count_scc(5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]])  ->  3       {0,1,2} {3} {4}

Aim for:  O(n + E) with Kosaraju. The last test has 20,000 nodes, so write the DFS iteratively.
Hint:     Pass 1: DFS the graph and record nodes in order of FINISHING. Pass 2: on the REVERSED graph,
          take nodes in reverse finishing order. Each DFS from an unvisited node there marks exactly one SCC.
"""


def count_scc(n: int, edges: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(n, edges):
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)

    def reach(s):
        seen, stack = {s}, [s]
        while stack:
            for u in adj[stack.pop()]:
                if u not in seen:
                    seen.add(u)
                    stack.append(u)
        return seen
    r = [reach(i) for i in range(n)]
    groups = {frozenset(j for j in range(n) if j in r[i] and i in r[j]) for i in range(n)}
    return len(groups)


def _cases():
    import random
    rng = random.Random(317)
    out = []
    for _ in range(8):
        n = rng.randint(1, 9)
        edges = [[rng.randrange(n), rng.randrange(n)] for _ in range(rng.randint(0, 2 * n))]
        out.append(((n, edges), _brute(n, edges)))
    n = 20_000
    edges = [[i, i + 1] for i in range(n - 1)]
    edges += [[i + 9, i] for i in range(0, n - 9, 10)]       # cycles of 10 consecutive nodes
    out.append(((n, edges), 2000))
    return out


USES = ["graph.adjacency"]

TESTS = [((5, [[0, 1], [1, 2], [2, 0], [1, 3], [3, 4]]), 3), ((3, []), 3), ((2, [[0, 1], [1, 0]]), 1)] + _cases()
