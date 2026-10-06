def rotate_image(matrix: list[list[int]]) -> None:
    n = len(matrix)
    for i in range(n):                  # 1) transpose across the main diagonal
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:                  # 2) mirror each row
        row.reverse()
