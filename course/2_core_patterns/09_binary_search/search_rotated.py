"""
Search in Rotated Sorted Array                              [medium] · binary search

A sorted list of distinct numbers was rotated at some unknown point, e.g.
[0, 1, 2, 4, 5, 6, 7] became [4, 5, 6, 7, 0, 1, 2]. Return the index of
`target`, or -1.

Example:
    search_rotated([4, 5, 6, 7, 0, 1, 2], 0)  ->  4

Aim for:  O(log n) time
Hint:     Split at the middle: at least one of the two halves is still properly
          sorted. Check whether the target lies inside that sorted half.
"""


def search_rotated(nums: list[int], target: int) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["bsearch.first_true"]

TESTS = [
    (([4, 5, 6, 7, 0, 1, 2], 0), 4),
    (([4, 5, 6, 7, 0, 1, 2], 3), -1),
    (([1], 0), -1),
    (([3, 1], 1), 1),
    (([5, 1, 3], 5), 0),
    (([1, 3], 3), 1),
    (([6, 7, 1, 2, 3, 4, 5], 6), 0),
]
