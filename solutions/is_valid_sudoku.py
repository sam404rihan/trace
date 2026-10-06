def is_valid_sudoku(board: list[str]) -> bool:
    seen = set()
    for r in range(9):
        for c in range(9):
            d = board[r][c]
            if d == ".":
                continue
            keys = (("row", r, d), ("col", c, d), ("box", r // 3, c // 3, d))
            if any(k in seen for k in keys):     # this digit already sits in that row/col/box
                return False
            seen.update(keys)
    return True
