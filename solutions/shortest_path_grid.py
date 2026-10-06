from collections import deque


def shortest_path_grid(grid: list[list[int]]) -> int:
    # BFS: cells come out of the queue in order of distance. O(rows · cols).
    rows, cols = len(grid), len(grid[0])
    if grid[0][0] == 1 or grid[rows - 1][cols - 1] == 1:
        return -1
    queue = deque([(0, 0, 0)])
    seen = {(0, 0)}
    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == (rows - 1, cols - 1):
            return dist
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0 and (nr, nc) not in seen:
                seen.add((nr, nc))       # mark when queued
                queue.append((nr, nc, dist + 1))
    return -1
