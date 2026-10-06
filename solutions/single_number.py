from functools import reduce
from operator import xor


def single_number(nums: list[int]) -> int:
    # Pairs cancel under XOR (x ^ x == 0), leaving the unpaired number. O(n), O(1).
    result = 0
    for x in nums:
        result ^= x
    return result

    # One-liner: return reduce(xor, nums)
