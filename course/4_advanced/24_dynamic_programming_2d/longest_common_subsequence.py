"""
Longest Common Subsequence                                [medium] · dynamic programming

Return the length of the longest sequence of characters that appears, in
order but not necessarily side by side, in both `a` and `b`.

Example:
    longest_common_subsequence("abcde", "ace")  ->  3      "ace"

Aim for:  O(len(a) · len(b)) time
Hint:     Build a 2D table where dp[i][j] = answer for a[:i] and b[:j].
          If a[i-1] == b[j-1], extend the diagonal: dp[i-1][j-1] + 1.
          Otherwise, drop a character from one side: max(dp[i-1][j], dp[i][j-1]).
          Draw the table on paper for "abcde" / "ace" first!
"""


def longest_common_subsequence(a: str, b: str) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["dp.two_strings"]

TESTS = [
    (("abcde", "ace"), 3),
    (("abc", "abc"), 3),
    (("abc", "def"), 0),
    (("", "a"), 0),
    (("AGGTAB", "GXTXAYB"), 4),
]
