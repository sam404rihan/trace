"""
Insert into a schedule                                                       [guided]

`intervals` is sorted by start and has no overlaps. Insert `new` and merge
wherever it now overlaps (touching counts as overlapping). Return the new
sorted, non-overlapping list.

Example:
    insert_interval([[1, 3], [6, 9]], [2, 5])  ->  [[1, 5], [6, 9]]

The one-pass method has three phases: copy everything that ends before `new`
starts, merge everything that overlaps it, then copy the rest.
"""


def insert_interval(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["intervals.merge"]
USES = ["intervals.overlap"]

STEPS = [
    {
        "title": "Overlaps with one interval",
        "text": "Copy intervals that end before new starts. When you reach one that overlaps, widen new to cover it: "
                "start = min, end = max. Then copy the rest.",
        "hint": "Phase 1: while intervals[i][1] < new[0], append and move on. "
                "Phase 2: while intervals[i][0] <= new[1], merge into new. Append new. Phase 3: append the rest.",
        "tests": [
            (([[1, 3], [6, 9]], [2, 5]), [[1, 5], [6, 9]]),
            (([[1, 2], [5, 7]], [6, 8]), [[1, 2], [5, 8]]),
        ],
    },
    {
        "title": "Swallowing several",
        "text": "new can cover many intervals at once. Keep merging while the next interval starts at or before new's end.",
        "hint": "Phase 2 is a loop, not an if.",
        "tests": [
            (([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]), [[1, 2], [3, 10], [12, 16]]),
            (([[2, 3], [4, 5], [6, 7]], [1, 9]), [[1, 9]]),
            (([[1, 5]], [2, 3]), [[1, 5]]),
        ],
    },
    {
        "title": "Edges",
        "text": "Inserting into an empty list, before everything, after everything, into a gap without touching, "
                "and exactly touching a neighbour.",
        "hint": "If your three phases check i < len(intervals), all of these fall out naturally.",
        "tests": [
            (([], [4, 8]), [[4, 8]]),
            (([[5, 6]], [1, 2]), [[1, 2], [5, 6]]),
            (([[1, 2]], [5, 6]), [[1, 2], [5, 6]]),
            (([[1, 2], [8, 9]], [4, 5]), [[1, 2], [4, 5], [8, 9]]),
            (([[1, 3], [6, 9]], [3, 6]), [[1, 9]]),
        ],
    },
]
