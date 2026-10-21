"""
Fill one LCS cell                                                           [snippet]

In the longest-common-subsequence table, dp[i][j] is the LCS length of the
first i letters of `a` and the first j letters of `b`. Everything above and to
the left of (i, j) is already filled. Return the value for dp[i][j] (i, j ≥ 1).

Example:
    a = "AB", b = "B"
    dp = [[0, 0],
          [0, 0],
          [0, ?]]
    lcs_cell(dp, "AB", "B", 2, 1)  ->  1      a[1] == b[0] == "B": diagonal + 1

Hint:     If a[i - 1] == b[j - 1], the letters pair up: dp[i - 1][j - 1] + 1.
          Otherwise drop one letter from one word: max(dp[i - 1][j], dp[i][j - 1]).
"""


def lcs_cell(dp: list[list[int]], a: str, b: str, i: int, j: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["dp.two_strings"]
USES = []

TESTS = [
    (([[0, 0], [0, 0], [0, 0]], "AB", "B", 2, 1), 1),
    (([[0, 0, 0], [0, 1, 1], [0, 1, 0]], "AC", "AB", 2, 2), 1),
    (([[0, 0, 0], [0, 0, 1], [0, 1, 0]], "BA", "AB", 2, 2), 1),
    (([[0, 0, 0], [0, 1, 1], [0, 1, 0]], "AB", "AB", 2, 2), 2),
]
