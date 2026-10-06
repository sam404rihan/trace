def min_cost_cut_stick(n: int, cuts: list[int]) -> int:
    points = [0] + sorted(cuts) + [n]
    m = len(points)
    cost = [[0] * m for _ in range(m)]      # cost[i][j]: every cut strictly inside points[i]..points[j]
    for gap in range(2, m):                 # shorter intervals first
        for i in range(m - gap):
            j = i + gap
            best_split = min(cost[i][k] + cost[k][j] for k in range(i + 1, j))   # k is cut first
            cost[i][j] = points[j] - points[i] + best_split
    return cost[0][m - 1]
