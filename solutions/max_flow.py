def max_flow(n: int, edges: list[tuple[int, int, int]], s: int, t: int) -> int:
    cap = [dict() for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] = cap[u].get(v, 0) + c        # parallel edges add up
        cap[v].setdefault(u, 0)                 # reverse edge, empty for now
    flow = 0
    while True:
        prev = {s: None}
        q = deque([s])
        while q and t not in prev:              # BFS: the augmenting path with the fewest edges
            u = q.popleft()
            for v, c in cap[u].items():
                if c > 0 and v not in prev:
                    prev[v] = u
                    q.append(v)
        if t not in prev:
            return flow
        path, v = [], t
        while v != s:
            path.append((prev[v], v))
            v = prev[v]
        push = min(cap[u][v] for u, v in path)
        for u, v in path:
            cap[u][v] -= push
            cap[v][u] += push                   # so a later path can undo this
        flow += push
