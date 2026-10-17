"""
Pivot Index                                                                   [easy]

Return the leftmost index i where the sum of everything to the left of i
equals the sum of everything to the right of i. Return -1 if there's none.
(Nothing on a side counts as a sum of 0.)

Example:
    pivot_index([1, 7, 3, 6, 5, 6])  ->  3      1+7+3 == 5+6

Aim for:  O(n) time, O(1) space
Hint:     You know the total. As you walk, keep `left_sum`. The right side is
          then total - left_sum - nums[i].
"""


def pivot_index(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["prefix.sums"]

TESTS = [
    (([1, 7, 3, 6, 5, 6],), 3),
    (([1, 2, 3],), -1),
    (([2, 1, -1],), 0),
    (([0],), 0),
    (([-1, -1, 0, 1, 1, 0],), 5),
]
