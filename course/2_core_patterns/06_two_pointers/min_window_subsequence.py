"""
Minimum Window Subsequence                                                    [hard]

Return the shortest substring of `s` that contains `t` as a SUBSEQUENCE (t's
letters appear in order, not necessarily next to each other). If several are
equally short, return the leftmost. If there's none, return "".

Example:
    min_window_subsequence("abcdebdde", "bde")   ->  "bcde"
        "bdde" is just as short but starts later.
    min_window_subsequence("jmeqksfrsdcmsiwvaovztaqenprpvnbstl", "u")  ->  ""

Aim for:  O(len(s) * len(t)) with two pointers, no extra memory.
Hint:     Scan forward matching t's letters in order. When the last one matches at index end,
          walk BACKWARDS from end matching t from its last letter to its first: that finds the
          latest possible start, so [start, end] is the shortest window ending there. Record it,
          then resume the forward scan from start + 1.
"""


def min_window_subsequence(s: str, t: str) -> str:
    raise NotImplementedError  # replace this line with your solution


def _brute(s, t):
    best = ""
    for i in range(len(s)):
        k = 0
        for j in range(i, len(s)):
            if s[j] == t[k]:
                k += 1
                if k == len(t):
                    if not best or j - i + 1 < len(best):
                        best = s[i:j + 1]
                    break
    return best


def _cases():
    import random
    rng = random.Random(727)
    out = []
    for _ in range(10):
        s = "".join(rng.choice("abc") for _ in range(rng.randint(1, 18)))
        t = "".join(rng.choice("abc") for _ in range(rng.randint(1, 4)))
        out.append(((s, t), _brute(s, t)))
    s = "".join(rng.choice("ab") for _ in range(20_000)) + "xyz"
    out.append(((s, "abxyz"), _brute(s[-200:], "abxyz")))
    return out


TESTS = [
    (("abcdebdde", "bde"), "bcde"),
    (("jmeqksfrsdcmsiwvaovztaqenprpvnbstl", "u"), ""),
    (("abc", "abc"), "abc"),
    (("aaa", "aa"), "aa"),
    (("ab", "ba"), ""),
    (("fgrqsqsnodwmxzkzxwqegkndaa", "kzed"), "kzxwqegknd"),
] + _cases()
