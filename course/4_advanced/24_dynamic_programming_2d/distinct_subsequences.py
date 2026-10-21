"""
Distinct Subsequences                                                           [hard]

Count how many different ways t appears as a subsequence of s (delete any
letters of s, keep the order). Ways that use different positions of s count
separately.

Example:
    distinct_subsequences("rabbbit", "rabbit")  ->  3      choose which of the three b's to drop
    distinct_subsequences("babgbag", "bag")     ->  5

Aim for:  O(len(s) · len(t)).
Hint:     dp[i][j] = ways for s[:i] to form t[:j]. Each s[i-1] can be skipped (dp[i-1][j]) or,
          if it equals t[j-1], used (+ dp[i-1][j-1]). dp[i][0] = 1. One row, updated with j
          descending, is enough.
"""


def distinct_subsequences(s: str, t: str) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(s, t):
    from itertools import combinations as comb
    return sum(1 for idx in comb(range(len(s)), len(t)) if all(s[i] == t[k] for k, i in enumerate(idx)))


def _make(rng):
    return ("".join(rng.choice("ab") for _ in range(rng.randint(0, 12))), "".join(rng.choice("ab") for _ in range(rng.randint(0, 4))))


def _cases():
    import random
    rng = random.Random(112)
    out = []
    for _ in range(10):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


USES = ["dp.two_strings"]

TESTS = [(("rabbbit", "rabbit"), 3), (("babgbag", "bag"), 5), (("abc", ""), 1), (("", "a"), 0), (("aaaa", "aa"), 6)] + _cases()
