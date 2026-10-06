def burst_balloons(nums: list[int]) -> int:
    vals = [1] + nums + [1]
    n = len(vals)
    dp = [[0] * n for _ in range(n)]            # dp[l][r]: best for the balloons strictly between l and r
    for width in range(2, n):
        for l in range(n - width):
            r = l + width
            dp[l][r] = max(dp[l][k] + vals[l] * vals[k] * vals[r] + dp[k][r] for k in range(l + 1, r))
    return dp[0][n - 1]
