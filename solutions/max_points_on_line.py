def max_points_on_line(points: list[tuple[int, int]]) -> int:
    if len(points) <= 2:
        return len(points)
    best = 0
    for i, (x1, y1) in enumerate(points):
        directions = Counter()
        for x2, y2 in points[i + 1:]:
            dx, dy = x2 - x1, y2 - y1
            g = gcd(dx, dy)
            dx, dy = dx // g, dy // g
            if dx < 0 or (dx == 0 and dy < 0):     # one canonical sign for each direction
                dx, dy = -dx, -dy
            directions[dx, dy] += 1
        if directions:
            best = max(best, max(directions.values()) + 1)
    return best
