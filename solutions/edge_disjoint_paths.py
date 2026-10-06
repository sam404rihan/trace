def edge_disjoint_paths(n: int, links: list[tuple[int, int]], s: int, t: int) -> int:
    cap = [dict() for _ in range(n)]
    for u, v in links:
        cap[u][v] = cap[u].get(v, 0) + 1        # each cable carries one route
        cap[v].setdefault(u, 0)
    routes = 0
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
            return routes
        v = t
        while v != s:
            u = prev[v]
            cap[u][v] -= 1
            cap[v][u] += 1
            v = u
        routes += 1
