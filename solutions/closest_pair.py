def closest_pair(points: list[list[int]]) -> int:
    pts = sorted(map(tuple, points))            # by x, then y
    best = inf                                  # squared distance
    window = []                                 # (y, x) of recent points, sorted by y
    left = 0                                    # pts[left:i] are the ones in the window
    for x, y in pts:
        d = isqrt(best) + 1 if best < inf else inf
        while left < len(pts) and x - pts[left][0] > d:     # too far left to matter
            px, py = pts[left]
            window.pop(bisect_left(window, (py, px)))
            left += 1
        lo = bisect_left(window, (y - d, -inf))
        hi = bisect_right(window, (y + d, inf))
        for wy, wx in window[lo:hi]:            # only a handful fit in the d x 2d box
            best = min(best, (x - wx) ** 2 + (y - wy) ** 2)
        insort(window, (y, x))
    return best
