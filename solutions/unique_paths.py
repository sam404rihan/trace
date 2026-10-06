def unique_paths(m: int, n: int) -> int:
    # paths to a cell = paths from above + paths from the left.
    # One row is enough: row[c] (old value = from above) += row[c - 1] (from the left).
    row = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]

    # Maths shortcut: math.comb(m + n - 2, m - 1), choosing which moves go down.
