from collections import deque


def key_then_exit(grid: list[str]) -> int:
    rows, cols = len(grid), len(grid[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "@")
    seen, queue = {(*start, False)}, deque([(*start, False, 0)])   # state = (row, col, has_key)
    while queue:
        r, c, has_key, steps = queue.popleft()
        if grid[r][c] == "E":
            return steps
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] == "#":
                continue
            if grid[nr][nc] == "D" and not has_key:
                continue                     # locked until we hold the key
            state = (nr, nc, has_key or grid[nr][nc] == "k")
            if state not in seen:
                seen.add(state)
                queue.append((*state, steps + 1))
    return -1
