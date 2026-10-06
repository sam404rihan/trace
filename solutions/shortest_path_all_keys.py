def shortest_path_all_keys(grid: list[str]) -> int:
    rows, cols = len(grid), len(grid[0])
    keys = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "@":
                start = (r, c)
            elif grid[r][c].islower():
                keys += 1
    all_keys = (1 << keys) - 1

    seen = {(*start, 0)}
    queue = deque([(*start, 0, 0)])         # (row, col, keys held as a bitmask, steps)
    while queue:
        r, c, mask, steps = queue.popleft()
        if mask == all_keys:
            return steps
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            ch = grid[nr][nc]
            if ch == "#":
                continue
            if ch.isupper() and not mask & (1 << (ord(ch) - ord("A"))):
                continue                    # locked, and we don't have the key yet
            new_mask = mask | (1 << (ord(ch) - ord("a"))) if ch.islower() else mask
            if (nr, nc, new_mask) not in seen:
                seen.add((nr, nc, new_mask))
                queue.append((nr, nc, new_mask, steps + 1))
    return -1
