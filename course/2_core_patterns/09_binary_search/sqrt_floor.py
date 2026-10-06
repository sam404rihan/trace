"""
Integer Square Root                                                           [easy]

Return the largest integer r with r * r <= x, for x >= 0.
Don't use math.sqrt, math.isqrt, or ** 0.5.

Example:
    sqrt_floor(8)  ->  2      2*2 = 4 <= 8, but 3*3 = 9 > 8

Aim for:  O(log x). The last test is 10^18: counting up from 1 takes a
          billion steps.
Hint:     Binary search on the answer: find the first r where r * r > x,
          then step back one.
"""


def sqrt_floor(x: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((4,), 2),
    ((8,), 2),
    ((0,), 0),
    ((1,), 1),
    ((2_147_395_599,), 46_339),
    ((10**18,), 10**9),
]
