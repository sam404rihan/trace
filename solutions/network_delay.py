import heapq
from collections import defaultdict


def network_delay(times: list[list[int]], n: int, k: int) -> int:
    # Dijkstra from k; the answer is when the LAST computer hears. O(E log V).
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist = {k: 0}
    heap = [(0, k)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue                     # stale entry
        for nxt, w in graph[node]:
            if d + w < dist.get(nxt, float("inf")):
                dist[nxt] = d + w
                heapq.heappush(heap, (d + w, nxt))
    return max(dist.values()) if len(dist) == n else -1
