def can_attend_meetings(intervals: list[list[int]]) -> bool:
    # After sorting by start, only neighbours can overlap. O(n log n).
    intervals = sorted(intervals)
    for (_, prev_end), (start, _) in zip(intervals, intervals[1:]):
        if start < prev_end:        # starts before the previous one finished
            return False
    return True
