def ship_capacity(weights: list[int], days: int) -> int:
    def fits(cap):
        used, load = 1, 0
        for w in weights:
            if load + w > cap:          # doesn't fit today: sail, start a new day
                used, load = used + 1, 0
            load += w
        return used <= days

    # The answer lies in [heaviest package, everything at once], and fits() flips once.
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if fits(mid):
            hi = mid                    # works: the answer is mid or smaller
        else:
            lo = mid + 1                # too small: the answer is bigger
    return lo
