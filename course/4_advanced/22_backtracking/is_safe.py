"""
Is this square safe?                                                        [snippet]

N-Queens, placed row by row. `queens[r]` is the column of the queen already
placed in row r, for rows 0 .. len(queens) - 1. Can a queen go in the NEXT
row, at column `col`, without sharing a column or a diagonal with any of them?

Example:
    is_safe([1, 3], 0)   ->  True
    is_safe([1, 3], 2)   ->  False     diagonal with the queen at row 1, column 3

Hint:     For each placed (r, c): same column if c == col. Same diagonal if
          abs(c - col) == abs(r - row), where row = len(queens).
"""


def is_safe(queens: list[int], col: int) -> bool:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 3], 0), True),
    (([1, 3], 2), False),
    (([1, 3], 1), False),
    (([], 0), True),
    (([0], 1), False),
    (([0, 2], 4), True),
    (([3, 0, 4], 1), True),
    (([3, 0, 4], 2), False),
]
