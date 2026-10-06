"""
Binary Search                                                 [easy] · binary search

`nums` is sorted in ascending order with no duplicates. Return the index of
`target`, or -1 if it isn't there.

Example:
    binary_search([-1, 0, 3, 5, 9, 12], 9)  ->  4
    binary_search([-1, 0, 3, 5, 9, 12], 2)  ->  -1

Aim for:  O(log n) time — no `in`, no .index()
Hint:     Keep a range [lo, hi] that must contain the target if it exists.
          Look at the middle and throw away the half it can't be in.
          Be careful: is your loop `lo < hi` or `lo <= hi`? Why?
"""


def binary_search(nums: list[int], target: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([-1, 0, 3, 5, 9, 12], 9), 4),
    (([-1, 0, 3, 5, 9, 12], 2), -1),
    (([5], 5), 0),
    (([], 1), -1),
    (([1, 3], 3), 1),
    (([1, 3], 1), 0),
    (([2, 4, 6, 8, 10, 12, 14, 16, 18], 2), 0),
    (([2, 4, 6, 8, 10, 12, 14, 16, 18], 18), 8),
    (([2, 4, 6, 8, 10, 12, 14, 16, 18], 7), -1),
]
