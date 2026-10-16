def grid_illumination(n: int, lamps: list[list[int]], queries: list[list[int]]) -> list[int]:
    # Count lamps per row, column and diagonal (r - c and r + c identify the two diagonals).
    # A query looks up four counts; switching a lamp off takes 1 off each. O(lamps + queries).
    on = set()
    rows, cols, diag, anti = Counter(), Counter(), Counter(), Counter()
    for r, c in lamps:
        if (r, c) in on:
            continue                    # listed twice, still one lamp
        on.add((r, c))
        rows[r] += 1
        cols[c] += 1
        diag[r - c] += 1
        anti[r + c] += 1
    answer = []
    for r, c in queries:
        answer.append(1 if rows[r] or cols[c] or diag[r - c] or anti[r + c] else 0)
        for a in (r - 1, r, r + 1):
            for b in (c - 1, c, c + 1):
                if (a, b) in on:
                    on.remove((a, b))
                    rows[a] -= 1
                    cols[b] -= 1
                    diag[a - b] -= 1
                    anti[a + b] -= 1
    return answer
