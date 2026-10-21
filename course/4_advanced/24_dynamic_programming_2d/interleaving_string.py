"""
Interleaving String                                                           [medium]

Can s3 be formed by interleaving s1 and s2, keeping each one's letters in
their original order?

Example:
    interleaving_string("aabcc", "dbbca", "aadbbcbcac")  ->  True
    interleaving_string("aabcc", "dbbca", "aadbbbaccc")  ->  False

Aim for:  O(len(s1) · len(s2)).
Hint:     dp[i][j] = can the first i letters of s1 and the first j of s2 make the first i + j of s3?
          dp[i][j] = (dp[i-1][j] and s1[i-1] == s3[i+j-1]) or (dp[i][j-1] and s2[j-1] == s3[i+j-1]).
"""


def interleaving_string(s1: str, s2: str, s3: str) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False
    if not s3:
        return True
    return (bool(s1) and s1[0] == s3[0] and _brute(s1[1:], s2, s3[1:])) or \
           (bool(s2) and s2[0] == s3[0] and _brute(s1, s2[1:], s3[1:]))


def _make(rng):
    a = "".join(rng.choice("ab") for _ in range(rng.randint(0, 5)))
    b = "".join(rng.choice("ab") for _ in range(rng.randint(0, 5)))
    c = list(a + b)
    if rng.random() < 0.5:
        rng.shuffle(c)
    return (a, b, "".join(c))


def _cases():
    import random
    rng = random.Random(110)
    out = []
    for _ in range(12):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


USES = ["dp.two_strings"]

TESTS = [(("aabcc", "dbbca", "aadbbcbcac"), True), (("aabcc", "dbbca", "aadbbbaccc"), False), (("", "", ""), True),
         (("a", "", "a"), True), (("ab", "c", "abcd"), False)] + _cases()
