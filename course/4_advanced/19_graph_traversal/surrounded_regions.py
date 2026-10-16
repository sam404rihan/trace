"""
Surrounded Regions                                                            [medium]

The board is a list of strings of "X" and "O". Capture every region of "O"s
that is completely surrounded by "X" (it doesn't touch the border) by turning
it into "X". Return the new board.

Example:
    ["XXXX", "XOOX", "XXOX", "XOXX"]   ->   ["XXXX", "XXXX", "XXXX", "XOXX"]
    (the bottom "O" touches the border, so it survives)

Hint:     Turn it around: flood fill from every border "O" and mark those cells safe.
          Everything that's still an unmarked "O" afterwards is surrounded.
"""


def surrounded_regions(board: list[str]) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _brute(board):
    R, C = len(board), len(board[0])
    out = [list(row) for row in board]
    seen = set()
    for r in range(R):
        for c in range(C):
            if board[r][c] == "O" and (r, c) not in seen:
                comp, stack, border = [], [(r, c)], False
                seen.add((r, c))
                while stack:
                    a, b = stack.pop()
                    comp.append((a, b))
                    border |= a in (0, R - 1) or b in (0, C - 1)
                    for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                        if 0 <= x < R and 0 <= y < C and board[x][y] == "O" and (x, y) not in seen:
                            seen.add((x, y))
                            stack.append((x, y))
                if not border:
                    for a, b in comp:
                        out[a][b] = "X"
    return ["".join(r) for r in out]


def _cases():
    import random
    rng = random.Random(87)
    out = []
    for _ in range(8):
        R, C = rng.randint(1, 7), rng.randint(1, 7)
        b = ["".join(rng.choice("XXO") for _ in range(C)) for _ in range(R)]
        out.append(((b,), _brute(b)))
    return out


USES = ["flood.from_targets"]

TESTS = [((["XXXX", "XOOX", "XXOX", "XOXX"],), ["XXXX", "XXXX", "XXXX", "XOXX"]), ((["X"],), ["X"]), ((["O"],), ["O"]),
         ((["OOO", "OXO", "OOO"],), ["OOO", "OXO", "OOO"])] + _cases()
