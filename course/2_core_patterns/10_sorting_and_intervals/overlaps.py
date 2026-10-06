"""
Do they overlap?                                                            [snippet]

Intervals are [start, end] with start <= end. Return True if a and b share
at least one point. Touching counts: [1, 3] and [3, 5] overlap at 3.

Example:
    overlaps([1, 3], [2, 6])  ->  True
    overlaps([1, 3], [4, 6])  ->  False

Hint:     It's easier to say when they DON'T overlap: one ends before the other
          starts. Overlap is the opposite of that, which gives one line:
          a[0] <= b[1] and b[0] <= a[1].
"""


def overlaps(a: list[int], b: list[int]) -> bool:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 3], [2, 6]), True),
    (([1, 3], [4, 6]), False),
    (([1, 3], [3, 5]), True),
    (([4, 6], [1, 3]), False),
    (([1, 10], [3, 4]), True),
    (([3, 4], [1, 10]), True),
    (([5, 5], [5, 5]), True),
]
