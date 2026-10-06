def n_queens(n: int) -> int:
    # One queen per row. Sets make "is this square attacked?" O(1):
    # squares on the same diagonal share row - col; on an anti-diagonal, row + col.
    cols, diagonals, anti_diagonals = set(), set(), set()

    def place(row):
        if row == n:
            return 1
        count = 0
        for col in range(n):
            if col in cols or row - col in diagonals or row + col in anti_diagonals:
                continue
            cols.add(col)
            diagonals.add(row - col)
            anti_diagonals.add(row + col)
            count += place(row + 1)
            cols.remove(col)
            diagonals.remove(row - col)
            anti_diagonals.remove(row + col)
        return count

    return place(0)
