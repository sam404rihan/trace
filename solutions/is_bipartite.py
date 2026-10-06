def is_bipartite(graph: list[list[int]]) -> bool:
    color = [-1] * len(graph)
    for start in range(len(graph)):             # the graph may be in several pieces
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            v = queue.popleft()
            for u in graph[v]:
                if color[u] == -1:
                    color[u] = 1 - color[v]     # opposite side
                    queue.append(u)
                elif color[u] == color[v]:
                    return False                # an odd cycle
    return True
