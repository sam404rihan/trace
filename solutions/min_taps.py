def min_taps(n: int, ranges: list[int]) -> int:
    reach = [0] * (n + 1)           # reach[x]: farthest right point a tap covering from x waters
    for i, r in enumerate(ranges):
        left = max(0, i - r)
        reach[left] = max(reach[left], min(n, i + r))
    taps = end = farthest = 0       # end: how far the opened taps water
    for x in range(n):
        farthest = max(farthest, reach[x])
        if x == end:                # about to leave the watered part: open the best tap
            if farthest <= x:
                return -1           # nothing reaches past x
            taps += 1
            end = farthest
    return taps
