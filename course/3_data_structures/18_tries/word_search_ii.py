"""
Word Search II                                                                  [hard]

The board is a list of strings (rows of letters). A word can be traced through
horizontally or vertically adjacent cells, using each cell at most once per
word. Return every word from `words` that appears on the board, sorted
alphabetically, with each word listed once.

Example:
    board ["oaan", "etae", "ihkr", "iflv"], words ["oath", "pea", "eat", "rain"]
    ->  ["eat", "oath"]

Aim for:  one DFS per starting cell that follows a trie of ALL the words at once, rather than
          one full search per word.
Hint:     Build a trie of the words and store the full word at its end node. DFS from every cell,
          moving into the trie as you go, and stop as soon as the current path isn't a trie prefix.
          Clear a word once it's found (and prune empty trie branches) to stay fast.
"""


def word_search_ii(board: list[str], words: list[str]) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _exists(board, word):
    R, C = len(board), len(board[0])

    def dfs(r, c, i, used):
        if board[r][c] != word[i] or (r, c) in used:
            return False
        if i == len(word) - 1:
            return True
        used.add((r, c))
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < R and 0 <= nc < C and dfs(nr, nc, i + 1, used):
                return True
        used.discard((r, c))
        return False
    return any(dfs(r, c, 0, set()) for r in range(R) for c in range(C))


def _cases():
    import random
    rng = random.Random(76)
    out = []
    for _ in range(6):
        R, C = rng.randint(1, 4), rng.randint(1, 4)
        board = ["".join(rng.choice("abc") for _ in range(C)) for _ in range(R)]
        words = ["".join(rng.choice("abc") for _ in range(rng.randint(1, 5))) for _ in range(8)]
        out.append(((board, words), sorted({w for w in words if _exists(board, w)})))
    return out


TESTS = [((["oaan", "etae", "ihkr", "iflv"], ["oath", "pea", "eat", "rain"]), ["eat", "oath"]),
         ((["ab", "cd"], ["abcb"]), []), ((["a"], ["a", "a"]), ["a"]), ((["ab", "cd"], ["acdb", "abdc", "ad"]), ["abdc", "acdb"])] + _cases()
