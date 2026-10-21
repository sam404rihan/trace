"""
Factor Them All                                                                 [hard]

Given up to 100,000 numbers, each between 2 and 1,000,000, return the prime
factorisation of each one: its prime factors in ascending order, repeated as often
as they divide it.

Example:
    factorize_all([12, 7, 1000])  ->  [[2, 2, 3], [7], [2, 2, 2, 5, 5, 5]]

Aim for:  one sieve up to max(nums), then O(log x) per number.
Hint:     Trial division costs up to sqrt(x) ≈ 1000 steps for a large prime, and there are
          100,000 numbers. Instead build spf[x] = the smallest prime factor of x with a sieve.
          Then x factors as spf[x], then spf[x // spf[x]], and so on down to 1.
"""
from math import isqrt


def factorize_all(nums: list[int]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def _primes(lo, hi):
    flags = bytearray([1]) * (hi + 1)
    flags[0:2] = b"\x00\x00"
    for p in range(2, isqrt(hi) + 1):
        if flags[p]:
            flags[p * p::p] = bytes(len(range(p * p, hi + 1, p)))
    return [i for i in range(max(lo, 2), hi + 1) if flags[i]]


def _big():
    import random
    rng = random.Random(3008)
    big = _primes(500_000, 1_000_000)
    small = _primes(600, 1000)
    nums, want = [], []
    for _ in range(100_000):
        if rng.random() < 0.6:
            p = rng.choice(big)
            nums.append(p); want.append([p])
        else:
            p, q = sorted((rng.choice(small), rng.choice(small)))
            nums.append(p * q); want.append([p, q])
    return ((nums,), want)


def _naive(x):
    out, d = [], 2
    while d * d <= x:
        while x % d == 0:
            out.append(d); x //= d
        d += 1
    return out + ([x] if x > 1 else [])


_MIXED = [2, 3, 4, 97, 128, 360, 997_920, 999_983, 1_000_000, 65_536, 30_030, 524_287, 999_999]

USES = ["nt.sieve"]

TESTS = [(([12, 7, 1000],), [[2, 2, 3], [7], [2, 2, 2, 5, 5, 5]]), (([2],), [[2]]),
         ((_MIXED,), [_naive(x) for x in _MIXED]), _big()]
