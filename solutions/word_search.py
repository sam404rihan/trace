def word_search(board: list[str], word: str) -> bool:
    R, C = len(board), len(board[0])
    grid = [list(row) for row in board]

    def dfs(r, c, i):
        if not (0 <= r < R and 0 <= c < C) or grid[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        grid[r][c] = "#"                    # choose: this cell is in use
        found = any(dfs(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        grid[r][c] = word[i]                # un-choose
        return found

    return any(dfs(r, c, 0) for r in range(R) for c in range(C))
