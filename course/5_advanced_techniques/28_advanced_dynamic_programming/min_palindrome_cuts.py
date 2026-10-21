"""
Palindrome Partitioning II                                                      [hard]

Cut s into pieces that are all palindromes, using as few cuts as possible.
Return that minimum number of cuts.

Example:
    min_palindrome_cuts("aab")   ->  1        "aa" | "b"
    min_palindrome_cuts("abba")  ->  0

Aim for:  O(n²). The last test has 2,000 characters.
Hint:     Precompute is_pal[i][j] (s[i..j] is a palindrome when s[i] == s[j] and the inside is too).
          Then cuts[j] = 0 if s[0..j] is a palindrome, else the min over i of cuts[i-1] + 1 for each
          palindromic s[i..j].
"""


def min_palindrome_cuts(s: str) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    from functools import lru_cache as memo

    @memo(None)
    def go(i):
        if i == len(s):
            return -1
        return min(1 + go(j) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
    return go(0)


def _fast(s):
    n = len(s)
    pal = [[False] * n for _ in range(n)]
    cuts = [0] * n
    for j in range(n):
        best = j
        for i in range(j + 1):
            if s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1]):
                pal[i][j] = True
                best = 0 if i == 0 else min(best, cuts[i - 1] + 1)
        cuts[j] = best
    return cuts[-1] if n else 0


def _cases():
    import random
    rng = random.Random(307)
    out = [((s,), _brute(s)) for s in ("".join(rng.choice("ab") for _ in range(rng.randint(1, 16))) for _ in range(8))]
    big = "".join(rng.choice("abc") for _ in range(2000))
    out.append(((big,), _fast(big)))
    return out


USES = ["dp.prefix", "dp.interval"]

TESTS = [(("aab",), 1), (("abba",), 0), (("a",), 0), (("ab",), 1), (("abcde",), 4)] + _cases()
