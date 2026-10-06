"""
Distance to the nearest exit                                                 [guided]

The grid is a list of strings: "E" is an exit, "." is open floor, "#" is a
wall. Return a grid of numbers, the same size, where each open cell or exit
holds the number of steps (up/down/left/right) to the NEAREST exit. Exits are 0.
Walls, and cells that can't reach any exit, are -1.

Example:
    distance_to_exit(["E..",
                      ".#.",
                      "..E"])
    ->  [[0, 1, 2],
         [1, -1, 1],
         [2, 1, 0]]
"""


def distance_to_exit(grid: list[str]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def _bfs_all(grid):
    from collections import deque
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    q = deque()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "E":
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and dist[nr][nc] < 0:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist


def _big():
    import random
    rng = random.Random(24)
    rows = cols = 220
    g = [["#" if rng.random() < 0.25 else "." for _ in range(cols)] for _ in range(rows)]
    for _ in range(600):
        g[rng.randrange(rows)][rng.randrange(cols)] = "E"
    grid = ["".join(row) for row in g]
    return grid, _bfs_all(grid)


_GRID, _DIST = _big()

STEPS = [
    {
        "title": "One exit",
        "text": "BFS outward from the exit. Each cell's distance is its neighbour's distance + 1, the first time BFS reaches it.",
        "hint": "dist = [[-1] * cols for each row]; set the exit to 0 and put it in a deque. Pop, look at 4 neighbours, "
                "and set any open one still at -1.",
        "tests": [
            ((["E..", "...", "..."],), [[0, 1, 2], [1, 2, 3], [2, 3, 4]]),
            ((["..", ".E"],), [[2, 1], [1, 0]]),
        ],
    },
    {
        "title": "Many exits",
        "text": "Now there are several exits. You could BFS from each one and keep the minimum, but there's a neater way: "
                "put ALL exits in the queue at distance 0 before you start (multi-source BFS). The rings grow from every "
                "exit at once, and each cell is reached first by its nearest exit.",
        "hint": "Same BFS, different start: loop over the grid, enqueue every 'E'.",
        "tests": [
            ((["E..", ".#.", "..E"],), [[0, 1, 2], [1, -1, 1], [2, 1, 0]]),
            ((["E...E"],), [[0, 1, 2, 1, 0]]),
            ((["E", ".", ".", "E"],), [[0], [1], [1], [0]]),
        ],
    },
    {
        "title": "Walls, gaps and scale",
        "text": "Walls stay -1, and so does any open area that walls cut off from every exit. The last test is a "
                "220×220 grid with 600 exits: one BFS per exit is far too slow, but one multi-source BFS visits each cell once.",
        "hint": "If you already enqueue every exit up front, this step only needs the -1 defaults to be right.",
        "tests": [
            ((["E#.", "##.", "..."],), [[0, -1, -1], [-1, -1, -1], [-1, -1, -1]]),
            ((["#E#"],), [[-1, 0, -1]]),
            ((_GRID,), _DIST),
        ],
    },
]
