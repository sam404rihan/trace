"""
Regular Expression Matching                                                     [hard]

Implement matching for patterns that use "." (any one character) and "*"
(zero or more of the PRECEDING element). The match must cover the whole string.
Every "*" in a pattern follows a letter or ".".

Example:
    regex_matching("aa", "a")      ->  False
    regex_matching("aa", "a*")     ->  True
    regex_matching("ab", ".*")     ->  True
    regex_matching("aab", "c*a*b") ->  True

Aim for:  O(len(s) · len(p)) DP. (Don't just call Python's re module!)
Hint:     dp[i][j] = does s[i:] match p[j:]? If p[j+1] is "*": skip "x*" (dp[i][j+2]) OR, if the first
          characters match, consume one character of s and stay on the star (dp[i+1][j]).
          Otherwise: first characters match and dp[i+1][j+1].
"""


def regex_matching(s: str, p: str) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(s, p):
    import re as _re
    return _re.fullmatch(p, s) is not None


def _make(rng):
    s = "".join(rng.choice("ab") for _ in range(rng.randint(0, 6)))
    p = ""
    for _ in range(rng.randint(0, 5)):
        p += rng.choice("ab.")
        if rng.random() < 0.4:
            p += "*"
    return (s, p)


def _cases():
    import random
    rng = random.Random(114)
    out = []
    for _ in range(16):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


TESTS = [(("aa", "a"), False), (("aa", "a*"), True), (("ab", ".*"), True), (("aab", "c*a*b"), True),
         (("mississippi", "mis*is*p*."), False), (("", "a*b*"), True)] + _cases()
