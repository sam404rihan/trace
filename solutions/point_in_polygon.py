def point_in_polygon(polygon: list[tuple[int, int]], point: tuple[int, int]) -> str:
    x, y = point
    n = len(polygon)
    inside = False
    for i in range(n):
        (x1, y1), (x2, y2) = polygon[i], polygon[(i + 1) % n]
        if ((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1) == 0                  # on this edge's line...
                and min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2)):   # ...and between its ends
            return "boundary"
        if (y1 > y) != (y2 > y):            # the edge crosses the horizontal line through the point
            side = (x2 - x1) * (y - y1) - (x - x1) * (y2 - y1)
            if (side > 0) == (y2 > y1):     # and the crossing is to the right of the point
                inside = not inside
    return "inside" if inside else "outside"
