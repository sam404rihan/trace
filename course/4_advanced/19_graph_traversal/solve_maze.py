"""
Maze solver                                                                   [build]

The maze is a list of strings: "S" is the start, "E" the exit, "#" walls,
"." open floor. Return a shortest route from S to E as a string of moves:
"U", "D", "L", "R". If there's no route, return None.

    solve_maze(["S.#",
                ".##",
                "..E"])
    ->  "DDRR"

Rules:
  - Any shortest route is accepted. The tests check that your route is legal
    (stays in bounds, never enters a wall, ends on E) and has the minimum number of moves.
  - S and E are always present, and S != E.

Hint:     BFS from S, remembering for each cell the cell you came from (a "parent" dict).
          When you reach E, walk the parents back to S and reverse, turning each
          step into a letter.
"""


def solve_maze(maze: list[str]) -> str | None:
    raise NotImplementedError  # replace this line with your solution


def _shortest(maze):
    from collections import deque
    rows, cols = len(maze), len(maze[0])
    start = next((r, c) for r in range(rows) for c in range(cols) if maze[r][c] == "S")
    dist = {start: 0}
    q = deque([start])
    while q:
        r, c = q.popleft()
        if maze[r][c] == "E":
            return dist[(r, c)]
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] != "#" and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                q.append((nr, nc))
    return None


def CHECK(got, expected, args):
    maze = args[0]
    best = _shortest(maze)
    if best is None:
        return got is None
    if not isinstance(got, str) or len(got) != best:
        return False
    rows, cols = len(maze), len(maze[0])
    r, c = next((r, c) for r in range(rows) for c in range(cols) if maze[r][c] == "S")
    moves = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
    for m in got:
        if m not in moves:
            return False
        r, c = r + moves[m][0], c + moves[m][1]
        if not (0 <= r < rows and 0 <= c < cols) or maze[r][c] == "#":
            return False
    return maze[r][c] == "E"


def _describe(maze):
    best = _shortest(maze)
    return None if best is None else f"any shortest route ({best} moves)"


def _big():
    import random
    rng = random.Random(25)
    rows, cols = 120, 160
    g = [["#" if rng.random() < 0.28 else "." for _ in range(cols)] for _ in range(rows)]
    g[0][0], g[rows - 1][cols - 1] = "S", "E"
    g[0][1] = g[1][0] = g[rows - 2][cols - 1] = g[rows - 1][cols - 2] = "."
    maze = ["".join(row) for row in g]
    if _shortest(maze) is None:
        for c in range(cols):
            g[0][c] = "." if c else "S"
        for r in range(rows):
            g[r][cols - 1] = "." if r < rows - 1 else "E"
        maze = ["".join(row) for row in g]
    return maze


_MAZES = [
    ["S.#", ".##", "..E"],
    ["S....", "###.#", "E...."],
    ["S#E"],
    ["S.", ".E"],
    ["S..#....", ".#.#.##.", ".#...#..", ".####.#.", "......#E"],
    _big(),
]

USES = ["bfs.path"]

TESTS = [((m,), _describe(m)) for m in _MAZES]
