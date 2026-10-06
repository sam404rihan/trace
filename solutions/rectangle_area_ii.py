MOD = 1_000_000_007


def rectangle_area_ii(rectangles: list[list[int]]) -> int:
    events = []                     # (x, +1 start / -1 end, y1, y2)
    for x1, y1, x2, y2 in rectangles:
        events.append((x1, 1, y1, y2))
        events.append((x2, -1, y1, y2))
    events.sort()

    active = []                     # y-intervals of the rectangles the sweep line is inside
    total, prev_x = 0, events[0][0]
    for x, kind, y1, y2 in events:
        covered, reach = 0, -inf    # length of the union of the active y-intervals
        for low, high in sorted(active):
            low = max(low, reach)
            if high > low:
                covered += high - low
                reach = high
        total += covered * (x - prev_x)     # constant between consecutive events
        prev_x = x
        if kind == 1:
            active.append((y1, y2))
        else:
            active.remove((y1, y2))
    return total % MOD
