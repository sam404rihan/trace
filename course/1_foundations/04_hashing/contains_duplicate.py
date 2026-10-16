"""
Contains Duplicate                                         [easy] · arrays and hashing

Return True if any value appears at least twice in `nums`, otherwise False.

Example:
    contains_duplicate([1, 2, 3, 1])  ->  True
    contains_duplicate([1, 2, 3, 4])  ->  False

Aim for:  O(n) time, O(n) space
Hint:     Remember what you've already seen. Which data structure answers
          "have I seen this?" in O(1)?
"""


def contains_duplicate(nums: list[int]) -> bool:
    raise NotImplementedError  # replace this line with your solution


USES = ["hash.seen_set"]

TESTS = [
    (([1, 2, 3, 1],), True),
    (([1, 2, 3, 4],), False),
    (([],), False),
    (([7],), False),
    (([1, 1, 1, 3, 3, 4, 3, 2, 4, 2],), True),
]
