def min_cost_flow(n: int, edges: list[tuple[int, int, int, int]], s: int, t: int) -> list[int]:
    to, cap, cost = [], [], []          # edge e's reverse is e ^ 1: they're added in pairs
    out = [[] for _ in range(n)]

    def add(u, v, c, w):
        out[u].append(len(to))
        to.append(v)
        cap.append(c)
        cost.append(w)

    for u, v, c, w in edges:
        add(u, v, c, w)
        add(v, u, 0, -w)                # the refund edge: sending flow back gives the cost back

    flow = total = 0
    while True:
        dist = [inf] * n                # SPFA: Bellman-Ford with a queue (negative refunds are fine)
        via = [-1] * n                  # the edge used to reach each node
        dist[s] = 0
        queue, queued = deque([s]), [False] * n
        queued[s] = True
        while queue:
            u = queue.popleft()
            queued[u] = False
            for e in out[u]:
                v = to[e]
                if cap[e] > 0 and dist[u] + cost[e] < dist[v]:
                    dist[v] = dist[u] + cost[e]
                    via[v] = e
                    if not queued[v]:
                        queued[v] = True
                        queue.append(v)
        if dist[t] == inf:
            return [flow, total]
        push, v = inf, t                # bottleneck along the cheapest path
        while v != s:
            push = min(push, cap[via[v]])
            v = to[via[v] ^ 1]
        v = t
        while v != s:
            cap[via[v]] -= push
            cap[via[v] ^ 1] += push
            v = to[via[v] ^ 1]
        flow += push
        total += push * dist[t]
