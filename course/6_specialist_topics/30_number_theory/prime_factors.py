"""
Prime Factors                                                                 [easy]

Return the prime factors of n (2 <= n <= 10**12) in increasing order, each one
repeated as often as it divides n.

Example:
    prime_factors(360)  ->  [2, 2, 2, 3, 3, 5]
    prime_factors(97)   ->  [97]

Aim for:  O(sqrt(n)). The last tests are near 10**12: trying every number up to n times
          out, but trying divisors only up to the square root takes about a million steps.
Hint:     Trial division. Try d = 2, 3, 4, ... while d * d <= n. Whenever d divides n,
          record d, divide it out, and try the same d again. A composite d never divides
          what's left, because its own prime factors were divided out first. Whatever is
          left above 1 at the end is one more prime factor.
"""


def prime_factors(n: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["nt.trial_division"]
USES = []

TESTS = [
    ((360,), [2, 2, 2, 3, 3, 5]),
    ((97,), [97]),
    ((2,), [2]),
    ((1024,), [2] * 10),
    ((600_851_475_143,), [71, 839, 1471, 6857]),
    ((2 ** 39,), [2] * 39),
    ((999_979 * 999_983,), [999_979, 999_983]),
    ((999_999_999_989,), [999_999_999_989]),
]
