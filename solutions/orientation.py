def orientation(p: tuple[int, int], q: tuple[int, int], r: tuple[int, int]) -> int:
    cross = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
    return (cross > 0) - (cross < 0)
