def euler_phi(n: int) -> int:
    result, p = n, 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p          # multiply by (1 - 1/p)
        p += 1
    if n > 1:                              # one prime factor bigger than sqrt is left
        result -= result // n
    return result
