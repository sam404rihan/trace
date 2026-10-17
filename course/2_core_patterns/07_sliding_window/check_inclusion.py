"""
Permutation in String                                                         [medium]

Return True if some rearrangement of s1 appears as a contiguous substring of s2.

Example:
    check_inclusion("ab", "eidbaooo")  ->  True       "ba"
    check_inclusion("ab", "eidboaoo")  ->  False

Aim for:  O(len(s2)), fixed-size window.
Hint:     Slide a window of length len(s1) across s2, keeping letter counts for the window.
          Compare them with s1's counts at every step (26 letters is a constant).
"""


def check_inclusion(s1: str, s2: str) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(a, b):
    return any(sorted(b[i:i + len(a)]) == sorted(a) for i in range(len(b) - len(a) + 1))


def _cases():
    import random
    rng = random.Random(50)
    out = []
    for _ in range(8):
        a = "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
        b = "".join(rng.choice("abcd") for _ in range(rng.randint(0, 14)))
        out.append(((a, b), _brute(a, b)))
    return out


USES = ["window.fixed"]

TESTS = [(("ab", "eidbaooo"), True), (("ab", "eidboaoo"), False), (("abc", "ab"), False), (("a", "a"), True),
         (("adc", "dcda"), True)] + _cases()
