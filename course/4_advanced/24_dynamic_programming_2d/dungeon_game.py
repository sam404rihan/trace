"""
Dungeon Game                                                                  [hard]

A knight starts in the top-left room of `dungeon` and must reach the princess
in the bottom-right room, moving only right or down. Entering a room changes
his health by its value (negative = demons, positive = a potion; the first and
last rooms count too). If his health ever drops to 0 or below, he dies.
Return the smallest starting health that gets him there alive.

Example:
    dungeon_game([[-2,  -3,  3],
                  [-5, -10,  1],
                  [10,  30, -5]])   ->  7      right, right, down, down
    dungeon_game([[0]])             ->  1

Aim for:  O(rows * cols).
Hint:     Going forward doesn't work: you'd have to track both current health and the lowest
          point so far. Go BACKWARDS from the princess instead: need[r][c] = the health you must
          have when entering (r, c). need = max(1, min(need below, need right) - dungeon[r][c]).
          At the princess, use 1 in place of the neighbours.
"""


def dungeon_game(dungeon: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(dungeon):
    """Every path, tracking the lowest running total."""
    rows, cols = len(dungeon), len(dungeon[0])
    best = float("inf")

    def go(r, c, total, low):
        nonlocal best
        total += dungeon[r][c]
        low = min(low, total)
        if r == rows - 1 and c == cols - 1:
            best = min(best, max(1, 1 - low))
            return
        if r + 1 < rows:
            go(r + 1, c, total, low)
        if c + 1 < cols:
            go(r, c + 1, total, low)
    go(0, 0, 0, 0)
    return best


def _fast(dungeon):
    rows, cols = len(dungeon), len(dungeon[0])
    INF = float("inf")
    need = [[INF] * (cols + 1) for _ in range(rows + 1)]
    need[rows][cols - 1] = need[rows - 1][cols] = 1
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            need[r][c] = max(1, min(need[r + 1][c], need[r][c + 1]) - dungeon[r][c])
    return need[0][0]


def _cases():
    import random
    rng = random.Random(174)
    out = []
    for _ in range(10):
        d = [[rng.randint(-10, 6) for _ in range(rng.randint(1, 5))]]
        d += [[rng.randint(-10, 6) for _ in d[0]] for _ in range(rng.randint(0, 4))]
        out.append(((d,), _brute(d)))
    big = [[rng.randint(-1000, 900) for _ in range(200)] for _ in range(200)]
    out.append(((big,), _fast(big)))
    return out


USES = ["dp.grid"]

TESTS = [
    (([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]],), 7),
    (([[0]],), 1),
    (([[-5]],), 6),
    (([[100]],), 1),
    (([[1, -3, 3], [0, -2, 0], [-3, -3, -3]],), 3),
    (([[0, 0], [-4, 10]],), 1),
] + _cases()
