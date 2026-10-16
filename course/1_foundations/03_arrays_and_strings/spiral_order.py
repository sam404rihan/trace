"""
Spiral order                                                                 [guided]

Return all the numbers of a 2D grid in spiral order: along the top row, down
the right column, back along the bottom row, up the left column, then the
same again one ring further in.

Example:
    spiral_order([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])   ->  [1, 2, 3, 6, 9, 8, 7, 4, 5]
"""


def spiral_order(matrix: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["matrix.boundaries"]
USES = []

STEPS = [
    {
        "title": "Square grids",
        "text": "Keep four boundaries: top, bottom, left, right. Walk the top row and move top down by one, "
                "walk the right column and move right in, and so on, while top <= bottom and left <= right.",
        "hint": "Four for-loops inside one while loop. After each side, shrink that boundary by one.",
        "tests": [
            (([[1, 2], [4, 3]],), [1, 2, 3, 4]),
            (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [1, 2, 3, 6, 9, 8, 7, 4, 5]),
            (([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]],),
             [1, 2, 3, 4, 8, 12, 16, 15, 14, 13, 9, 5, 6, 7, 11, 10]),
        ],
    },
    {
        "title": "Rectangles",
        "text": "On a rectangle, the last ring can be a single row or a single column. Without a check, "
                "you walk it twice: once going right and again going left.",
        "hint": "Before the bottom row, check top <= bottom again. Before the left column, check left <= right again.",
        "tests": [
            (([[1, 2, 3, 4], [5, 6, 7, 8]],), [1, 2, 3, 4, 8, 7, 6, 5]),
            (([[1, 2], [3, 4], [5, 6], [7, 8]],), [1, 2, 4, 6, 8, 7, 5, 3]),
            (([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]],), [1, 2, 3, 4, 5, 10, 15, 14, 13, 12, 11, 6, 7, 8, 9]),
        ],
    },
    {
        "title": "Edges",
        "text": "One row, one column, a single cell, and empty input ([] or [[]]).",
        "hint": "Return [] early if not matrix or not matrix[0].",
        "tests": [
            (([[1, 2, 3]],), [1, 2, 3]),
            (([[1], [2], [3]],), [1, 2, 3]),
            (([[7]],), [7]),
            (([],), []),
            (([[]],), []),
        ],
    },
]
