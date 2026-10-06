def dungeon_game(dungeon: list[list[int]]) -> int:
    rows, cols = len(dungeon), len(dungeon[0])
    # need[r][c]: health required when ENTERING room (r, c). Padded with inf on the far edges.
    need = [[inf] * (cols + 1) for _ in range(rows + 1)]
    need[rows][cols - 1] = need[rows - 1][cols] = 1     # after the princess, just stay alive
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            after = min(need[r + 1][c], need[r][c + 1])  # the easier way onward
            need[r][c] = max(1, after - dungeon[r][c])   # never below 1, even after a potion
    return need[0][0]
