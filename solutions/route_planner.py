import heapq


def route_planner(roads: list[tuple[str, str, int]], start: str, end: str) -> tuple[int, list[str]]:
    adj = {}
    for a, b, w in roads:                       # two-way roads
        adj.setdefault(a, []).append((b, w))
        adj.setdefault(b, []).append((a, w))

    dist, prev = {start: 0}, {}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == end:
            route = [end]
            while route[-1] != start:           # walk the breadcrumbs back to the start
                route.append(prev[route[-1]])
            return d, route[::-1]
        if d > dist[u]:
            continue
        for v, w in adj.get(u, []):
            if d + w < dist.get(v, float("inf")):
                dist[v] = d + w
                prev[v] = u                     # best known way into v is via u
                heapq.heappush(pq, (d + w, v))
    return -1, []
