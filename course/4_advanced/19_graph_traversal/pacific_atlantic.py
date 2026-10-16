"""
Pacific Atlantic Water Flow                                                   [medium]

heights is a grid. The Pacific touches the top and left edges, the Atlantic
the bottom and right edges. Rain flows from a cell to a neighbour (up, down,
left, right) with equal or lower height. Return every [row, col] from which
water can reach BOTH oceans, sorted.

Example:
    [[1, 2, 2, 3, 5],
     [3, 2, 3, 4, 4],
     [2, 4, 5, 3, 1],      ->  [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
     [6, 7, 1, 4, 5],
     [5, 1, 1, 2, 4]]

Aim for:  O(rows · cols). Search FROM the oceans, uphill, not from every cell.
Hint:     Two flood fills. Start one from all Pacific edge cells and one from all Atlantic edge cells,
          moving only to neighbours that are >= the current height. The answer is the intersection.
"""


def pacific_atlantic(heights: list[list[int]]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def _brute(h):
    R, C = len(h), len(h[0])
    out = []
    for r in range(R):
        for c in range(C):
            seen, stack, pac, atl = {(r, c)}, [(r, c)], False, False
            while stack:
                a, b = stack.pop()
                pac |= a == 0 or b == 0
                atl |= a == R - 1 or b == C - 1
                for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                    if 0 <= x < R and 0 <= y < C and (x, y) not in seen and h[x][y] <= h[a][b]:
                        seen.add((x, y))
                        stack.append((x, y))
            if pac and atl:
                out.append([r, c])
    return out


def _cases():
    import random
    rng = random.Random(86)
    out = []
    for _ in range(8):
        R, C = rng.randint(1, 6), rng.randint(1, 6)
        h = [[rng.randint(0, 5) for _ in range(C)] for _ in range(R)]
        out.append(((h,), _brute(h)))
    return out


EX = [[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]]
USES = ["flood.from_targets"]

TESTS = [((EX,), [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]), (([[1]],), [[0, 0]])] + _cases()
