"""
# Number theory

Integers have structure: every number factors into primes in exactly one way, and
arithmetic "mod m" wraps around like a clock. Interview and contest problems lean on a
handful of tools built from those two facts.

## Use it when
- "Return the answer modulo 1,000,000,007": the true answer is huge, so reduce as you go
- Counting primes, factoring many numbers, divisors, gcd/lcm
- nCr for big n, or "how many ways" answers that need division mod p
- Anything about remainders, cycles of length m, or "coprime"

## The toolkit
```
gcd(a, b) = gcd(b, a % b), gcd(a, 0) = a        O(log min(a, b))
fast power: square the base, halve the exponent  O(log e) multiplications
sieve: cross out multiples of each prime p from p*p   O(n log log n)
smallest-prime-factor sieve: factor any x <= n in O(log x)
(a * b) % m == ((a % m) * (b % m)) % m          reduce after every step
```

## Division mod a prime
You can't divide mod p directly, but you can multiply by an inverse:
a / b == a * b^(p-2)   (mod p)        Fermat, p prime and b not a multiple of p
For any modulus, extended Euclid finds x with b*x + m*y = 1 when gcd(b, m) = 1.

## Common mistakes
- Reducing only at the end: Python won't overflow, but the numbers get slow and huge
- Sieving from 2*p instead of p*p (correct, just slower)
- (a - b) % m in other languages can be negative; Python's % is never negative for m > 0
- Trial division up to n instead of sqrt(n)
"""


def mod_pow(base, exp, mod):
    result = 1
    base %= mod
    while exp:
        if exp & 1:                      # this bit of the exponent is set
            result = result * base % mod
        base = base * base % mod         # base, base^2, base^4, base^8, ...
        exp >>= 1
    return result


def sieve(n):
    is_prime = bytearray([1]) * (n + 1)
    is_prime[0:2] = b"\x00\x00"
    for p in range(2, int(n ** 0.5) + 1):
        if is_prime[p]:
            is_prime[p * p::p] = bytes(len(range(p * p, n + 1, p)))
    return [i for i in range(n + 1) if is_prime[i]]


print("3^200 mod 13 =", mod_pow(3, 200, 13), "  (Python's pow agrees:", pow(3, 200, 13), ")")
print("primes up to 50:", sieve(50))
print("gcd(84, 36) =", gcd(84, 36), "  lcm =", lcm(84, 36))
MOD = 1_000_000_007
print("2 / 3 mod p =", 2 * mod_pow(3, MOD - 2, MOD) % MOD, "  check:", 3 * (2 * mod_pow(3, MOD - 2, MOD)) % MOD)
