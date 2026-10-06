def solve_sudoku(board: list[str]) -> list[str]:
    grid = [list(row) for row in board]
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    empty = []
    for r in range(9):
        for c in range(9):
            d = grid[r][c]
            if d == ".":
                empty.append((r, c))
            else:
                rows[r].add(d)
                cols[c].add(d)
                boxes[r // 3 * 3 + c // 3].add(d)

    def options(r, c):
        used = rows[r] | cols[c] | boxes[r // 3 * 3 + c // 3]
        return [d for d in "123456789" if d not in used]

    def solve():
        if not empty:
            return True
        # Most constrained cell first: fewest legal digits means the least branching.
        i = min(range(len(empty)), key=lambda j: len(options(*empty[j])))
        r, c = empty.pop(i)
        b = r // 3 * 3 + c // 3
        for d in options(r, c):
            grid[r][c] = d                                  # choose
            rows[r].add(d); cols[c].add(d); boxes[b].add(d)
            if solve():                                     # explore
                return True
            rows[r].remove(d); cols[c].remove(d); boxes[b].remove(d)   # un-choose
        grid[r][c] = "."
        empty.insert(i, (r, c))
        return False

    solve()
    return ["".join(row) for row in grid]
