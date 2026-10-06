"""
Jump Game                                                                   [medium]

You start at index 0. nums[i] is the MAXIMUM jump length from index i.
Return True if you can reach the last index.

Example:
    can_jump([2, 3, 1, 1, 4])  ->  True
    can_jump([3, 2, 1, 0, 4])  ->  False     everything lands on the 0

Aim for:  O(n) time, O(1) space
Hint:     Greedy "furthest reach": walk left to right keeping
          reach = max(reach, i + nums[i]). If i ever passes reach, you're stuck.
"""


def can_jump(nums: list[int]) -> bool:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([2, 3, 1, 1, 4],), True),
    (([3, 2, 1, 0, 4],), False),
    (([0],), True),
    (([1, 0, 1],), False),
    (([2, 0, 0],), True),
]
