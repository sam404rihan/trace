def max_area_island(grid: list[list[int]]) -> int:
    R, C = len(grid), len(grid[0])
    seen, best = set(), 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 1 and (r, c) not in seen:
                seen.add((r, c))
                stack, area = [(r, c)], 0           # iterative flood fill: no recursion limit
                while stack:
                    a, b = stack.pop()
                    area += 1
                    for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                        if 0 <= x < R and 0 <= y < C and grid[x][y] == 1 and (x, y) not in seen:
                            seen.add((x, y))
                            stack.append((x, y))
                best = max(best, area)
    return best
