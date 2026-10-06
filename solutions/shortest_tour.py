def shortest_tour(dist: list[list[int]]) -> int:
    n = len(dist)
    if n == 1:
        return 0
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]     # dp[mask][last]: visited `mask`, standing at `last`
    dp[1][0] = 0
    for mask in range(1 << n):                  # smaller masks first: their supersets come later
        row = dp[mask]
        for last in range(n):
            cost = row[last]
            if cost == INF:
                continue
            for nxt in range(n):
                if not mask >> nxt & 1:
                    new = mask | 1 << nxt
                    if cost + dist[last][nxt] < dp[new][nxt]:
                        dp[new][nxt] = cost + dist[last][nxt]
    full = (1 << n) - 1
    return min(dp[full][last] + dist[last][0] for last in range(1, n))
