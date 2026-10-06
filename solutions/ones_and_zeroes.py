def ones_and_zeroes(strs: list[str], m: int, n: int) -> int:
    dp = [[0] * (n + 1) for _ in range(m + 1)]   # dp[z][o]: most strings within z zeros and o ones
    for s in strs:
        a, b = s.count("0"), s.count("1")
        for z in range(m, a - 1, -1):             # downwards: each string used at most once
            for o in range(n, b - 1, -1):
                dp[z][o] = max(dp[z][o], dp[z - a][o - b] + 1)
    return dp[m][n]
