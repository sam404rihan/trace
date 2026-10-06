def overlaps(a: list[int], b: list[int]) -> bool:
    # Not overlapping means a ends before b starts, or b ends before a starts. Negate that.
    return a[0] <= b[1] and b[0] <= a[1]
