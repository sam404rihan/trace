from collections import deque


def route_to_exit(grid: list[str]) -> list[tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "S")
    parent, queue = {start: None}, deque([start])
    while queue:
        r, c = queue.popleft()
        if grid[r][c] == "E":
            path, cell = [], (r, c)
            while cell is not None:          # walk the parents back to S
                path.append(cell)
                cell = parent[cell]
            return path[::-1]
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):   # up, down, left, right
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and (nr, nc) not in parent:
                parent[(nr, nc)] = (r, c)
                queue.append((nr, nc))
    return []
