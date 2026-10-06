def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    # Sort by start, then each interval either extends the last merged one or
    # starts a new one. O(n log n).
    merged = []
    for start, end in sorted(intervals, key=lambda iv: iv[0]):
        if merged and start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)   # max: [1, 10] swallows [2, 3]
        else:
            merged.append([start, end])
    return merged
