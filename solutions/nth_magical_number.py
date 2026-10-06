MOD = 1_000_000_007


def nth_magical_number(n: int, a: int, b: int) -> int:
    lcm = a * b // gcd(a, b)

    def magical_up_to(x):
        return x // a + x // b - x // lcm       # multiples of both were counted twice

    lo, hi = 1, n * min(a, b)                   # the n-th multiple of the smaller one is enough
    while lo < hi:
        mid = (lo + hi) // 2
        if magical_up_to(mid) >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo % MOD
