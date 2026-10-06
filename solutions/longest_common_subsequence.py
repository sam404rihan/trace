def longest_common_subsequence(a: str, b: str) -> int:
    # dp[i][j] = LCS length of a[:i] and b[:j]. O(len(a) · len(b)).
    dp = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1          # extend the match
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])  # skip a char on one side
    return dp[-1][-1]

    # Space trick: each row only needs the previous row, so O(len(b)) space works.
