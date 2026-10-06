"""
Count the Coprimes                                                            [medium]

Return how many integers k in 1..n have gcd(k, n) == 1. This is Euler's totient,
phi(n). n can be up to 10^12.

Example:
    euler_phi(9)   ->  6        1, 2, 4, 5, 7, 8
    euler_phi(1)   ->  1
    euler_phi(13)  ->  12       every number below a prime is coprime to it

Aim for:  O(sqrt(n)).
Hint:     phi(n) = n · Π (1 - 1/p) over the distinct primes p dividing n. Factor n by trial
          division up to sqrt(n): for each prime p you find, do result -= result // p, then
          divide all the p's out of n. Whatever is left above 1 is one more prime factor.
"""
from math import gcd


def euler_phi(n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(n):
    result, m, p = n, n, 2
    while p * p <= m:
        if m % p == 0:
            while m % p == 0:
                m //= p
            result -= result // p
        p += 1
    if m > 1:
        result -= result // m
    return result


TESTS = [((9,), 6), ((1,), 1), ((13,), 12), ((10,), 4), ((36,), 12), ((97 * 89,), 96 * 88)] \
    + [((n,), sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)) for n in (2, 64, 210, 1000, 997)] \
    + [((n,), _ref(n)) for n in (999_999_999_989, 2**40, 735_134_400_000, 999_966_000_289)]
