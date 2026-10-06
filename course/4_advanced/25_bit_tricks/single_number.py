"""
Single Number                                                                 [easy]

Every number in `nums` appears exactly twice, except one that appears once.
Return that one.

Example:
    single_number([4, 1, 2, 1, 2])  ->  4

Aim for:  O(n) time and O(1) extra space, so no Counter or set
Hint:     x ^ x == 0 and x ^ 0 == x, and order doesn't matter. XOR everything.
"""


def single_number(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([2, 2, 1],), 1),
    (([4, 1, 2, 1, 2],), 4),
    (([1],), 1),
    (([-3, 7, 7],), -3),
]
