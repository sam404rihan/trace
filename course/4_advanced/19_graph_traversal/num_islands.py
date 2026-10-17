"""
Number of Islands                                                  [easy] · graphs

`grid` is a 2D map of 1s (land) and 0s (water). An island is a group of land
cells connected horizontally or vertically (not diagonally). Count the islands.

Example:
    1 1 0 0 0
    1 1 0 0 0         num_islands(grid)  ->  3
    0 0 1 0 0
    0 0 0 1 1

Aim for:  O(rows · cols) time
Hint:     Scan every cell. When you find unvisited land, that's a new island —
          flood-fill it (DFS or BFS) so you never count its cells again.
"""


def num_islands(grid: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["graph.components"]
USES = ["grid.neighbors", "dfs.flood_fill"]

TESTS = [
    (([[1, 1, 1, 1, 0],
       [1, 1, 0, 1, 0],
       [1, 1, 0, 0, 0],
       [0, 0, 0, 0, 0]],), 1),
    (([[1, 1, 0, 0, 0],
       [1, 1, 0, 0, 0],
       [0, 0, 1, 0, 0],
       [0, 0, 0, 1, 1]],), 3),
    (([[1, 0, 1],
       [0, 1, 0],
       [1, 0, 1]],), 5),
    (([[0]],), 0),
    (([],), 0),
]
