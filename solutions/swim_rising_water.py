def swim_rising_water(grid: list[list[int]]) -> int:
    n = len(grid)
    heap, seen = [(grid[0][0], 0, 0)], {(0, 0)}
    while heap:
        level, r, c = heappop(heap)             # the lowest "worst cell so far" route first
        if (r, c) == (n - 1, n - 1):
            return level
        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= x < n and 0 <= y < n and (x, y) not in seen:
                seen.add((x, y))
                heappush(heap, (max(level, grid[x][y]), x, y))
    return -1
