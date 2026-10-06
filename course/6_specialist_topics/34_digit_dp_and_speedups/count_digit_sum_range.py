"""
Count of Integers With Digit Sum in Range                                     [hard]

Count the integers x with num1 <= x <= num2 whose digit sum is between min_sum
and max_sum (inclusive). num1 and num2 are strings of up to 22 digits, so you
can't loop over the range. Return the count modulo 1_000_000_007.

Example:
    count_digit_sum_range("1", "12", 1, 8)  ->  11       1..8, 10, 11, 12
    count_digit_sum_range("1", "5", 1, 5)   ->  5

Aim for:  O(digits · max_sum · 10) digit DP.
Hint:     Let f(bound) = how many x in [0, bound] have a digit sum in range. The answer is
          f(num2) - f(num1) + (1 if num1 itself qualifies). The DP walks the digits with state
          (position, digit sum so far, tight). Stop early once the sum passes max_sum.
"""

MOD = 1_000_000_007


def count_digit_sum_range(num1: str, num2: str, min_sum: int, max_sum: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(num1, num2, lo, hi):
    return sum(lo <= sum(map(int, str(x))) <= hi for x in range(int(num1), int(num2) + 1)) % MOD


def _sums_with_free_digits(k, cap):
    """ways[s]: how many k-digit strings (leading zeros allowed) have digit sum s, s <= cap."""
    ways = [1] + [0] * cap
    for _ in range(k):
        nxt = [0] * (cap + 1)
        for s, w in enumerate(ways):
            if w:
                for d in range(10):
                    if s + d <= cap:
                        nxt[s + d] += w
        ways = nxt
    return ways


def _upto(bound, lo, hi):
    """Count x in [0, bound] with lo <= digit sum <= hi, by fixing a prefix of bound and
    letting the rest be free: an independent way to get the same numbers."""
    digits = [int(c) for c in bound]
    total, prefix = 0, 0
    for i, top in enumerate(digits):
        free = _sums_with_free_digits(len(digits) - i - 1, hi)
        for d in range(top):                    # place a smaller digit here; the rest are free
            base = prefix + d
            total += sum(free[s - base] for s in range(max(lo, base), hi + 1) if s - base < len(free))
        prefix += top
    total += lo <= prefix <= hi                 # bound itself
    return total


def _ref(num1, num2, lo, hi):
    first = sum(map(int, num1))
    return (_upto(num2, lo, hi) - _upto(num1, lo, hi) + (lo <= first <= hi)) % MOD


def _cases():
    import random
    rng = random.Random(2719)
    out = []
    for _ in range(8):
        a, b = sorted(rng.randint(1, 3000) for _ in range(2))
        lo = rng.randint(1, 20)
        hi = rng.randint(lo, 30)
        out.append(((str(a), str(b), lo, hi), _brute(str(a), str(b), lo, hi)))
    for _ in range(3):
        a, b = sorted(rng.randint(1, 10**22 - 1) for _ in range(2))
        lo = rng.randint(1, 100)
        hi = rng.randint(lo, 200)
        out.append(((str(a), str(b), lo, hi), _ref(str(a), str(b), lo, hi)))
    return out


TESTS = [
    (("1", "12", 1, 8), 11),
    (("1", "5", 1, 5), 5),
    (("1", "1", 1, 1), 1),
    (("10", "10", 2, 400), 0),
    (("1", "9999999999999999999999", 1, 400), (10**22 - 1) % MOD),
] + _cases()
