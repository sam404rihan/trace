"""
Fast modular power                                                          [snippet]

Return base ** exp % mod without computing the giant number base ** exp.
Use repeated squaring: walk the bits of exp from the lowest one. Keep a running
square of the base, and multiply it into the result whenever the bit is 1.

Example:
    mod_pow(3, 13, 7)  ->  3        3^13 = 3^8 · 3^4 · 3^1   (13 is 1101 in binary)
    mod_pow(2, 10, 1000)  ->  24    1024 % 1000

Hint:     result = 1; base %= mod
          while exp: if exp & 1: result = result * base % mod
                     base = base * base % mod; exp >>= 1
          Python's pow(base, exp, mod) does exactly this. Write it once yourself.
"""


def mod_pow(base: int, exp: int, mod: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _cases():
    import random
    rng = random.Random(3001)
    out = []
    for _ in range(6):
        b, e, m = rng.randint(0, 10**9), rng.randint(0, 10**18), rng.randint(2, 10**9 + 7)
        out.append(((b, e, m), pow(b, e, m)))
    return out


TESTS = [((3, 13, 7), 3), ((2, 10, 1000), 24), ((5, 0, 13), 1), ((0, 5, 7), 0), ((10, 3, 1), 0),
         ((7, 10**18, 1_000_000_007), pow(7, 10**18, 1_000_000_007))] + _cases()
