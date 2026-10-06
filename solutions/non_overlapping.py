def non_overlapping(intervals: list[list[int]]) -> int:
    removed, last_end = 0, float("-inf")
    for start, end in sorted(intervals, key=lambda iv: iv[1]):   # earliest end leaves the most room
        if start >= last_end:
            last_end = end
        else:
            removed += 1
    return removed
