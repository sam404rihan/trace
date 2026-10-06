def is_safe(queens: list[int], col: int) -> bool:
    row = len(queens)
    for r, c in enumerate(queens):
        if c == col or abs(c - col) == row - r:     # same column, or same diagonal
            return False
    return True
