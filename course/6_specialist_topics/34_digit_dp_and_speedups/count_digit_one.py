"""
Number of Digit One                                                           [medium]

Count how many times the digit 1 is written in total when you write out every
integer from 0 to n. n can be up to 10^15.

Example:
    count_digit_one(13)  ->  6        1, 10, 11 (twice), 12, 13
    count_digit_one(0)   ->  0

Aim for:  O(number of digits).
Hint:     Count each position separately. For the position worth p (1, 10, 100, ...), split n into
          high = n // (10p), cur = n // p % 10, low = n % p. Full cycles give high·p ones there.
          Then add p more if cur > 1, or low + 1 if cur == 1. (A digit DP with a "ones so far"
          state also works.)
"""


def count_digit_one(n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(n):
    total, p = 0, 1
    while p <= n:
        high, cur, low = n // (p * 10), n // p % 10, n % p
        total += high * p + (p if cur > 1 else low + 1 if cur == 1 else 0)
        p *= 10
    return total


def _brute(n):
    return sum(str(x).count("1") for x in range(n + 1))


USES = []

TESTS = [((13,), 6), ((0,), 0), ((1,), 1), ((9,), 1), ((10,), 2), ((99,), 20), ((100,), 21), ((111,), 36)] \
    + [((n,), _brute(n)) for n in (1234, 2019, 9999)] + [((n,), _ref(n)) for n in (10**15, 314_159_265_358_979, 111_111_111_111_111)]
