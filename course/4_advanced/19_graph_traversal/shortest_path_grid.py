"""
Shortest Path in a Grid                                                     [medium]

`grid` has 0 (open) and 1 (wall). Moving up/down/left/right through open
cells, return the fewest moves from the top-left cell to the bottom-right
cell, or -1 if you can't get there (including when either end is a wall).

Example:
    0 0 0
    1 1 0         ->  4
    1 1 0

Aim for:  O(rows · cols)
Hint:     BFS, because every move costs the same. Put (row, col, distance) in
          the queue and mark cells seen when you queue them.
"""


def shortest_path_grid(grid: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


USES = ["grid.neighbors", "bfs.shortest"]

TESTS = [
    (([[0, 0, 0], [1, 1, 0], [1, 1, 0]],), 4),
    (([[0, 1], [1, 0]],), -1),
    (([[0]],), 0),
    (([[1]],), -1),
    (([[0, 0, 0], [0, 1, 0], [0, 0, 0]],), 4),
    (([[0, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 1, 1, 1], [0, 0, 0, 0]],), 13),
]
