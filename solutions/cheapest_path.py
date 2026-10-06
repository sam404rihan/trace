import heapq


def cheapest_path(n: int, edges: list[tuple[int, int, int]], src: int, dst: int) -> int:
    adj = [[] for _ in range(n)]
    for a, b, w in edges:
        adj[a].append((b, w))
    dist = [float("inf")] * n
    dist[src] = 0
    pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == dst:
            return d                    # the first time dst is popped, its distance is final
        if d > dist[u]:
            continue                    # stale entry: u was already settled more cheaply
        for v, w in adj[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(pq, (dist[v], v))
    return -1
