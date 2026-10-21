"""
Longest Happy Prefix                                                          [easy]

A "happy prefix" is a non-empty prefix of s that is also a suffix, but isn't
the whole string. Return the longest one, or "".

Example:
    longest_happy_prefix("level")     ->  "l"
    longest_happy_prefix("ababab")    ->  "abab"

Aim for:  O(n). The last test has 200,000 characters.
Hint:     It's exactly the last value of the prefix function: s[:pi[-1]].
"""


def longest_happy_prefix(s: str) -> str:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    return next((s[:L] for L in range(len(s) - 1, 0, -1) if s[:L] == s[-L:]), "")


def _fast(s):
    pi, k = [0] * len(s), 0
    for i in range(1, len(s)):
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return s[:pi[-1]] if s else ""


def _cases():
    import random
    rng = random.Random(216)
    out = [((s,), _brute(s)) for s in ("".join(rng.choice("ab") for _ in range(rng.randint(1, 16))) for _ in range(8))]
    big = "ab" * 100_000
    out.append(((big,), _fast(big)))
    return out


USES = ["str.prefix_function"]

TESTS = [(("level",), "l"), (("ababab",), "abab"), (("a",), ""), (("abc",), "")] + _cases()
