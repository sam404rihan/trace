"""
Extended Euclid                                                               [medium]

Return (g, x, y) where g = gcd(a, b) and a·x + b·y = g. Many (x, y) pairs work;
any of them is accepted.

This is how you divide modulo m: if gcd(b, m) == 1, then b·x + m·y = 1, so
b·x ≡ 1 (mod m) and x is the inverse of b.

Example:
    extended_gcd(30, 18)  ->  (6, -1, 2)       30·(-1) + 18·2 = 6
    extended_gcd(7, 0)    ->  (7, 1, 0)

Aim for:  O(log min(a, b)).
Hint:     Same recursion as gcd. If b == 0 return (a, 1, 0). Otherwise get (g, x1, y1) for
          (b, a % b). Since a % b = a - (a // b)·b, the answer is (g, y1, x1 - (a // b)·y1).
"""
from math import gcd


def extended_gcd(a: int, b: int) -> tuple[int, int, int]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected, args):
    a, b = args
    try:
        g, x, y = got
    except (TypeError, ValueError):
        return False
    return g == expected and a * x + b * y == g


def _cases():
    import random
    rng = random.Random(3005)
    pairs = [(rng.randint(0, 10**18), rng.randint(0, 10**18)) for _ in range(8)]
    for _ in range(3):
        k = rng.randint(1, 10**6)
        pairs.append((k * rng.randint(1, 10**9), k * rng.randint(1, 10**9)))
    return [((a, b), gcd(a, b)) for a, b in pairs]


TESTS = [((30, 18), 6), ((7, 0), 7), ((0, 9), 9), ((1, 1), 1), ((240, 46), 2), ((17, 5), 1),
         ((832_040, 514_229), 1)] + _cases()
