from collections import deque


def shortest_path_all_keys(grid: list[str]) -> int:
    rows, cols = len(grid), len(grid[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "@")
    total = sum(ch.islower() for row in grid for ch in row)
    first = (*start, frozenset())
    seen, queue = {first}, deque([(first, 0)])      # state = (row, col, keys held)
    while queue:
        (r, c, keys), steps = queue.popleft()
        if len(keys) == total:
            return steps
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if not (0 <= nr < rows and 0 <= nc < cols) or grid[nr][nc] == "#":
                continue
            ch = grid[nr][nc]
            if ch.isupper() and ch.lower() not in keys:
                continue                              # locked, and we don't have its key yet
            state = (nr, nc, (keys | {ch}) if ch.islower() else keys)
            if state not in seen:
                seen.add(state)
                queue.append((state, steps + 1))
    return -1
