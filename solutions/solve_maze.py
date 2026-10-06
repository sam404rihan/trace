from collections import deque


def solve_maze(maze: list[str]) -> str | None:
    rows, cols = len(maze), len(maze[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if maze[r][c] == "S")
    came_from = {start: None}               # cell -> (previous cell, move letter)
    q = deque([start])
    while q:
        r, c = q.popleft()
        if maze[r][c] == "E":               # BFS reaches E first by a shortest route
            moves, cell = [], (r, c)
            while came_from[cell]:
                cell, move = came_from[cell]
                moves.append(move)
            return "".join(reversed(moves))
        for dr, dc, move in ((-1, 0, "U"), (1, 0, "D"), (0, -1, "L"), (0, 1, "R")):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#" and (nr, nc) not in came_from:
                came_from[(nr, nc)] = ((r, c), move)
                q.append((nr, nc))
    return None
