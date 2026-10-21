"""
Longest Palindromic Substring                                                 [medium]

Return a longest substring of s that reads the same forwards and backwards.
If several are equally long, any of them is accepted.

Example:
    longest_palindrome_substring("babad")  ->  "bab"   (or "aba")
    longest_palindrome_substring("cbbd")   ->  "bb"

Aim for:  O(n²) time, O(1) space.
Hint:     Expand around every centre: there are 2n - 1 of them (each letter, and each gap between
          two letters). From a centre, grow outwards while both ends match.
"""


def longest_palindrome_substring(s: str) -> str:
    raise NotImplementedError  # replace this line with your solution


def _best_len(s):
    return max((j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1]), default=0)


def CHECK(got, expected, args):
    s = args[0]
    return isinstance(got, str) and got in s and got == got[::-1] and len(got) == _best_len(s)


def _describe(s):
    return f"any palindrome of length {_best_len(s)}"


def _cases():
    import random
    rng = random.Random(103)
    return [((s,), _describe(s)) for s in ("".join(rng.choice("ab") for _ in range(rng.randint(1, 20))) for _ in range(8))]


USES = ["palin.expand"]

TESTS = [((s,), _describe(s)) for s in ("babad", "cbbd", "a", "racecarxyz", "abcd", "aaaa", "forgeeksskeegfor")] + _cases()
