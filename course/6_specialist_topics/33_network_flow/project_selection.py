"""
Project Selection                                                             [hard]

profit[i] is what project i earns (negative = it costs money, like buying a
tool). requires lists pairs (a, b): if you do project a, you must also do
project b. Choose a set of projects that respects every requirement and
maximizes the total profit. Doing nothing (profit 0) is allowed.

Example:
    project_selection([10, -4, -3], [(0, 1), (0, 2)])          ->  3
        Project 0 needs both tools: 10 - 4 - 3.
    project_selection([5, -8, 6, -2], [(0, 1), (2, 3)])        ->  4      just projects 2 and 3
    project_selection([-1, -1], [])                            ->  0

Aim for:  one min cut (max flow) on n + 2 nodes.
Hint:     Source → i with capacity profit[i] for every profitable project, i → sink with capacity
          -profit[i] for every costly one, and a → b with infinite capacity for each requirement.
          A finite cut = a valid choice (the source side is what you do): cutting s → i means
          giving up a profit, cutting i → t means paying a cost, and an infinite edge can never
          be cut. Answer = (sum of positive profits) - (min cut).
"""


def project_selection(profit: list[int], requires: list[tuple[int, int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(profit, requires):
    n, best = len(profit), 0
    for mask in range(1 << n):
        if all(not mask >> a & 1 or mask >> b & 1 for a, b in requires):
            best = max(best, sum(profit[i] for i in range(n) if mask >> i & 1))
    return best


def _maxflow(n, edges, s, t):
    from collections import deque
    cap = [dict() for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] = cap[u].get(v, 0) + c
        cap[v].setdefault(u, 0)
    flow = 0
    while True:
        level = [-1] * n
        level[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for v, c in cap[u].items():
                if c > 0 and level[v] < 0:
                    level[v] = level[u] + 1
                    q.append(v)
        if level[t] < 0:
            return flow
        it = {u: iter(list(cap[u])) for u in range(n)}

        def push(u, f):
            if u == t:
                return f
            for v in it[u]:
                if cap[u][v] > 0 and level[v] == level[u] + 1:
                    got = push(v, min(f, cap[u][v]))
                    if got:
                        cap[u][v] -= got
                        cap[v][u] += got
                        return got
            return 0
        while True:
            f = push(s, float("inf"))
            if not f:
                break
            flow += f


def _closure(profit, requires):
    n = len(profit)
    s, t, edges = n, n + 1, []
    for i, p in enumerate(profit):
        if p > 0:
            edges.append((s, i, p))
        elif p < 0:
            edges.append((i, t, -p))
    big = sum(abs(p) for p in profit) + 1
    edges += [(a, b, big) for a, b in requires]
    return sum(p for p in profit if p > 0) - _maxflow(n + 2, edges, s, t)


def _cases():
    import random
    rng = random.Random(1956)
    out = []
    for _ in range(10):
        n = rng.randint(1, 10)
        profit = [rng.randint(-10, 10) for _ in range(n)]
        requires = [tuple(rng.sample(range(n), 2)) for _ in range(rng.randint(0, 12))] if n > 1 else []
        out.append(((profit, requires), _brute(profit, requires)))
    n = 60
    profit = [rng.randint(-100, 100) for _ in range(n)]
    requires = [tuple(rng.sample(range(n), 2)) for _ in range(120)]
    out.append(((profit, requires), _closure(profit, requires)))
    return out


TESTS = [
    (([10, -4, -3], [(0, 1), (0, 2)]), 3),
    (([5, -8, 6, -2], [(0, 1), (2, 3)]), 4),
    (([-1, -1], []), 0),
    (([7], []), 7),
    (([4, 4, -7], [(0, 2), (1, 2)]), 1),
    (([3, 3], [(0, 1), (1, 0)]), 6),
] + _cases()
