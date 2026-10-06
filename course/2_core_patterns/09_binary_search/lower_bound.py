"""
Lower bound                                                                 [snippet]

`nums` is sorted. Return the first index i where nums[i] >= x. If every
number is smaller than x, return len(nums).

Example:
    lower_bound([1, 3, 3, 5], 3)  ->  1
    lower_bound([1, 3, 3, 5], 4)  ->  3
    lower_bound([1, 3, 3, 5], 9)  ->  4

This is the most reusable binary search there is: "first position where a
yes/no question flips to yes". Write it by hand, without bisect.

Aim for:  O(log n).
Hint:     lo, hi = 0, len(nums)   (hi is one past the end, because the answer can be len(nums))
          while lo < hi: mid = (lo + hi) // 2
              if nums[mid] < x: lo = mid + 1   else: hi = mid
"""


def lower_bound(nums: list[int], x: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 3, 3, 5], 3), 1),
    (([1, 3, 3, 5], 4), 3),
    (([1, 3, 3, 5], 9), 4),
    (([1, 3, 3, 5], 0), 0),
    (([], 5), 0),
    (([2, 2, 2, 2, 2], 2), 0),
    ((list(range(0, 2_000_000, 2)), 777_777), 388_889),
]
