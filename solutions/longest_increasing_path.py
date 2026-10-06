def longest_increasing_path(matrix: list[list[int]]) -> int:
    R, C = len(matrix), len(matrix[0])
    # Process cells from largest to smallest: when we reach a cell, all bigger neighbours are done.
    best = [[1] * C for _ in range(R)]
    order = sorted(((matrix[r][c], r, c) for r in range(R) for c in range(C)), reverse=True)
    for v, r, c in order:
        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= x < R and 0 <= y < C and matrix[x][y] > v:
                best[r][c] = max(best[r][c], 1 + best[x][y])
    return max(max(row) for row in best)
