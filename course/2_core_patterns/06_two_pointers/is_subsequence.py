"""
Is It a Subsequence?                                                          [easy]

Return True if t is a subsequence of s: t's letters appear in s in the same
order, though not necessarily next to each other.

Example:
    is_subsequence("abcde", "ace")  ->  True
    is_subsequence("abcde", "aec")  ->  False      the c comes before the e in s

Aim for:  O(len(s) + len(t)). The last tests have 1,500,000 letters in s: cutting s
          down with slices after every match copies it again and again, and
          times out.
Hint:     Keep i in t and j in s. Every step moves j on; i moves on only when
          t[i] == s[j]. t is a subsequence if i reaches the end of t.
"""


def is_subsequence(s: str, t: str) -> bool:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["pointers.two_sequences"]
USES = []

TESTS = [
    (("abcde", "ace"), True),
    (("abcde", "aec"), False),
    (("abc", ""), True),
    (("", "a"), False),
    (("", ""), True),
    (("aaa", "aaaa"), False),
    (("axbxc", "abc"), True),
    (("abc", "abc"), True),
    (("ab" * 750_000, "ab" * 250_000), True),
    (("ab" * 750_000, "ab" * 250_000 + "c"), False),
]
