"""
Fast Power                                                                  [medium]

Return x raised to the power n, for an integer x and n >= 0.
Don't use ** or pow().

Example:
    power(2, 10)  ->  1024

Aim for:  O(log n). The last tests use n = 1,000,000,000: multiplying n times
          is far too slow, and recursing n levels deep crashes.
Hint:     x^n = (x^(n//2))² when n is even, and x * x^(n-1) when n is odd.
          Compute half = power(x, n // 2) ONCE and square it.
"""


def power(x: int, n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["recursion.trust"]

TESTS = [
    ((2, 10), 1024),
    ((3, 0), 1),
    ((5, 1), 5),
    ((-2, 3), -8),
    ((7, 13), 96889010407),
    ((1, 10**9), 1),
    ((-1, 10**9 + 1), -1),
]
