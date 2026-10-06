"""
Binomials Mod a Prime                                                           [hard]

Answer many questions "n choose k, modulo 1,000,000,007". queries is a list of
(n, k) pairs with 0 <= k <= n <= 200,000. Return the answers in order.

Example:
    binomials([(5, 2), (10, 0), (6, 6)])  ->  [10, 1, 1]
    binomials([(100, 50)])  ->  [538992043]

Aim for:  O(N + Q) after one precomputation, where N = the largest n.
Hint:     C(n, k) = n! / (k! · (n-k)!). Precompute fact[i] = i! mod p, then inv_fact[N] =
          pow(fact[N], p - 2, p) (Fermat), and walk down: inv_fact[i - 1] = inv_fact[i] · i.
          Each query is then three multiplications.
"""
from math import comb

MOD = 1_000_000_007


def binomials(queries: list[tuple[int, int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _tables(N):
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv = [1] * (N + 1)
    inv[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N, 0, -1):
        inv[i - 1] = inv[i] * i % MOD
    return fact, inv


def _big():
    import random
    rng = random.Random(3006)
    N = 200_000
    fact, inv = _tables(N)
    qs = []
    for _ in range(100_000):
        n = rng.randint(N // 2, N)
        qs.append((n, rng.randint(0, n)))
    return ((qs,), [fact[n] * inv[k] % MOD * inv[n - k] % MOD for n, k in qs])


def _small():
    import random
    rng = random.Random(3007)
    qs = []
    for _ in range(40):
        n = rng.randint(0, 300)
        qs.append((n, rng.randint(0, n)))
    return ((qs,), [comb(n, k) % MOD for n, k in qs])


TESTS = [(([(5, 2), (10, 0), (6, 6)],), [10, 1, 1]), (([(100, 50)],), [538992043]), (([(0, 0)],), [1]),
         (([],), []), _small(), _big()]
