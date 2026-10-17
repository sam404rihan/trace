"""
Route to the exit                                                             [easy]

The grid is a list of strings: "S" is the start, "E" the exit, "#" a wall and
"." open floor. Return a shortest route from S to E as a list of (row, col)
cells, both ends included, or [] if there is none.

To make the answer unique: BFS from S, look at neighbours in the order up, down,
left, right, and give each cell its parent the first time you see it.

Example:
    route_to_exit(["S.#",
                   ".#.",
                   "..E"])  ->  [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]

Aim for:  O(rows * cols).
Hint:     Keep parent = {start: None}. When BFS first reaches a cell, record the cell it came
          from. When you pop E, follow the parents back to S and reverse the list.
"""


def route_to_exit(grid: list[str]) -> list[tuple[int, int]]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["bfs.path"]
USES = ["grid.neighbors", "bfs.shortest"]

TESTS = [
    ((["S.E"],), [(0, 0), (0, 1), (0, 2)]),
    ((["S.#", ".#.", "..E"],), [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]),
    ((["S#E"],), []),
    ((["S..", "##.", "E.."],), [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0)]),
    ((["S...", ".##.", "...E"],), [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (2, 3)]),
]
