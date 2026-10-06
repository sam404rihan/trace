def min_weighted_subgraph(n: int, edges: list[list[int]], src1: int, src2: int, dest: int) -> int:
    forward = [[] for _ in range(n)]
    backward = [[] for _ in range(n)]
    for a, b, w in edges:
        forward[a].append((b, w))
        backward[b].append((a, w))      # reversed: distances TO dest

    def dijkstra(graph, source):
        dist = [inf] * n
        dist[source] = 0
        heap = [(0, source)]
        while heap:
            d, u = heappop(heap)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heappush(heap, (dist[v], v))
        return dist

    from1, from2 = dijkstra(forward, src1), dijkstra(forward, src2)
    to_dest = dijkstra(backward, dest)
    # The two paths meet at some node m and share the rest: a "Y" shape.
    best = min(from1[m] + from2[m] + to_dest[m] for m in range(n))
    return -1 if best == inf else best
