"""
Valid Sudoku                                                                  [medium]

A 9×9 board is 9 strings, with "." for empty cells. Return True if the digits
placed so far break no rule: no digit repeats within a row, a column, or any of
the nine 3×3 boxes. (The board doesn't have to be solvable.)

Example:
    the board "53..7....", "6..195...", ".98....6.", ...   ->  True
    the same board with a second 9 in the top-left box      ->  False

Aim for:  one pass over the 81 cells.
Hint:     One set per row, per column and per box. The box of (r, c) is (r // 3) * 3 + c // 3.
          Or put tuples like ("row", r, d), ("col", c, d), ("box", r // 3, c // 3, d) in one set.
"""


def is_valid_sudoku(board: list[str]) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _brute(board):
    groups = [[board[r][c] for c in range(9)] for r in range(9)]
    groups += [[board[r][c] for r in range(9)] for c in range(9)]
    groups += [[board[br + r][bc + c] for r in range(3) for c in range(3)] for br in (0, 3, 6) for bc in (0, 3, 6)]
    for g in groups:
        digits = [x for x in g if x != "."]
        if len(digits) != len(set(digits)):
            return False
    return True


_OK = ["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"]


def _cases():
    import random
    rng = random.Random(41)
    out = []
    for i in range(8):
        grid = [["."] * 9 for _ in range(9)]
        for _ in range(rng.randint(6, 18)):
            grid[rng.randrange(9)][rng.randrange(9)] = str(rng.randint(1, 9))
        board = ["".join(r) for r in grid]
        out.append(((board,), _brute(board)))
    return out


TESTS = [
    ((_OK,), True),
    ((["539.7...."] + _OK[1:],), False),                       # a second 9 in the top-left box only
    ((["53..7..5."] + _OK[1:],), False),                       # a 5 twice in the first row
    ((["83..7...."] + _OK[1:],), False),                       # an 8 twice in the first column
    (([".........",] * 9,), True),
] + _cases()
