"""
Product of Array Except Self                             [medium] · arrays and hashing

Return a list `answer` where answer[i] is the product of every element of
`nums` except nums[i]. Don't use division.

Example:
    product_except_self([1, 2, 3, 4])  ->  [24, 12, 8, 6]

Aim for:  O(n) time, O(1) extra space (the output list doesn't count)
Hint:     answer[i] = (product of everything left of i) * (product of everything
          right of i). Can you build both with one pass each?
"""


def product_except_self(nums: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


USES = ["array.left_right_passes"]

TESTS = [
    (([1, 2, 3, 4],), [24, 12, 8, 6]),
    (([-1, 1, 0, -3, 3],), [0, 0, 9, 0, 0]),
    (([2, 3],), [3, 2]),
    (([0, 0],), [0, 0]),
    (([5, 1, 1, 2],), [2, 10, 10, 5]),
]
