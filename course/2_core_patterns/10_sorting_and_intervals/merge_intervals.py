"""
Merge Intervals                                                             [medium]

Merge all overlapping intervals and return the result sorted by start.
Intervals that touch (one ends where the next starts) also merge.

Example:
    merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])  ->  [[1, 6], [8, 10], [15, 18]]

Aim for:  O(n log n)
Hint:     Sort by start, then sweep. Compare each interval with the LAST
          merged one. Remember max() for the end: [1, 10] swallows [2, 3].
"""


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def FINISH(result):
    return [list(iv) for iv in result]  # accept tuples as well as lists


USES = ["intervals.overlap", "intervals.merge", "intervals.sort_by_start"]

TESTS = [
    (([[1, 3], [2, 6], [8, 10], [15, 18]],), [[1, 6], [8, 10], [15, 18]]),
    (([[1, 4], [4, 5]],), [[1, 5]]),
    (([[1, 4], [0, 4]],), [[0, 4]]),
    (([[1, 10], [2, 3], [4, 5]],), [[1, 10]]),
    (([],), []),
]
