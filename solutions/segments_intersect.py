def segments_intersect(a: tuple[int, int], b: tuple[int, int], c: tuple[int, int], d: tuple[int, int]) -> bool:
    def turn(p, q, r):
        v = (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])
        return (v > 0) - (v < 0)

    def within(p, q, r):                    # r inside the bounding box of p and q
        return min(p[0], q[0]) <= r[0] <= max(p[0], q[0]) and min(p[1], q[1]) <= r[1] <= max(p[1], q[1])

    o1, o2, o3, o4 = turn(a, b, c), turn(a, b, d), turn(c, d, a), turn(c, d, b)
    if o1 != o2 and o3 != o4:               # each segment straddles the other's line
        return True
    return ((o1 == 0 and within(a, b, c)) or (o2 == 0 and within(a, b, d))
            or (o3 == 0 and within(c, d, a)) or (o4 == 0 and within(c, d, b)))
