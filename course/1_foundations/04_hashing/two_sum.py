"""
Two Sum                                                    [easy] · arrays and hashing

Given a list of integers `nums` and an integer `target`, return the indices
[i, j] (with i < j) of the two numbers that add up to `target`.
Exactly one answer exists, and you can't use the same element twice.

Example:
    two_sum([2, 7, 11, 15], 9)  ->  [0, 1]      because 2 + 7 == 9

Aim for:  O(n) time, O(n) space   (the nested-loop O(n²) version is a fine first step)
Hint:     For each number x you need a partner target - x. Where could you
          look that partner up in O(1)?
"""


def two_sum(nums: list[int], target: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([2, 7, 11, 15], 9), [0, 1]),
    (([3, 2, 4], 6), [1, 2]),
    (([3, 3], 6), [0, 1]),
    (([-1, -2, -3, -4, -5], -8), [2, 4]),
    (([1, 5, 9, 14, 20], 34), [3, 4]),
]
