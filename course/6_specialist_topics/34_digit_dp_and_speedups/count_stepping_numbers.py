"""
Count Stepping Numbers in Range                                               [hard]

A stepping number has no leading zero and every two adjacent digits differ by
exactly 1 (like 123, 3434, 98, or any single digit). Count the stepping numbers
in [low, high], both given as strings because they can have up to 100 digits.
Return the count modulo 1_000_000_007.

Example:
    count_stepping_numbers("1", "11")     ->  10      1..9 and 10
    count_stepping_numbers("90", "101")   ->  2       98 and 101

Aim for:  O(digits · 10 · 2 · 2) digit DP.
Hint:     Write count(bound) = stepping numbers in [1, bound]; answer = count(high) - count(low)
          + (1 if low is itself stepping). The digit DP walks bound's digits with state
          (position, previous digit, tight = still equal to bound's prefix, started = placed a
          non-zero digit yet). Before starting, any digit 0..limit is allowed (0 keeps it
          unstarted); after, only previous ± 1.
"""

MOD = 1_000_000_007


def count_stepping_numbers(low: str, high: str) -> int:
    raise NotImplementedError  # replace this line with your solution


def _is_stepping(x):
    s = str(x)
    return all(abs(int(a) - int(b)) == 1 for a, b in zip(s, s[1:]))


def _brute(low, high):
    return sum(_is_stepping(x) for x in range(int(low), int(high) + 1)) % MOD


def _bfs_count(low, high):
    """Generate every stepping number up to high digit by digit (fine up to ~18 digits)."""
    lo, hi = int(low), int(high)
    total, frontier = 0, list(range(1, 10))
    while frontier:
        nxt = []
        for x in frontier:
            if x > hi:
                continue
            if x >= lo:
                total += 1
            d = x % 10
            for nd in (d - 1, d + 1):
                if 0 <= nd <= 9:
                    nxt.append(x * 10 + nd)
        frontier = nxt
    return total % MOD


def _with_digits(length):
    """How many stepping numbers have exactly `length` digits (no upper bound inside)."""
    ends = [0] + [1] * 9                    # by last digit, for length 1 (no leading zero)
    for _ in range(length - 1):
        ends = [(ends[d - 1] if d > 0 else 0) + (ends[d + 1] if d < 9 else 0) for d in range(10)]
    return sum(ends)


def _cases():
    import random
    rng = random.Random(2801)
    out = []
    for _ in range(8):
        a, b = sorted(rng.randint(1, 5000) for _ in range(2))
        out.append(((str(a), str(b)), _brute(str(a), str(b))))
    for _ in range(3):
        a, b = sorted(rng.randint(1, 10**12) for _ in range(2))
        out.append(((str(a), str(b)), _bfs_count(str(a), str(b))))
    every = sum(_with_digits(k) for k in range(1, 101))
    out.append((("1", "9" * 100), every % MOD))
    out.append((("1" + "0" * 99, "9" * 100), _with_digits(100) % MOD))
    out.append((("1" + "0" * 49, "9" * 100), sum(_with_digits(k) for k in range(50, 101)) % MOD))
    return out


USES = ["recursion.memo", "prefix.sums", "dp.digit", "dp.digit_started"]

TESTS = [
    (("1", "11"), 10),
    (("90", "101"), 2),
    (("1", "1"), 1),
    (("10", "10"), 1),
    (("11", "11"), 0),
] + _cases()
