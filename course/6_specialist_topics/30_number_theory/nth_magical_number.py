"""
Nth Magical Number                                                            [hard]

A positive integer is "magical" if it's divisible by a or by b. Return the
n-th magical number (1-based), modulo 1_000_000_007. n can be up to 10**9 and
a, b up to 40,000, so you can't list them one by one.

Example:
    nth_magical_number(1, 2, 3)   ->  2
    nth_magical_number(4, 2, 3)   ->  6       2, 3, 4, 6
    nth_magical_number(5, 2, 4)   ->  10      2, 4, 6, 8, 10
    nth_magical_number(3, 6, 4)   ->  8       4, 6, 8

Aim for:  O(log(n · min(a, b))).
Hint:     Count the magical numbers up to x with inclusion-exclusion:
          x // a + x // b - x // lcm(a, b), where lcm = a * b // gcd(a, b). That count only
          grows with x, so binary search for the smallest x whose count is >= n. Take the
          modulo only at the very end.
"""

MOD = 1_000_000_007


def nth_magical_number(n: int, a: int, b: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(n, a, b):
    x, found = 0, 0
    while found < n:
        x += 1
        if x % a == 0 or x % b == 0:
            found += 1
    return x % MOD


def _fast(n, a, b):
    from math import gcd
    lcm = a * b // gcd(a, b)
    lo, hi = 1, n * min(a, b)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid // a + mid // b - mid // lcm >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo % MOD


def _cases():
    import random
    rng = random.Random(878)
    out = []
    for _ in range(8):
        n, a, b = rng.randint(1, 60), rng.randint(2, 12), rng.randint(2, 12)
        out.append(((n, a, b), _brute(n, a, b)))
    for n, a, b in ((10**9, 40_000, 40_000), (10**9, 39_999, 40_000), (987_654_321, 1234, 5678)):
        out.append(((n, a, b), _fast(n, a, b)))
    return out


USES = ["bsearch.first_true", "bsearch.on_answer"]

TESTS = [
    ((1, 2, 3), 2),
    ((4, 2, 3), 6),
    ((5, 2, 4), 10),
    ((3, 6, 4), 8),
    ((7, 5, 5), 35),
    ((1_000_000_000, 40_000, 40_000), 999_720_007),
] + _cases()
