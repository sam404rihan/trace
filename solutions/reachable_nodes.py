from collections import deque


def reachable_nodes(n: int, edges: list[tuple[int, int]], start: int) -> list[int]:
    graph = [[] for _ in range(n)]
    for a, b in edges:                      # undirected: each edge goes both ways
        graph[a].append(b)
        graph[b].append(a)
    seen, queue = {start}, deque([start])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return sorted(seen)
