"""
Two Sum II (sorted input)                                                     [easy]

`nums` is sorted in ascending order. Return the indices [i, j] (i < j) of the
two numbers that add up to `target`. Exactly one answer exists.

Example:
    two_sum_sorted([2, 7, 11, 15], 9)  ->  [0, 1]

Aim for:  O(n) time and O(1) space. No dict this time: use the sorting.
Hint:     Start with the smallest and largest. Too small? Move left up.
          Too big? Move right down.
"""


def two_sum_sorted(nums: list[int], target: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([2, 7, 11, 15], 9), [0, 1]),
    (([2, 3, 4], 6), [0, 2]),
    (([-1, 0], -1), [0, 1]),
    (([1, 2, 3, 4, 4, 9, 56, 90], 8), [3, 4]),
]
