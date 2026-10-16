"""
Grid Illumination                                                             [hard]

An n x n grid has lamps at the cells in `lamps`. A cell can be listed more than
once; it's still one lamp. A lamp lights every cell in its row, its column and
both of its diagonals. For each query [r, c], in order:

  1. answer 1 if cell (r, c) is lit, else 0;
  2. then turn off every lamp in the 3 x 3 block centred on (r, c).

Return the answers. n can be 1,000,000,000, with 20,000 lamps and 20,000
queries, so you can't build the grid or check every lamp for every query.

Example:
    grid_illumination(5, [[0, 0], [4, 4]], [[1, 1], [1, 0]])  ->  [1, 0]
        (1, 1) is on the diagonal of both lamps: lit. Then the lamp at (0, 0) goes off.
        (1, 0) shares no row, column or diagonal with the lamp left at (4, 4): dark.

Aim for:  O(lamps + queries).
Hint:     All cells on one diagonal share r - c, and on the other diagonal r + c. Keep four
          dicts that count the lamps on each row, column, r - c and r + c, plus a set of the
          lamps that are on. A cell is lit if any of its four counts is above 0. Turning a
          lamp off means removing it from the set and taking 1 off each of its four counts.
"""


def grid_illumination(n: int, lamps: list[list[int]], queries: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _brute(n, lamps, queries):
    on = {tuple(lamp) for lamp in lamps}
    out = []
    for r, c in queries:
        out.append(int(any(a == r or b == c or a - b == r - c or a + b == r + c for a, b in on)))
        on = {(a, b) for a, b in on if max(abs(a - r), abs(b - c)) > 1}
    return out


def _fast(n, lamps, queries):
    on = {tuple(lamp) for lamp in lamps}
    lines = {}
    for r, c in on:
        for key in (("row", r), ("col", c), ("diag", r - c), ("anti", r + c)):
            lines[key] = lines.get(key, 0) + 1
    out = []
    for r, c in queries:
        out.append(int(any(lines.get(k, 0) for k in (("row", r), ("col", c), ("diag", r - c), ("anti", r + c)))))
        for a in (r - 1, r, r + 1):
            for b in (c - 1, c, c + 1):
                if (a, b) in on:
                    on.remove((a, b))
                    for key in (("row", a), ("col", b), ("diag", a - b), ("anti", a + b)):
                        lines[key] -= 1
    return out


def _cases():
    import random
    rng = random.Random(1001)
    out = []
    for _ in range(8):
        n = rng.randint(1, 8)
        lamps = [[rng.randrange(n), rng.randrange(n)] for _ in range(rng.randint(0, 8))]
        queries = [[rng.randrange(n), rng.randrange(n)] for _ in range(rng.randint(1, 8))]
        out.append(((n, lamps, queries), _brute(n, lamps, queries)))
    lamps = [[rng.randrange(3000), rng.randrange(3000)] for _ in range(20_000)]
    queries = [[rng.randrange(3000), rng.randrange(3000)] for _ in range(20_000)]
    out.append(((1_000_000_000, lamps, queries), _fast(1_000_000_000, lamps, queries)))
    return out


USES = ["hash.group_key", "hash.set_lookup"]

TESTS = [
    ((5, [[0, 0], [4, 4]], [[1, 1], [1, 0]]), [1, 0]),
    ((5, [[0, 0], [4, 4]], [[1, 1], [1, 1]]), [1, 1]),
    ((5, [[0, 0], [0, 4]], [[0, 4], [0, 1], [1, 4]]), [1, 1, 0]),
    ((1, [[0, 0], [0, 0]], [[0, 0], [0, 0]]), [1, 0]),
    ((3, [], [[1, 1]]), [0]),
    ((6, [[2, 3], [2, 3]], [[0, 0], [2, 2], [5, 0]]), [0, 1, 0]),
] + _cases()
