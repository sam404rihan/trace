"""
How many halvings?                                                          [snippet]

Starting from n (n ≥ 1), keep doing n = n // 2 until n is 1. Return how many
times you halved.

Example:
    halvings(8)   ->  3      8 → 4 → 2 → 1
    halvings(9)   ->  3      9 → 4 → 2 → 1
    halvings(1)   ->  0

This count is ⌊log₂ n⌋. It's why halving algorithms like binary search take
only about 20 steps for a million items, and 40 for a trillion.

Hint:     A while loop with a counter.
"""


def halvings(n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = []

TESTS = [
    ((8,), 3),
    ((9,), 3),
    ((1,), 0),
    ((2,), 1),
    ((1_000_000,), 19),
    ((10 ** 12,), 39),
]
