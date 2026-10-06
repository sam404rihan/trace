def submatrix_sum_target(matrix: list[list[int]], target: int) -> int:
    rows, cols = len(matrix), len(matrix[0])
    total = 0
    for top in range(rows):
        col_sums = [0] * cols                   # column sums of rows top..bottom
        for bottom in range(top, rows):
            for j in range(cols):
                col_sums[j] += matrix[bottom][j]
            seen = Counter({0: 1})              # 1D: subarrays of col_sums summing to target
            running = 0
            for v in col_sums:
                running += v
                total += seen[running - target]
                seen[running] += 1
    return total
