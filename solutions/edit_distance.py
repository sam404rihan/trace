def edit_distance(a: str, b: str) -> int:
    # dp[i][j] = edits to turn a[:i] into b[:j]. O(len(a) · len(b)).
    rows, cols = len(a) + 1, len(b) + 1
    dp = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        dp[i][0] = i                     # delete all i characters
    for j in range(cols):
        dp[0][j] = j                     # insert all j characters
    for i in range(1, rows):
        for j in range(1, cols):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]              # free: characters match
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],         # delete a[i-1]
                                   dp[i][j - 1],         # insert b[j-1]
                                   dp[i - 1][j - 1])     # replace
    return dp[-1][-1]
