def city_fewest_reachable(n: int, edges: list[list[int]], threshold: int) -> int:
    INF = float("inf")
    d = [[0 if i == j else INF for j in range(n)] for i in range(n)]
    for a, b, w in edges:
        if w < d[a][b]:
            d[a][b] = d[b][a] = w
    for k in range(n):                          # Floyd–Warshall
        dk = d[k]
        for i in range(n):
            via = d[i][k]
            if via == INF:
                continue
            di = d[i]
            for j in range(n):
                if via + dk[j] < di[j]:
                    di[j] = via + dk[j]
    best_city, best_count = -1, INF
    for i in range(n):
        count = sum(1 for j in range(n) if j != i and d[i][j] <= threshold)
        if count <= best_count:                 # "<=" lets a later (larger) city win ties
            best_city, best_count = i, count
    return best_city
