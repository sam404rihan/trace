def max_value_of_equation(points: list[list[int]], k: int) -> int:
    window = deque()                # (y - x, x) of earlier points, y - x decreasing
    best = float("-inf")
    for x, y in points:
        while window and x - window[0][1] > k:
            window.popleft()                    # too far to the left for this or any later j
        if window:
            best = max(best, window[0][0] + y + x)
        while window and window[-1][0] <= y - x:
            window.pop()                        # the new point is closer and at least as good
        window.append((y - x, x))
    return best
