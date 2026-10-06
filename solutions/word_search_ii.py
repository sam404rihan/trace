def word_search_ii(board: list[str], words: list[str]) -> list[str]:
    root = {}
    for w in words:                         # trie of every word; "$" holds the full word at its end
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w
    R, C = len(board), len(board[0])
    grid = [list(row) for row in board]
    found = []

    def dfs(r, c, parent):
        ch = grid[r][c]
        node = parent.get(ch)
        if node is None:
            return
        if "$" in node:
            found.append(node.pop("$"))     # record once
        grid[r][c] = "#"                    # mark used for this path
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < R and 0 <= nc < C and grid[nr][nc] != "#":
                dfs(nr, nc, node)
        grid[r][c] = ch
        if not node:                        # prune: nothing left to find down this branch
            parent.pop(ch)

    for r in range(R):
        for c in range(C):
            dfs(r, c, root)
    return sorted(found)
