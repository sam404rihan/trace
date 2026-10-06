"""
Counting Bits                                                                 [easy]

Return a list where item i is the number of 1 bits in i, for every i from
0 to n.

Example:
    count_bits(5)  ->  [0, 1, 1, 2, 1, 2]      0, 1, 10, 11, 100, 101

Aim for:  O(n), reusing earlier answers instead of counting each number from scratch
Hint:     i >> 1 is i without its last bit, and you've already counted it.
          So bits[i] = bits[i >> 1] + (i & 1). (A tiny bit of DP.)
"""


def count_bits(n: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((2,), [0, 1, 1]),
    ((5,), [0, 1, 1, 2, 1, 2]),
    ((0,), [0]),
    ((8,), [0, 1, 1, 2, 1, 2, 2, 3, 1]),
]
