"""
Count enclosed cells                                                          [easy]

The grid is a list of strings: "." is open, "#" is a wall. Moving up, down,
left or right through open cells, some open cells can reach the edge of the
grid and some are walled in. Return how many open cells can NOT reach the edge.

Example:
    count_enclosed(["#####",
                    "#..##",
                    "#####"])  ->  2

Aim for:  O(rows * cols), with one search, not one search per cell.
Hint:     Search once FROM the edge instead: put every open cell on the border in a stack,
          flood fill from all of them, and mark what you reach. The open cells you never
          reached are the enclosed ones.
"""


def count_enclosed(grid: list[str]) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["flood.from_targets"]
USES = ["dfs.flood_fill", "grid.neighbors"]

TESTS = [
    ((["#####", "#..##", "#####"],), 2),
    ((["#####", "#.#.#", "#...#", "##.##"],), 0),
    (([".#.", "#.#", ".#."],), 1),
    ((["....", ".##.", ".#..", "...."],), 0),
    ((["######", "#..#.#", "#..#.#", "######"],), 6),
]
