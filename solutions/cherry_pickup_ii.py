def cherry_pickup_ii(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    NONE = -1                                   # unreachable (cherry counts are never negative)
    best = [[NONE] * cols for _ in range(cols)] # best[a][b]: robots in columns a and b, this row
    best[0][cols - 1] = grid[0][0] + (grid[0][cols - 1] if cols > 1 else 0)
    for r in range(1, rows):
        nxt = [[NONE] * cols for _ in range(cols)]
        for a in range(cols):
            for b in range(cols):
                if best[a][b] == NONE:
                    continue
                for na in (a - 1, a, a + 1):
                    if not 0 <= na < cols:
                        continue
                    for nb in (b - 1, b, b + 1):
                        if 0 <= nb < cols:
                            gain = grid[r][na] + (grid[r][nb] if na != nb else 0)   # shared cell once
                            nxt[na][nb] = max(nxt[na][nb], best[a][b] + gain)
        best = nxt
    return max(max(row) for row in best)
