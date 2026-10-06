def pacific_atlantic(heights):
    R, C = len(heights), len(heights[0])

    def flood(starts):
        seen, stack = set(starts), list(starts)
        while stack:
            r, c = stack.pop()
            for x, y in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                # walk UPHILL from the ocean: water could flow from (x, y) down to (r, c)
                if 0 <= x < R and 0 <= y < C and (x, y) not in seen and heights[x][y] >= heights[r][c]:
                    seen.add((x, y))
                    stack.append((x, y))
        return seen

    pacific = flood([(0, c) for c in range(C)] + [(r, 0) for r in range(R)])
    atlantic = flood([(R - 1, c) for c in range(C)] + [(r, C - 1) for r in range(R)])
    return sorted([r, c] for r, c in pacific & atlantic)
