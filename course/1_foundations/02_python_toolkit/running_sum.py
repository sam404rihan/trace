"""
Running Sum                                                                   [easy]

Return a list where item i is the sum of nums[0] through nums[i].

Example:
    running_sum([1, 2, 3, 4])  ->  [1, 3, 6, 10]

Aim for:  O(n) — one pass. Then try the one-liner from the lesson.
Hint:     Keep a running `total`. Or: list(itertools.accumulate(nums)).
"""


def running_sum(nums: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


USES = []

TESTS = [
    (([1, 2, 3, 4],), [1, 3, 6, 10]),
    (([1, 1, 1, 1, 1],), [1, 2, 3, 4, 5]),
    (([3, -1, 2],), [3, 2, 4]),
    (([],), []),
]
