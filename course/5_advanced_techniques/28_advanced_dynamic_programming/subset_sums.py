"""
Every subset sum by mask                                                    [snippet]

For n numbers there are 2^n subsets, and subset `mask` contains nums[i] when
bit i of mask is set. Return a list out of length 2^n where out[mask] is the
sum of that subset.

Example:
    subset_sums([3, 5])  ->  [0, 3, 5, 8]       masks 00, 01, 10, 11

Aim for:  O(2^n): each entry from a smaller one, not by re-adding its bits.
Hint:     mask & (mask - 1) is mask without its lowest bit, and that bit's index is
          (mask & -mask).bit_length() - 1. So out[mask] = out[mask & (mask - 1)] + nums[that index].
"""


def subset_sums(nums: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    n = len(nums)
    return [sum(nums[i] for i in range(n) if m >> i & 1) for m in range(1 << n)]


USES = ["dp.bitmask", "bits.clear_lowest"]

TESTS = [((v,), _brute(v)) for v in ([3, 5], [], [7], [1, 2, 4], [-3, 10, 0, 6], list(range(1, 13)))]
