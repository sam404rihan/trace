def floyd_step(dist, k):
    n = len(dist)
    for i in range(n):
        via = dist[i][k]                    # cost to reach the stopover from i
        if via == float("inf"):
            continue
        row, krow = dist[i], dist[k]
        for j in range(n):
            if via + krow[j] < row[j]:
                row[j] = via + krow[j]
    return dist
