"""
N-Queens                                                                      [hard]

Place n queens on an n×n chessboard so that no two attack each other (no
two share a row, column, or diagonal). Return how many ways there are.

Example:
    n_queens(4)  ->  2

Aim for:  backtracking with O(1) conflict checks
Hint:     Place one queen per row. Keep three sets: used columns, used
          "row - col" diagonals and used "row + col" anti-diagonals. A square
          is safe when its column and both diagonals are unused.
"""


def n_queens(n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((1,), 1),
    ((4,), 2),
    ((5,), 10),
    ((6,), 4),
    ((8,), 92),
]
