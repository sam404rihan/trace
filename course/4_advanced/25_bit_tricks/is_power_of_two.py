"""
Power of Two                                                                  [easy]

Return True if n is a power of two (1, 2, 4, 8, ...).

Example:
    is_power_of_two(16)  ->  True
    is_power_of_two(6)   ->  False

Aim for:  O(1), no loops
Hint:     A power of two has exactly one 1 bit. x & (x - 1) removes the lowest
          1 bit. What's left for a power of two? Don't forget n <= 0.
"""


def is_power_of_two(n: int) -> bool:
    raise NotImplementedError  # replace this line with your solution


USES = ["bits.clear_lowest"]

TESTS = [
    ((1,), True),
    ((16,), True),
    ((3,), False),
    ((0,), False),
    ((-8,), False),
    ((2**40,), True),
    ((2**40 + 1,), False),
]
