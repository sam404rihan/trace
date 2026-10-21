"""
Edit Distance                                                                 [hard]

Return the minimum number of single-character edits (insert, delete or
replace a character) that turn `a` into `b`.

Example:
    edit_distance("horse", "ros")  ->  3
        horse -> rorse (replace h with r) -> rose (delete r) -> ros (delete e)

Aim for:  O(len(a) · len(b))
Hint:     dp[i][j] = edits to turn a[:i] into b[:j]. Base cases: dp[i][0] = i,
          dp[0][j] = j. If the last characters match, dp[i-1][j-1]; otherwise
          1 + min(delete dp[i-1][j], insert dp[i][j-1], replace dp[i-1][j-1]).
          The lesson prints this exact table.
"""


def edit_distance(a: str, b: str) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["dp.two_strings"]

TESTS = [
    (("horse", "ros"), 3),
    (("intention", "execution"), 5),
    (("", "abc"), 3),
    (("abc", "abc"), 0),
    (("kitten", "sitting"), 3),
]
