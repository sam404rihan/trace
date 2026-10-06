def spiral_order(matrix: list[list[int]]) -> list[int]:
    if not matrix or not matrix[0]:
        return []
    out = []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):        # top row, left to right
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):        # right column, downwards
            out.append(matrix[r][right])
        right -= 1
        if top <= bottom:                       # bottom row, right to left (if any rows remain)
            for c in range(right, left - 1, -1):
                out.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:                       # left column, upwards (if any columns remain)
            for r in range(bottom, top - 1, -1):
                out.append(matrix[r][left])
            left += 1
    return out
