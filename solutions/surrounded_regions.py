def surrounded_regions(board: list[str]) -> list[str]:
    R, C = len(board), len(board[0])
    grid = [list(row) for row in board]
    stack = [(r, c) for r in range(R) for c in range(C)
             if (r in (0, R - 1) or c in (0, C - 1)) and grid[r][c] == "O"]
    for r, c in stack:
        grid[r][c] = "S"                            # safe: connected to the border
    while stack:
        r, c = stack.pop()
        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= x < R and 0 <= y < C and grid[x][y] == "O":
                grid[x][y] = "S"
                stack.append((x, y))
    return ["".join("O" if ch == "S" else "X" for ch in row) for row in grid]
