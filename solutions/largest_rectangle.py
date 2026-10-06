def largest_rectangle(heights: list[int]) -> int:
    stack, best = [], 0                     # indexes, heights increasing upwards
    for i, h in enumerate(heights + [0]):   # the sentinel 0 flushes the stack at the end
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            best = max(best, height * width)
        stack.append(i)
    return best
