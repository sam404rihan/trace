def count_enclosed(grid: list[str]) -> int:
    rows, cols = len(grid), len(grid[0])
    # Search FROM the edge: every open border cell starts the flood at once.
    stack = [(r, c) for r in range(rows) for c in range(cols)
             if grid[r][c] == "." and (r in (0, rows - 1) or c in (0, cols - 1))]
    safe = set(stack)
    while stack:
        r, c = stack.pop()
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "." and (nr, nc) not in safe:
                safe.add((nr, nc))
                stack.append((nr, nc))
    return sum(row.count(".") for row in grid) - len(safe)
