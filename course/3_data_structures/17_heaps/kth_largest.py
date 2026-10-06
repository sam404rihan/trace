"""
Kth Largest Element in an Array                                      [medium] · heap

Return the k-th largest value in `nums` (k-th largest in sorted order, so
duplicates count separately).

Example:
    kth_largest([3, 2, 1, 5, 6, 4], 2)  ->  5

Aim for:  O(n log k) with a heap. (Sorting is O(n log n) — fine, but practise the heap.)
Hint:     Keep a min-heap of the k largest values seen so far (module `heapq`).
          Whenever it grows past k, pop the smallest. The top is your answer.
          Want to see how a heap works inside? Read structures/heap.py.
"""


def kth_largest(nums: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([3, 2, 1, 5, 6, 4], 2), 5),
    (([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4),
    (([1], 1), 1),
    (([7, 7, 7], 2), 7),
    (([-5, -1, -10], 3), -10),
]
