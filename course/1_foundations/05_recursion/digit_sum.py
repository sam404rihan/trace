"""
Digit sum, recursively                                                      [snippet]

Return the sum of the digits of a non-negative integer, using recursion:
the last digit is n % 10, and the rest of the number is n // 10.

Example:
    digit_sum(4096)  ->  19
    digit_sum(7)     ->  7

Hint:     Base case: a single digit (n < 10) is its own sum.
          Otherwise: last digit + digit_sum(the rest). Trust the smaller call.
"""


def digit_sum(n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["recursion.trust"]
USES = []

TESTS = [
    ((4096,), 19),
    ((7,), 7),
    ((0,), 0),
    ((10,), 1),
    ((999_999,), 54),
]
