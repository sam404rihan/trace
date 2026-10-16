"""
Rotting Oranges                                                             [medium]

Each cell is 0 (empty), 1 (fresh orange) or 2 (rotten orange). Every minute,
each fresh orange next to a rotten one (up/down/left/right) becomes rotten.
Return the minutes until no fresh orange is left, or -1 if some never rot.

Example:
    2 1 1
    1 1 0         ->  4
    0 1 1

Aim for:  O(rows · cols)
Hint:     Multi-source BFS: put EVERY rotten orange in the queue at the start.
          Process the queue one level (one minute) at a time, and count the
          fresh oranges so you know if any are left over.
"""


def rotting_oranges(grid: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["bfs.multi_source"]

TESTS = [
    (([[2, 1, 1], [1, 1, 0], [0, 1, 1]],), 4),
    (([[2, 1, 1], [0, 1, 1], [1, 0, 1]],), -1),
    (([[0, 2]],), 0),
    (([[1]],), -1),
    (([[0]],), 0),
    (([[2, 1, 1, 1, 2]],), 2),
]
