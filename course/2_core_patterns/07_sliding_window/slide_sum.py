"""
Slide the window one step                                                   [snippet]

A window of size k has just moved one step to the right, so it now ends at
index `right`. `window_sum` is the sum of the previous window, the one that
ended at right - 1. Return the new window's sum without re-adding everything.

Example:
    nums = [2, 1, 5, 1, 3], k = 3
    previous window [2, 1, 5] has sum 8
    slide_sum(8, nums, 3, 3)  ->  7      window [1, 5, 1]

Hint:     One in, one out: add the number entering on the right, subtract the
          one leaving on the left. Which index is leaving? right - k.
"""


def slide_sum(window_sum: int, nums: list[int], right: int, k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((8, [2, 1, 5, 1, 3], 3, 3), 7),
    ((7, [2, 1, 5, 1, 3], 4, 3), 9),
    ((3, [3, -2, 7], 1, 1), -2),
    ((5, [3, -2, 7, 4], 3, 2), 11),
]
