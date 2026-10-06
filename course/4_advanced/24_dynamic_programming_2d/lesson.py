"""
# Dynamic programming (2D)

Same recipe as 1D, but the state needs two numbers: a position in each of
two strings, a cell in a grid, or "first i items with capacity w".

## Use it when
- **Two strings:** edit distance, longest common subsequence, "is s a subsequence/interleaving of t"
- **Grids:** number of paths, minimum path sum, largest square
- **Items + budget:** 0/1 knapsack, "can a subset sum to target"

## The shapes
**Two strings:** `dp[i][j]` = answer for `a[:i]` and `b[:j]`
```
if a[i-1] == b[j-1]: dp[i][j] = dp[i-1][j-1] + ...     # use both characters
else:                dp[i][j] = best of dp[i-1][j], dp[i][j-1], (dp[i-1][j-1])
```
Row 0 and column 0 are the "one string is empty" base cases.

**Grids:** `dp[r][c]` comes from the cell above and the cell to the left:
`dp[r][c] = dp[r-1][c] + dp[r][c-1]`

**Knapsack:** `dp[i][w]` = best value using the first i items with capacity w:
`dp[i][w] = max(dp[i-1][w], dp[i-1][w - weight] + value)` (skip it or take it)

## Tips
- Add an extra row and column of base cases so `i - 1` never goes out of range
- Draw the table on paper for a tiny example first. Fill 3 or 4 cells by hand
- **Space saving:** if each row only needs the previous row, keep two rows (or one).
  For 0/1 knapsack in a single row, loop the capacity BACKWARDS so each item is used once
- Top-down `@cache def solve(i, j)` is often easier to get right. Convert later if needed

## Common mistakes
- Building the grid with `[[0] * cols] * rows` (all rows are the same list!)
- Mixing up "first i characters" (dp index) with "character i" (string index): `a[i-1]`
- Looping capacity forwards in 1-row knapsack, which lets an item be taken twice

Press Run to see a filled-in table.
"""
a, b = "kitten", "sitting"
rows, cols = len(a) + 1, len(b) + 1
dp = [[0] * cols for _ in range(rows)]
for i in range(rows):
    dp[i][0] = i                     # delete everything
for j in range(cols):
    dp[0][j] = j                     # insert everything
for i in range(1, rows):
    for j in range(1, cols):
        if a[i - 1] == b[j - 1]:
            dp[i][j] = dp[i - 1][j - 1]
        else:
            dp[i][j] = 1 + min(dp[i - 1][j],      # delete
                               dp[i][j - 1],      # insert
                               dp[i - 1][j - 1])  # replace

print(f"edit distance table for {a!r} -> {b!r}:\n")
print("      " + "  ".join(" " + ch for ch in "-" + b))
for i in range(rows):
    print(f"  {('-' + a)[i]}  " + "  ".join(f"{v:>2}" for v in dp[i]))
print(f"\nanswer (bottom-right): {dp[-1][-1]}")

# Paths through a grid, with one blocked cell
grid_rows, grid_cols, blocked = 3, 4, {(1, 1)}
paths = [[0] * grid_cols for _ in range(grid_rows)]
for r in range(grid_rows):
    for c in range(grid_cols):
        if (r, c) in blocked:
            continue
        if r == 0 and c == 0:
            paths[r][c] = 1
        else:
            paths[r][c] = (paths[r - 1][c] if r else 0) + (paths[r][c - 1] if c else 0)
print("\npaths to each cell (X = blocked):")
for r in range(grid_rows):
    print("  " + " ".join(" X" if (r, c) in blocked else f"{paths[r][c]:>2}" for c in range(grid_cols)))
