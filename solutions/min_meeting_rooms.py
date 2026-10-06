def min_meeting_rooms(intervals: list[list[int]]) -> int:
    ends, best = [], 0                      # min-heap of end times of rooms in use
    for start, end in sorted(intervals):
        if ends and ends[0] <= start:
            heappop(ends)                   # that room is free again
        heappush(ends, end)
        best = max(best, len(ends))
    return best
