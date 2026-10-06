def lcs_cell(dp: list[list[int]], a: str, b: str, i: int, j: int) -> int:
    if a[i - 1] == b[j - 1]:
        return dp[i - 1][j - 1] + 1                 # pair the two letters up
    return max(dp[i - 1][j], dp[i][j - 1])          # drop a letter from one of the words
