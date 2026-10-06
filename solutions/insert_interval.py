def insert_interval(intervals: list[list[int]], new: list[int]) -> list[list[int]]:
    out, i, n = [], 0, len(intervals)
    start, end = new
    while i < n and intervals[i][1] < start:        # 1) entirely before new
        out.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= end:         # 2) overlaps new: absorb it
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    out.append([start, end])
    out.extend(intervals[i:])                       # 3) entirely after new
    return out
