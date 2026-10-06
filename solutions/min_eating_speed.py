def min_eating_speed(piles: list[int], h: int) -> int:
    # Binary search on the speed. Faster never takes longer, so "fits in h hours"
    # flips from False to True exactly once. O(n log max(piles)).
    def hours(speed):
        return sum((p + speed - 1) // speed for p in piles)   # ceil(p / speed) without floats

    lo, hi = 1, max(piles)          # max(piles) always works: one pile per hour
    while lo < hi:
        mid = (lo + hi) // 2
        if hours(mid) <= h:
            hi = mid                # fast enough: maybe slower works too
        else:
            lo = mid + 1
    return lo
