"""
Meeting Rooms                                                                 [easy]

Each interval [start, end] is a meeting. Return True if one person can attend
all of them, meaning no two overlap. A meeting ending at 5 and another
starting at 5 is fine.

Example:
    can_attend_meetings([[0, 30], [5, 10], [15, 20]])  ->  False

Aim for:  O(n log n)
Hint:     Sort by start time. Then you only need to compare each meeting with
          the one right before it.
"""


def can_attend_meetings(intervals: list[list[int]]) -> bool:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["intervals.sort_by_start"]
USES = ["intervals.overlap"]

TESTS = [
    (([[0, 30], [5, 10], [15, 20]],), False),
    (([[7, 10], [2, 4]],), True),
    (([],), True),
    (([[1, 5], [5, 8]],), True),
    (([[1, 5], [8, 9], [4, 6]],), False),
]
