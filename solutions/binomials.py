MOD = 1_000_000_007


def binomials(queries: list[tuple[int, int]]) -> list[int]:
    if not queries:
        return []
    N = max(n for n, _ in queries)
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD - 2, MOD)        # Fermat: x^(p-2) is 1/x mod a prime
    for i in range(N, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD     # 1/(i-1)! = i / i!
    return [fact[n] * inv_fact[k] % MOD * inv_fact[n - k] % MOD for n, k in queries]
