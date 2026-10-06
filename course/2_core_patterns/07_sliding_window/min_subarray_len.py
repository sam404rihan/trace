"""
Shortest Subarray With Sum at Least Target                                  [medium]

`nums` holds positive integers. Return the length of the shortest contiguous
subarray whose sum is >= target, or 0 if there's none.

Example:
    min_subarray_len(7, [2, 3, 1, 2, 4, 3])  ->  2      [4, 3]

Aim for:  O(n)
Hint:     Variable window. Add nums[right] to the sum. WHILE the sum is big
          enough, record the length and shrink from the left.
"""


def min_subarray_len(target: int, nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((7, [2, 3, 1, 2, 4, 3]), 2),
    ((4, [1, 4, 4]), 1),
    ((11, [1, 1, 1, 1, 1, 1, 1, 1]), 0),
    ((15, [1, 2, 3, 4, 5]), 5),
    ((100, []), 0),
]
