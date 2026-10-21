"""
Sudoku solver                                                                 [build]

The board is 9 strings of 9 characters: digits, or "." for an empty cell.
Fill every empty cell so that each row, each column and each 3×3 box holds
the digits 1-9 exactly once. Return the solved board in the same format.

    solve_sudoku(["53..7....", "6..195...", ".98....6.",
                  "8...6...3", "4..8.3..1", "7...2...6",
                  ".6....28.", "...419..5", "....8..79"])
    ->  ["534678912", "672195348", "198342567",
         "859761423", "426853791", "713924856",
         "961537284", "287419635", "345286179"]

Rules:
  - Every puzzle in the tests has at least one solution. Any valid solution
    that keeps the given digits is accepted.
  - The last test is a famously hard puzzle. A plain left-to-right search can be too
    slow for it. That's where the speed-up in the hint pays off.

Aim for:  backtracking: find an empty cell, try each digit that doesn't clash, recurse,
          and undo on failure. Make the clash check O(1) with sets for each row,
          column and box: box index = (r // 3) * 3 + c // 3.
Hint:     Convert the board to a list of lists so you can write into it. Speed-up:
          always fill the empty cell with the FEWEST legal digits first.
"""


def solve_sudoku(board: list[str]) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


_SOLVED = ["534678912", "672195348", "198342567", "859761423", "426853791",
           "713924856", "961537284", "287419635", "345286179"]


def _holes(seed, count):
    import random
    rng = random.Random(seed)
    cells = rng.sample(range(81), count)
    grid = [list(row) for row in _SOLVED]
    for i in cells:
        grid[i // 9][i % 9] = "."
    return ["".join(row) for row in grid]


def CHECK(got, expected, args):
    puzzle = args[0]
    if not isinstance(got, list) or len(got) != 9 or any(not isinstance(r, str) or len(r) != 9 for r in got):
        return False
    digits = set("123456789")
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] != "." and puzzle[r][c] != got[r][c]:
                return False
    rows = [set(row) for row in got]
    cols = [{got[r][c] for r in range(9)} for c in range(9)]
    boxes = [{got[br + r][bc + c] for r in range(3) for c in range(3)} for br in (0, 3, 6) for bc in (0, 3, 6)]
    return all(group == digits for group in rows + cols + boxes)


_PUZZLES = [
    ["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"],
    _holes(1, 30),
    _holes(2, 45),
    _holes(3, 52),
    ["8........", "..36.....", ".7..9.2..", ".5...7...", "....457..", "...1...3.", "..1....68", "..85...1.", ".9....4.."],
]

USES = ["hash.set_lookup", "bt.core"]

TESTS = [((p,), "a valid completed board") for p in _PUZZLES]
