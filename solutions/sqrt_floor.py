def sqrt_floor(x: int) -> int:
    # Binary search on the answer: the first r with r*r > x, minus one. O(log x).
    lo, hi = 0, x + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if mid * mid > x:
            hi = mid
        else:
            lo = mid + 1
    return lo - 1

    # In real code: math.isqrt(x)
