"""
Flood Fill                                                                    [easy]

`image` is a grid of colours. Starting from cell (sr, sc), recolour it and
every cell connected to it (up/down/left/right) that has the SAME original
colour, to `color`. Return the image. This is the paint bucket tool.

Example:
    flood_fill([[1, 1, 1],
                [1, 1, 0],
                [1, 0, 1]], 1, 1, 2)  ->  [[2, 2, 2],
                                            [2, 2, 0],
                                            [2, 0, 1]]

Aim for:  O(rows · cols)
Hint:     DFS or BFS from (sr, sc) over cells with the original colour.
          If the new colour equals the original, return right away, or
          you'll loop forever.
"""


def flood_fill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["dfs.flood_fill"]
USES = ["grid.neighbors"]

TESTS = [
    (([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2), [[2, 2, 2], [2, 2, 0], [2, 0, 1]]),
    (([[0, 0, 0], [0, 0, 0]], 0, 0, 0), [[0, 0, 0], [0, 0, 0]]),
    (([[0]], 0, 0, 5), [[5]]),
    (([[1, 2], [2, 1]], 0, 0, 3), [[3, 2], [2, 1]]),
]
