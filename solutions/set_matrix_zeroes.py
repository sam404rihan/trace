def set_matrix_zeroes(matrix: list[list[int]]) -> None:
    R, C = len(matrix), len(matrix[0])
    first_row_zero = any(v == 0 for v in matrix[0])
    first_col_zero = any(matrix[r][0] == 0 for r in range(R))
    # Use row 0 and column 0 as markers for the rest of the grid.
    for r in range(1, R):
        for c in range(1, C):
            if matrix[r][c] == 0:
                matrix[r][0] = matrix[0][c] = 0
    for r in range(1, R):
        for c in range(1, C):
            if matrix[r][0] == 0 or matrix[0][c] == 0:
                matrix[r][c] = 0
    if first_row_zero:
        for c in range(C):
            matrix[0][c] = 0
    if first_col_zero:
        for r in range(R):
            matrix[r][0] = 0
