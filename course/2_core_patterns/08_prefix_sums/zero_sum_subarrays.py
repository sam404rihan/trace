"""
Count Zero-Sum Subarrays                                                      [easy]

Count the contiguous subarrays of `nums` that add up to 0. Numbers can be
negative.

Example:
    zero_sum_subarrays([1, -1, 2, -2])  ->  3      [1, -1], [2, -2] and [1, -1, 2, -2]
    zero_sum_subarrays([0, 0])          ->  3

Aim for:  O(n). The last test has 100,000 numbers: adding up every subarray is
          O(n²) and times out.
Hint:     nums[i:j] adds up to 0 exactly when the running totals before i and
          before j are equal. So walk once with a running total and a dict of how
          many times each total has appeared, starting with {0: 1} for the empty
          start. A new total pairs with every earlier copy of itself.
"""


def zero_sum_subarrays(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["prefix.count_dict"]
USES = ["hash.count_pairs", "prefix.sums"]

TESTS = [
    (([1, -1, 2, -2],), 3),
    (([0, 0],), 3),
    (([1, 2, 3],), 0),
    (([],), 0),
    (([0],), 1),
    (([3, -3, 3, -3],), 4),
    (([4, 2, -3, 1, 6],), 1),
    (([1, -1] * 50_000,), 2_500_000_000),
]
