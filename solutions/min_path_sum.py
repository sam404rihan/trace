def min_path_sum(grid: list[list[int]]) -> int:
    cols = len(grid[0])
    dp = [float("inf")] * cols      # one row of the table is enough
    dp[0] = 0
    for row in grid:
        for c in range(cols):
            left = dp[c - 1] if c else float("inf")
            dp[c] = row[c] + min(dp[c], left)   # dp[c] still holds the cell above
    return dp[-1]
