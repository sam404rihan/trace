from functools import cache


def climb_stairs(n: int) -> int:
    # Bottom-up: ways(n) = ways(n-1) + ways(n-2) — it's Fibonacci! O(n), O(1).
    one_back, two_back = 1, 1          # ways(1), ways(0)
    for _ in range(n - 1):
        one_back, two_back = one_back + two_back, one_back
    return one_back


@cache                                   # memoisation: each n is computed once
def climb_stairs_memo(n: int) -> int:
    # Top-down: same recursion as the naive version, O(n) thanks to the cache.
    # Without @cache this makes ~2ⁿ calls, which is why n = 45 times out.
    if n <= 2:
        return n
    return climb_stairs_memo(n - 1) + climb_stairs_memo(n - 2)
