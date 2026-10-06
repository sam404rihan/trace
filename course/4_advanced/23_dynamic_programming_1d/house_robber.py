"""
House Robber                                                                [medium]

nums[i] is the money in house i along a street. You can't rob two houses
next to each other. Return the most money you can take.

Example:
    house_robber([2, 7, 9, 3, 1])  ->  12      2 + 9 + 1

Aim for:  O(n) time, O(1) space
Hint:     At house i you either skip it (keep the best up to i - 1) or rob it
          (best up to i - 2, plus nums[i]). You only ever need the last two answers.
"""


def house_robber(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 2, 3, 1],), 4),
    (([2, 7, 9, 3, 1],), 12),
    (([5],), 5),
    (([],), 0),
    (([2, 1, 1, 2],), 4),
]
