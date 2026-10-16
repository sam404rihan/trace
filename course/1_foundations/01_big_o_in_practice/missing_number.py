"""
Missing Number                                                                [easy]

`nums` contains n distinct numbers taken from 0, 1, 2, ..., n. Exactly one
number in that range is missing. Return it.

Example:
    missing_number([3, 0, 1])  ->  2

Aim for:  O(n). The last test has 200,000 numbers: checking
          `for i in range(n + 1): if i not in nums` is O(n²) and will time out.
Hint:     What should 0 + 1 + ... + n add up to? (n * (n + 1) // 2)
          Or put nums in a set so each `in` check is O(1).
"""


def missing_number(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


BIG = list(range(200_001))
BIG.remove(123_456)

USES = []

TESTS = [
    (([3, 0, 1],), 2),
    (([0, 1],), 2),
    (([9, 6, 4, 2, 3, 5, 7, 0, 1],), 8),
    (([1],), 0),
    ((BIG,), 123_456),
]
