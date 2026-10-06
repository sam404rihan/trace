def diff_lines(old: list[str], new: list[str]) -> list[str]:
    n, m = len(old), len(new)
    # dp[i][j] = LCS of the SUFFIXES old[i:] and new[j:], so we can walk forwards from (0, 0).
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if old[i] == new[j]:
                dp[i][j] = dp[i + 1][j + 1] + 1
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])

    out, i, j = [], 0, 0
    while i < n or j < m:
        if i < n and j < m and old[i] == new[j]:
            out.append("  " + old[i])               # part of the LCS: keep it
            i, j = i + 1, j + 1
        elif j == m or (i < n and dp[i + 1][j] >= dp[i][j + 1]):
            out.append("- " + old[i])               # dropping the old line loses nothing
            i += 1
        else:
            out.append("+ " + new[j])
            j += 1
    return out
