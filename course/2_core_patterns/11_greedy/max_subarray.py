"""
Maximum Subarray                                                            [medium]

Return the largest sum of any non-empty contiguous subarray of `nums`.

Example:
    max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])  ->  6      [4, -1, 2, 1]

Aim for:  O(n) time, O(1) space (Kadane's algorithm)
Hint:     Walk once keeping `current`, the best sum of a subarray ending here.
          At each x: either extend (current + x) or start over (x), whichever
          is bigger. Start with nums[0], not 0, or all-negative lists break.
"""


def max_subarray(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["greedy.kadane"]

TESTS = [
    (([-2, 1, -3, 4, -1, 2, 1, -5, 4],), 6),
    (([1],), 1),
    (([5, 4, -1, 7, 8],), 23),
    (([-3, -2, -5],), -2),
]
