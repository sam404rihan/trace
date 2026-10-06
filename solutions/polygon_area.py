def polygon_area(points: list[tuple[int, int]]) -> float:
    twice = 0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]      # wrap around to the first corner
        twice += x1 * y2 - x2 * y1
    return abs(twice) / 2
