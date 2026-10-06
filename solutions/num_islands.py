def num_islands(grid: list[list[int]]) -> int:
    # Each unvisited land cell starts a new island; flood-fill sinks all of it.
    # O(rows · cols). Iterative DFS with a stack avoids recursion limits.
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    islands = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1:
                continue
            islands += 1
            stack = [(r, c)]
            grid[r][c] = 0                     # mark visited by sinking it
            while stack:
                cr, cc = stack.pop()
                for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                        grid[nr][nc] = 0
                        stack.append((nr, nc))
    return islands
