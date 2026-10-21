"""
Staff the Projects                                                            [easy]

Worker i can join at most limit[i] projects. Project j needs need[j] people. can lists
the (worker, project) pairs where the worker has the right skills. A worker fills at
most one seat on any one project. Return the most seats that can be filled.

Example:
    max_staffing([2, 1], [1, 2], [(0, 0), (0, 1), (1, 1)])  ->  3
        worker 0 joins both projects, worker 1 joins project 1
    max_staffing([1, 1], [2], [(0, 0)])  ->  1

Aim for:  one max flow.
Hint:     Source -> worker i with capacity limit[i]; worker -> project with capacity 1 for each
          allowed pair; project j -> sink with capacity need[j]. Every unit of flow is one
          seat, and the capacities enforce every rule.
"""

def _maxflow(n, edges, s, t):
    """Edmonds-Karp on an adjacency dict, for computing expected answers."""
    from collections import deque
    cap = [dict() for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] = cap[u].get(v, 0) + c
        cap[v].setdefault(u, 0)
    flow = 0
    while True:
        prev = {s: None}
        q = deque([s])
        while q and t not in prev:
            u = q.popleft()
            for v, c in cap[u].items():
                if c > 0 and v not in prev:
                    prev[v] = u
                    q.append(v)
        if t not in prev:
            return flow, cap
        path, v = [], t
        while v != s:
            path.append((prev[v], v))
            v = prev[v]
        push = min(cap[u][v] for u, v in path)
        for u, v in path:
            cap[u][v] -= push
            cap[v][u] += push
        flow += push


def max_staffing(limit: list[int], need: list[int], can: list[tuple[int, int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _model(limit, need, can):
    W, P = len(limit), len(need)
    s, t = W + P, W + P + 1
    edges = [(s, i, c) for i, c in enumerate(limit)] + [(W + j, t, c) for j, c in enumerate(need)]
    edges += [(i, W + j, 1) for i, j in can]
    return _maxflow(W + P + 2, edges, s, t)[0]


def _cases():
    import random
    rng = random.Random(3307)
    out = []
    for W, P, m in ((3, 2, 4), (5, 4, 10), (8, 6, 20), (20, 10, 80), (150, 60, 2000)):
        limit = [rng.randint(0, 4) for _ in range(W)]
        need = [rng.randint(0, 6) for _ in range(P)]
        can = list({(rng.randrange(W), rng.randrange(P)) for _ in range(m)})
        out.append(((limit, need, can), _model(limit, need, can)))
    for W, P in ((300, 300), (400, 350)):        # one seat each, two options each: greedy choices block each other
        limit, need = [1] * W, [1] * P
        can = list({(i, rng.randrange(P)) for i in range(W) for _ in range(2)})
        out.append(((limit, need, can), _model(limit, need, can)))
    return out


TEACHES = ["flow.model"]
USES = ["flow.augment"]

TESTS = [(([2, 1], [1, 2], [(0, 0), (0, 1), (1, 1)]), 3), (([1, 1], [2], [(0, 0)]), 1), (([3], [1, 1, 1, 1], [(0, 0), (0, 1), (0, 2), (0, 3)]), 3),
         (([], [2], []), 0), (([1, 1, 1], [0, 2], [(0, 0), (1, 0), (2, 1), (0, 1)]), 2),
         # traps for greedy seat filling: an early choice blocks the only seat someone else could take
         (([1, 1, 1, 1], [1, 1, 2], [(0, 2), (1, 1), (1, 2), (2, 0), (3, 0), (3, 1)]), 4),
         (([1, 1, 1], [1, 1, 1], [(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)]), 3)] + _cases()
