"""
Shortest Path to Get All Keys                                                 [hard]

`grid` is a list of strings:
    "@"        your start
    "."        open floor
    "#"        wall
    "a".."f"   a key
    "A".."F"   a lock: you can walk through it only once you hold its key
Each step moves up, down, left or right. Return the fewest steps to collect
EVERY key in the grid, or -1 if you can't. Each key has exactly one matching
lock somewhere (or none), and the keys are the first few letters: a, b, c...

Example:
    shortest_path_all_keys(["@.a..",
                            "###.#",
                            "b.A.B"])   ->  8
    shortest_path_all_keys(["@..aA",
                            "..B#.",
                            "....b"])   ->  6

Aim for:  O(rows * cols * 2^keys): BFS over (row, col, keys held).
Hint:     A plain BFS on cells fails, because you may need to come back to a cell after picking
          up a key. So make the state (r, c, mask) where bit i of mask = holding key i. Picking up
          a key sets its bit. A lock is passable when its bit is set. Stop when mask has every
          key's bit.
"""


def shortest_path_all_keys(grid: list[str]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(grid):
    from collections import deque
    rows, cols = len(grid), len(grid[0])
    keys = sum(ch.islower() for row in grid for ch in row)
    start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == "@")
    full = (1 << keys) - 1
    seen = {(start[0], start[1], 0)}
    q = deque([(start[0], start[1], 0, 0)])
    while q:
        r, c, mask, d = q.popleft()
        if mask == full:
            return d
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            ch = grid[nr][nc]
            if ch == "#" or ch.isupper() and not mask >> (ord(ch) - 65) & 1:
                continue
            m = mask | (1 << (ord(ch) - 97)) if ch.islower() else mask
            if (nr, nc, m) not in seen:
                seen.add((nr, nc, m))
                q.append((nr, nc, m, d + 1))
    return -1


def _random_grid(rng, rows, cols, keys):
    cells = [["." if rng.random() < 0.75 else "#" for _ in range(cols)] for _ in range(rows)]
    spots = rng.sample([(r, c) for r in range(rows) for c in range(cols)], 1 + 2 * keys)
    r, c = spots[0]
    cells[r][c] = "@"
    for i in range(keys):
        r, c = spots[1 + 2 * i]
        cells[r][c] = chr(97 + i)
        r, c = spots[2 + 2 * i]
        cells[r][c] = chr(65 + i)
    return ["".join(row) for row in cells]


def _cases():
    import random
    rng = random.Random(864)
    out = []
    for _ in range(10):
        g = _random_grid(rng, rng.randint(2, 6), rng.randint(2, 6), rng.randint(1, 3))
        out.append(((g,), _ref(g)))
    g = _random_grid(rng, 30, 30, 6)
    out.append(((g,), _ref(g)))
    return out


TESTS = [
    ((["@.a..", "###.#", "b.A.B"],), 8),
    ((["@..aA", "..B#.", "....b"],), 6),
    ((["@Aa"],), -1),
    ((["@a"],), 1),
    ((["a@b"],), 3),
] + _cases()
