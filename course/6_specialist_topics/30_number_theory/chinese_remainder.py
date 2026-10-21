"""
Chinese Remainder Theorem                                                     [hard]

Find the smallest non-negative x with  x % mods[i] == rems[i]  for every i.
The moduli are NOT necessarily coprime, so there may be no answer: return -1
then. Moduli are >= 1 and can be large (the answer can have dozens of digits).

Example:
    chinese_remainder([2, 3, 2], [3, 5, 7])   ->  23       23 = 2 mod 3, 3 mod 5, 2 mod 7
    chinese_remainder([1, 3], [4, 6])         ->  9        mods share a factor 2, but it's consistent
    chinese_remainder([1, 2], [4, 6])         ->  -1       x would be odd and even at once

Aim for:  O(k log M) with extended Euclid, merging the conditions two at a time.
Hint:     Keep a combined condition x ≡ r (mod m), starting with r = 0, m = 1. To merge
          x ≡ r2 (mod m2): write x = r + m·t, so you need m·t ≡ r2 - r (mod m2). With
          g = gcd(m, m2), that's solvable only if g divides r2 - r. Then
          t ≡ ((r2 - r) / g) · inverse(m / g) (mod m2 / g), and the new modulus is lcm(m, m2).
          Python's pow(x, -1, mod) gives modular inverses.
"""


def chinese_remainder(rems: list[int], mods: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(rems, mods):
    from math import lcm
    limit = 1
    for m in mods:
        limit = lcm(limit, m)
    for x in range(limit):
        if all(x % m == r % m for r, m in zip(rems, mods)):
            return x
    return -1


def _merge(rems, mods):
    from math import gcd
    r, m = 0, 1
    for r2, m2 in zip(rems, mods):
        g = gcd(m, m2)
        if (r2 - r) % g:
            return -1
        t = ((r2 - r) // g) * pow(m // g, -1, m2 // g) % (m2 // g) if m2 // g > 1 else 0
        r, m = r + m * t, m // g * m2
        r %= m
    return r


def _cases():
    import random
    rng = random.Random(3)
    out = []
    for _ in range(10):
        mods = [rng.randint(1, 12) for _ in range(rng.randint(1, 4))]
        rems = [rng.randrange(m) for m in mods]
        out.append(((rems, mods), _brute(rems, mods)))
    primes = [1_000_000_007, 998_244_353, 1_000_000_009, 2_147_483_647, 999_999_937]
    x = rng.randrange(10**40)
    out.append((([x % p for p in primes], primes), _merge([x % p for p in primes], primes)))
    mods = [2**20 * 3, 2**15 * 5**6, 3**10 * 7]
    x = rng.randrange(10**20)
    out.append((([x % m for m in mods], mods), _merge([x % m for m in mods], mods)))
    return out


USES = ["nt.mod_inverse"]

TESTS = [
    (([2, 3, 2], [3, 5, 7]), 23),
    (([1, 3], [4, 6]), 9),
    (([1, 2], [4, 6]), -1),
    (([0], [1]), 0),
    (([5], [7]), 5),
    (([3, 3], [6, 6]), 3),
    (([3, 4], [6, 6]), -1),
] + _cases()
