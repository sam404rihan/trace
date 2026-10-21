def matrix_chain(dims: list[int]) -> int:
    # Interval DP: the best way to multiply matrices i..j tries every place for the last split.
    n = len(dims) - 1
    cost = [[0] * n for _ in range(n)]          # cost[i][j]: matrices i..j; one matrix costs 0
    for length in range(2, n + 1):              # shorter runs first, so the parts are ready
        for i in range(n - length + 1):
            j = i + length - 1
            cost[i][j] = min(cost[i][k] + cost[k + 1][j] + dims[i] * dims[k + 1] * dims[j + 1]
                             for k in range(i, j))
    return cost[0][n - 1]
