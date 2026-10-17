"""
Subarray Sum Equals K                                                       [medium]

Return how many contiguous subarrays of `nums` add up to exactly `k`.
Numbers can be negative.

Example:
    subarray_sum_equals_k([1, 2, 3], 3)  ->  2      [1, 2] and [3]

Aim for:  O(n)
Hint:     Negatives break the sliding window. Use a running total and a
          Counter of totals seen so far (start it with {0: 1}). At each step,
          how many earlier totals equal total - k?
"""


def subarray_sum_equals_k(nums: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["hash.complement", "prefix.sums", "prefix.count_dict"]

TESTS = [
    (([1, 1, 1], 2), 2),
    (([1, 2, 3], 3), 2),
    (([1, -1, 0], 0), 3),
    (([3], 3), 1),
    (([1, 2, 1, 2, 1], 3), 4),
]
