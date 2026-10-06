"""
Decode Ways II                                                                [hard]

Letters are encoded as numbers: "A" -> "1", "B" -> "2", ..., "Z" -> "26".
The message `s` holds digits and "*", where "*" stands for any digit 1-9
(never 0). Count the ways to decode the whole message, modulo 1_000_000_007.
A group can't start with 0: "06" is not a valid code for "F".

Example:
    decode_ways_ii("*")     ->  9        "A" through "I"
    decode_ways_ii("1*")    ->  18       "11".."19" as one letter (9) or two letters (9)
    decode_ways_ii("2*")    ->  15
    decode_ways_ii("**")    ->  96

Aim for:  O(n) time, O(1) space.
Hint:     Same DP as Decode Ways: ways[i] = (ways to decode s[i-1] alone) * ways[i-1]
          + (ways to decode s[i-2:i] as one letter) * ways[i-2]. The only new part is counting
          how many letters each one- or two-character group can be when it has stars:
          "*" -> 9; "**" -> 15 (11-19 and 21-26); "1*" -> 9; "2*" -> 6; "*d" -> 2 if d <= 6 else 1.
"""

MOD = 1_000_000_007


def decode_ways_ii(s: str) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    """Expand every star, then count with the plain Decode Ways DP."""
    from itertools import product
    stars = [i for i, ch in enumerate(s) if ch == "*"]
    total = 0
    for digits in product("123456789", repeat=len(stars)):
        t = list(s)
        for i, d in zip(stars, digits):
            t[i] = d
        prev, cur = 1, 1 if t[0] != "0" else 0
        for i in range(1, len(t)):
            nxt = (cur if t[i] != "0" else 0) + (prev if 10 <= int(t[i - 1] + t[i]) <= 26 else 0)
            prev, cur = cur, nxt
        total += cur
    return total % MOD


def _fast(s):
    def one(c):
        return 9 if c == "*" else (0 if c == "0" else 1)

    def two(a, b):
        if a == "*" and b == "*":
            return 15
        if a == "*":
            return 2 if b <= "6" else 1
        if b == "*":
            return 9 if a == "1" else 6 if a == "2" else 0
        return 1 if 10 <= int(a + b) <= 26 else 0
    prev, cur = 1, one(s[0])
    for i in range(1, len(s)):
        prev, cur = cur, (one(s[i]) * cur + two(s[i - 1], s[i]) * prev) % MOD
    return cur


def _cases():
    import random
    rng = random.Random(639)
    out = []
    for _ in range(10):
        s = "".join(rng.choice("0123456*1*2*") for _ in range(rng.randint(1, 4)))
        out.append(((s,), _brute(s)))
    big = "".join(rng.choice("123*0*12*7*") for _ in range(100_000))
    out.append(((big,), _fast(big)))
    return out


TESTS = [
    (("*",), 9),
    (("1*",), 18),
    (("2*",), 15),
    (("**",), 96),
    (("0",), 0),
    (("*0",), 2),
    (("*1*1*0",), 404),
    (("7*9*3*6*3*0*5*4*9*7*3*7*1*8*3*2*0*0*6*",), 196465252),
] + _cases()
