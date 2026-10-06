def count_primes(n: int) -> int:
    if n < 3:
        return 0
    is_prime = bytearray([1]) * n
    is_prime[0] = is_prime[1] = 0
    for p in range(2, isqrt(n - 1) + 1):
        if is_prime[p]:
            is_prime[p * p::p] = bytes(len(range(p * p, n, p)))     # cross out p*p, p*p + p, ...
    return sum(is_prime)
