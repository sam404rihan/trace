"""
Find a meeting time                                                           [build]

Each person has a list of busy intervals [start, end] (in minutes, in no
particular order, possibly overlapping). Return every free slot that
everyone shares inside the working day [day_start, day_end], keeping only
slots at least `min_len` minutes long.

    free_slots([[[60, 120], [300, 360]],          # person A
                [[90, 150], [200, 240]]],         # person B
               0, 480, 30)
    ->  [[0, 60], [150, 200], [240, 300], [360, 480]]

Rules:
  - A slot is free if no one is busy during it. Busy intervals that touch
    leave no gap.
  - Busy time outside [day_start, day_end] doesn't matter. Clip the slots to the day.
  - Return slots in time order.

Hint:     Throw everyone's busy intervals into one list, sort by start, and merge
          them. The gaps between merged blocks (and before the first and after the
          last, inside the day) are the free slots.
"""


def free_slots(busy: list[list[list[int]]], day_start: int, day_end: int, min_len: int) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


USES = ["intervals.overlap", "intervals.merge", "intervals.sort_by_start"]

TESTS = [
    (([[[60, 120], [300, 360]], [[90, 150], [200, 240]]], 0, 480, 30),
     [[0, 60], [150, 200], [240, 300], [360, 480]]),
    (([[[60, 120], [300, 360]], [[90, 150], [200, 240]]], 0, 480, 60),
     [[0, 60], [240, 300], [360, 480]]),
    (([[[0, 100]], [[100, 200]]], 0, 200, 1), []),
    (([[[-50, 30], [470, 600]], []], 0, 480, 10), [[30, 470]]),
    (([[[200, 300], [100, 150]], [[120, 210]]], 100, 400, 15), [[300, 400]]),
    (([[], []], 540, 1020, 60), [[540, 1020]]),
    (([[[10, 20], [25, 30]]], 0, 40, 5), [[0, 10], [20, 25], [30, 40]]),
]
