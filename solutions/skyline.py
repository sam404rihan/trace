def skyline(buildings: list[list[int]]) -> list[list[int]]:
    xs = sorted({b[0] for b in buildings} | {b[1] for b in buildings})
    by_left = sorted(buildings)
    overhead = []                           # (-height, right): tallest on top
    i, outline = 0, []
    for x in xs:
        while i < len(by_left) and by_left[i][0] <= x:      # buildings that have started
            heappush(overhead, (-by_left[i][2], by_left[i][1]))
            i += 1
        while overhead and overhead[0][1] <= x:             # the tallest one already ended
            heappop(overhead)                               # (shorter ended ones can wait)
        height = -overhead[0][0] if overhead else 0
        if not outline or outline[-1][1] != height:
            outline.append([x, height])
    return outline
