"""
Number of 1 Bits                                                                [easy]

Return how many bits are set to 1 in the binary form of a non-negative integer.

Example:
    hamming_weight(11)          ->  3       1011
    hamming_weight(2**31)       ->  1

Aim for:  one loop step per SET bit, not per bit.
Hint:     n & (n - 1) clears the lowest 1 bit. Count how many times you can do that before n is 0.
"""


def hamming_weight(n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [((n,), bin(n).count("1")) for n in (11, 128, 0, 1, 2**31, 2**32 - 3, 255, 1023, 2**60 + 7)]
