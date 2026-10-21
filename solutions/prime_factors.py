def prime_factors(n: int) -> list[int]:
    # Trial division up to sqrt(n): each prime is divided out as often as it goes in. O(sqrt(n)).
    factors, d = [], 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)                   # one prime factor above the square root is left
    return factors
