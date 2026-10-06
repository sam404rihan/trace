def min_obstacles(grid: list[list[int]]) -> int:
    R, C = len(grid), len(grid[0])
    dist = [[float("inf")] * C for _ in range(R)]
    dist[0][0] = 0
    dq = deque([(0, 0)])
    while dq:
        r, c = dq.popleft()
        for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= x < R and 0 <= y < C:
                nd = dist[r][c] + grid[x][y]
                if nd < dist[x][y]:
                    dist[x][y] = nd
                    if grid[x][y]:
                        dq.append((x, y))       # cost 1: back of the line
                    else:
                        dq.appendleft((x, y))   # cost 0: same distance, front of the line
    return dist[R - 1][C - 1]
