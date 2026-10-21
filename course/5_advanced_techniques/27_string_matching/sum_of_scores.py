"""
Sum of Scores of Built Strings                                                [hard]

The "score" of a suffix of `s` is the length of the longest common prefix of
that suffix and `s` itself. Return the sum of the scores of ALL suffixes
(including s itself, which scores len(s)).

Example:
    sum_of_scores("babab")       ->  9
        suffixes "b", "ab", "bab", "abab", "babab" score 1, 0, 3, 0, 5.
    sum_of_scores("azbazbzaz")   ->  14

Aim for:  O(n) with the Z-function. Comparing each suffix character by character is O(n²):
          too slow for "aaaa...a" with 100,000 letters.
Hint:     z[i] = length of the longest common prefix of s and s[i:]. The Z-algorithm keeps the
          rightmost window [l, r) that matches a prefix of s. For i inside it, start from
          min(r - i, z[i - l]) (already known to match) and only extend past r by comparing.
          The answer is n + sum(z[1:]).
"""


def sum_of_scores(s: str) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    total = 0
    for i in range(len(s)):
        k = 0
        while i + k < len(s) and s[k] == s[i + k]:
            k += 1
        total += k
    return total


def _cases():
    import random
    rng = random.Random(2223)
    out = []
    for _ in range(10):
        s = "".join(rng.choice("ab") for _ in range(rng.randint(1, 20)))
        out.append(((s,), _brute(s)))
    n = 100_000
    out.append((("a" * n,), n * (n + 1) // 2))
    out.append((("ab" * (n // 2),), sum(n - 2 * k for k in range(n // 2))))
    return out


USES = []

TESTS = [
    (("babab",), 9),
    (("azbazbzaz",), 14),
    (("a",), 1),
    (("ab",), 2),
    (("aaa",), 6),
] + _cases()
