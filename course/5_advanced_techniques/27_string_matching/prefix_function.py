"""
Prefix function                                                             [snippet]

For each i, pi[i] is the length of the longest PROPER prefix of s[:i+1] that is
also a suffix of s[:i+1]. ("Proper" means not the whole thing.) Return pi.

Example:
    prefix_function("abacaba")  ->  [0, 0, 1, 0, 1, 2, 3]
    prefix_function("aaaa")     ->  [0, 1, 2, 3]

Aim for:  O(n). k (the current border length) goes up by at most 1 per step, so all the
          fall-backs together are O(n) too.
Hint:     k = 0. For i from 1: while k > 0 and s[i] != s[k]: k = pi[k - 1].
          If s[i] == s[k]: k += 1. Then pi[i] = k.
"""


def prefix_function(s: str) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    out = []
    for i in range(len(s)):
        t = s[:i + 1]
        out.append(max((L for L in range(len(t)) if t[:L] == t[len(t) - L:]), default=0))
    return out


def _cases():
    import random
    rng = random.Random(211)
    return [((s,), _brute(s)) for s in ("".join(rng.choice("ab") for _ in range(rng.randint(1, 18))) for _ in range(10))]


TEACHES = ["str.prefix_function"]
USES = []

TESTS = [(("abacaba",), [0, 0, 1, 0, 1, 2, 3]), (("aaaa",), [0, 1, 2, 3]), (("abcd",), [0, 0, 0, 0]), (("",), []),
         (("aabaaab",), [0, 1, 0, 1, 2, 2, 3])] + _cases()
