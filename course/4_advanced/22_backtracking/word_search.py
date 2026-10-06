"""
Word Search                                                                   [medium]

The board is a list of strings (rows of letters). Return True if `word` can
be traced through horizontally or vertically adjacent cells, using each cell
at most once.

Example:
    board ["ABCE", "SFCS", "ADEE"]:   "ABCCED" -> True,  "SEE" -> True,  "ABCB" -> False

Aim for:  DFS with backtracking. Mark the cell as used while exploring from it, then unmark it.
Hint:     dfs(r, c, i): fail if out of bounds, used, or board[r][c] != word[i]. Succeed when
          i == len(word) - 1. Otherwise mark, try the 4 neighbours with i + 1, and unmark.
"""


def word_search(board: list[str], word: str) -> bool:
    raise NotImplementedError  # replace this line with your solution


def _exists(board, word):
    R, C = len(board), len(board[0])

    def dfs(r, c, i, used):
        if not (0 <= r < R and 0 <= c < C) or (r, c) in used or board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        used.add((r, c))
        ok = any(dfs(r + dr, c + dc, i + 1, used) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        used.discard((r, c))
        return ok
    return any(dfs(r, c, 0, set()) for r in range(R) for c in range(C))


def _cases():
    import random
    rng = random.Random(83)
    out = []
    for _ in range(8):
        R, C = rng.randint(1, 4), rng.randint(1, 4)
        board = ["".join(rng.choice("ab") for _ in range(C)) for _ in range(R)]
        w = "".join(rng.choice("ab") for _ in range(rng.randint(1, 7)))
        out.append(((board, w), _exists(board, w)))
    return out


B = ["ABCE", "SFCS", "ADEE"]
TESTS = [((B, "ABCCED"), True), ((B, "SEE"), True), ((B, "ABCB"), False), ((["a"], "a"), True),
         ((["aa"], "aaa"), False)] + _cases()
