"""
Open neighbours of a cell                                                   [snippet]

The grid is a list of strings: "." is open, "#" is a wall. Return the open
cells next to (r, c), as (row, col) tuples, in this order: up, down, left, right.
Skip anything off the edge of the grid.

Example:
    grid = ["..#",
            ".#.",
            "..."]
    open_neighbors(grid, 1, 0)  ->  [(0, 0), (2, 0)]

Every grid BFS and DFS starts with exactly this helper.

Hint:     for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)): check 0 <= nr < rows and
          0 <= nc < cols before you look at grid[nr][nc].
"""


def open_neighbors(grid: list[str], r: int, c: int) -> list[tuple[int, int]]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((["..#", ".#.", "..."], 1, 0), [(0, 0), (2, 0)]),
    ((["..#", ".#.", "..."], 0, 0), [(1, 0), (0, 1)]),
    ((["..#", ".#.", "..."], 2, 1), [(2, 0), (2, 2)]),
    ((["."], 0, 0), []),
    (([".#.", "...", ".#."], 1, 1), [(1, 0), (1, 2)]),
]
