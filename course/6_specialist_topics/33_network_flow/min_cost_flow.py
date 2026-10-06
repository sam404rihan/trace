"""
Minimum Cost Maximum Flow                                                     [hard]

A directed network has nodes 0..n-1 and edges (u, v, capacity, cost): up to
`capacity` units can flow from u to v, and each unit costs `cost` (costs are
>= 0). Send as much flow as possible from s to t, and among all maximum flows
pick the cheapest. Return [max flow, its minimum total cost].

Example:
    min_cost_flow(4, [(0, 1, 2, 1), (0, 2, 1, 2), (1, 2, 1, 1), (1, 3, 1, 3), (2, 3, 2, 1)], 0, 3)
        ->  [3, 10]
        One unit on each of 0→1→3 (cost 4), 0→1→2→3 (cost 3) and 0→2→3 (cost 3).
    min_cost_flow(3, [(0, 1, 5, 2), (1, 2, 3, 4)], 0, 2)  ->  [3, 18]

Aim for:  successive shortest paths: O(flow · V · E) with Bellman-Ford / SPFA.
Hint:     Like Ford-Fulkerson, but always augment along the CHEAPEST path in the residual graph.
          Every edge gets a reverse edge with capacity 0 and cost -cost (sending flow back
          refunds it), so use Bellman-Ford or SPFA, which handle the negative reverse costs.
          Push the bottleneck capacity along the path, add bottleneck × path cost, repeat until
          t is unreachable.
"""


def min_cost_flow(n: int, edges: list[tuple[int, int, int, int]], s: int, t: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _ssp(n, edges, s, t):
    """Successive shortest paths with Bellman-Ford over an edge list."""
    to, cap, cost, head = [], [], [], [[] for _ in range(n)]
    for u, v, c, w in edges:
        for a, b, cc, ww in ((u, v, c, w), (v, u, 0, -w)):
            head[a].append(len(to))
            to.append(b)
            cap.append(cc)
            cost.append(ww)
    flow = total = 0
    while True:
        dist, via = [float("inf")] * n, [-1] * n
        dist[s] = 0
        for _ in range(n):
            changed = False
            for u in range(n):
                if dist[u] == float("inf"):
                    continue
                for e in head[u]:
                    if cap[e] > 0 and dist[u] + cost[e] < dist[to[e]]:
                        dist[to[e]] = dist[u] + cost[e]
                        via[to[e]] = e
                        changed = True
            if not changed:
                break
        if dist[t] == float("inf"):
            return [flow, total]
        push, v = float("inf"), t
        while v != s:
            e = via[v]
            push = min(push, cap[e])
            v = to[e ^ 1]
        v = t
        while v != s:
            e = via[v]
            cap[e] -= push
            cap[e ^ 1] += push
            v = to[e ^ 1]
        flow += push
        total += push * dist[t]


def _brute_assignment(costs):
    """For bipartite unit-capacity tests: try every perfect assignment."""
    from itertools import permutations
    n = len(costs)
    return [n, min(sum(costs[i][p[i]] for i in range(n)) for p in permutations(range(n)))]


def _assignment_network(costs):
    n = len(costs)
    s, t = 2 * n, 2 * n + 1
    edges = [(s, i, 1, 0) for i in range(n)] + [(n + j, t, 1, 0) for j in range(n)]
    edges += [(i, n + j, 1, costs[i][j]) for i in range(n) for j in range(n)]
    return 2 * n + 2, edges, s, t


def _cases():
    import random
    rng = random.Random(1736)
    out = []
    for _ in range(5):                      # assignment problems, checked by brute force
        k = rng.randint(1, 6)
        costs = [[rng.randint(0, 20) for _ in range(k)] for _ in range(k)]
        out.append((_assignment_network(costs), _brute_assignment(costs)))
    for _ in range(5):                      # random networks
        n = rng.randint(2, 8)
        edges = [(*rng.sample(range(n), 2), rng.randint(1, 5), rng.randint(0, 9)) for _ in range(rng.randint(1, 16))]
        out.append(((n, edges, 0, n - 1), _ssp(n, edges, 0, n - 1)))
    n = 40
    edges = [(*rng.sample(range(n), 2), rng.randint(1, 20), rng.randint(0, 50)) for _ in range(200)]
    out.append(((n, edges, 0, n - 1), _ssp(n, edges, 0, n - 1)))
    return out


TESTS = [
    ((4, [(0, 1, 2, 1), (0, 2, 1, 2), (1, 2, 1, 1), (1, 3, 1, 3), (2, 3, 2, 1)], 0, 3), [3, 10]),
    ((3, [(0, 1, 5, 2), (1, 2, 3, 4)], 0, 2), [3, 18]),
    ((2, [], 0, 1), [0, 0]),
    ((2, [(0, 1, 4, 0), (0, 1, 2, 7)], 0, 1), [6, 14]),
    ((4, [(0, 1, 1, 1), (0, 2, 1, 5), (1, 3, 1, 5), (2, 3, 1, 1), (1, 2, 1, 1)], 0, 3), [2, 12]),
] + _cases()
