"""
Move Zeroes                                                                   [easy]

Move every 0 in `nums` to the end, keeping the other numbers in their
original order. Do it in place (no new list), then return `nums`.

Example:
    move_zeroes([0, 1, 0, 3, 12])  ->  [1, 3, 12, 0, 0]

Aim for:  O(n) time, O(1) extra space
Hint:     The "write pointer" trick from the lesson: copy each non-zero to
          nums[write], then fill the rest with zeros.
"""


def move_zeroes(nums: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([0, 1, 0, 3, 12],), [1, 3, 12, 0, 0]),
    (([0],), [0]),
    (([1, 2],), [1, 2]),
    (([0, 0, 1],), [1, 0, 0]),
    (([4, 0, 5, 0, 0, 6],), [4, 5, 6, 0, 0, 0]),
]
