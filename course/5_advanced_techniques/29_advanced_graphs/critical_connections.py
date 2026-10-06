"""
Critical Connections (bridges)                                                  [hard]

Servers 0..n-1 are linked by two-way connections. A connection is critical if
removing it disconnects some servers from others. Return every critical
connection as [smaller, larger], sorted.

Example:
    critical_connections(4, [[0, 1], [1, 2], [2, 0], [1, 3]])  ->  [[1, 3]]

Aim for:  O(n + E): Tarjan's low-link values. The last test has 20,000 servers. Recursion that deep
          crashes Python, so use an explicit stack (or a thread with a bigger stack).
Hint:     DFS, numbering nodes by discovery time tin. low[v] = the smallest tin reachable from v's subtree
          using at most one back edge. A tree edge (v, u) is a bridge exactly when low[u] > tin[v].
          Skip the edge you arrived by (track the edge index, not the parent node).
"""


def critical_connections(n: int, connections: list[list[int]]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def _connected_without(n, conns, skip):
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(conns):
        if i != skip:
            adj[a].append(b)
            adj[b].append(a)
    seen, stack = {0}, [0]
    while stack:
        for u in adj[stack.pop()]:
            if u not in seen:
                seen.add(u)
                stack.append(u)
    return len(seen) == n


def _brute(n, conns):
    return sorted(sorted(c) for i, c in enumerate(conns) if not _connected_without(n, conns, i))


def _bridges(n, conns):
    adj = [[] for _ in range(n)]
    for i, (a, b) in enumerate(conns):
        adj[a].append((b, i))
        adj[b].append((a, i))
    tin, low, timer, out = [-1] * n, [0] * n, 0, []
    for root in range(n):
        if tin[root] != -1:
            continue
        tin[root] = low[root] = timer; timer += 1
        stack = [(root, -1, 0)]
        while stack:
            v, pe, idx = stack[-1]
            if idx < len(adj[v]):
                stack[-1] = (v, pe, idx + 1)
                u, e = adj[v][idx]
                if e == pe:
                    continue
                if tin[u] == -1:
                    tin[u] = low[u] = timer; timer += 1
                    stack.append((u, e, 0))
                else:
                    low[v] = min(low[v], tin[u])
            else:
                stack.pop()
                if stack:
                    p = stack[-1][0]
                    low[p] = min(low[p], low[v])
                    if low[v] > tin[p]:
                        out.append(sorted((p, v)))
    return sorted(out)


def _cases():
    import random
    rng = random.Random(316)
    out = []
    for _ in range(8):
        n = rng.randint(2, 9)
        conns = [[i, rng.randrange(i)] for i in range(1, n)]
        for _ in range(rng.randint(0, n)):
            a, b = rng.sample(range(n), 2)
            if sorted([a, b]) not in [sorted(c) for c in conns]:
                conns.append([a, b])
        out.append(((n, conns), _brute(n, conns)))
    n = 20_000
    conns = [[i, i + 1] for i in range(n - 1)]               # a long path: every edge is a bridge...
    conns += [[i, i + 2] for i in range(0, n - 2, 50)]       # ...except where shortcuts make cycles
    out.append(((n, conns), _bridges(n, conns)))
    return out


TESTS = [((4, [[0, 1], [1, 2], [2, 0], [1, 3]]), [[1, 3]]), ((2, [[0, 1]]), [[0, 1]]), ((3, [[0, 1], [1, 2], [2, 0]]), [])] + _cases()
