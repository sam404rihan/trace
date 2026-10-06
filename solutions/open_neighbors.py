def open_neighbors(grid: list[str], r: int, c: int) -> list[tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    out = []
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):     # up, down, left, right
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
            out.append((nr, nc))
    return out
