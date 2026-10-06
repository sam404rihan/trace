def maximal_rectangle(grid: list[str]) -> int:
    cols = len(grid[0])
    heights = [0] * (cols + 1)          # the extra 0 at the end flushes the stack
    best = 0
    for row in grid:
        for j, ch in enumerate(row):
            heights[j] = heights[j] + 1 if ch == "1" else 0
        stack = [-1]                    # indices with increasing heights
        for j, h in enumerate(heights):
            while stack[-1] != -1 and heights[stack[-1]] >= h:
                height = heights[stack.pop()]
                width = j - stack[-1] - 1       # it spans from the bar below it to j
                best = max(best, height * width)
            stack.append(j)
    return best
