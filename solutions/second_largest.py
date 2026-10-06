def second_largest(nums: list[int]) -> int | None:
    # One pass tracking the top two distinct values. O(n), O(1) space.
    best = second = float("-inf")
    for x in nums:
        if x > best:
            best, second = x, best      # old best slides down to second
        elif best > x > second:          # strictly between: ignores duplicates of best
            second = x
    return None if second == float("-inf") else second

    # Shortcut, O(n log n):
    #   distinct = sorted(set(nums))
    #   return distinct[-2] if len(distinct) >= 2 else None
