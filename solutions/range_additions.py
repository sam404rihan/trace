def range_additions(n: int, updates: list[list[int]]) -> list[int]:
    # Mark where each update starts and stops; a running total spreads it. O(n + updates).
    diff = [0] * (n + 1)
    for l, r, v in updates:
        diff[l] += v
        diff[r + 1] -= v
    out, running = [], 0
    for i in range(n):
        running += diff[i]
        out.append(running)
    return out
