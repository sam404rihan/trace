def tree_diameter(n: int, edges: list[tuple[int, int]]) -> int:
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    def farthest(src):
        dist = [-1] * n
        dist[src] = 0
        order = [src]
        for v in order:
            for w in adj[v]:
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    order.append(w)
        return order[-1], dist[order[-1]]       # BFS visits by distance, so the last node is a farthest one

    end, _ = farthest(0)
    return farthest(end)[1]
