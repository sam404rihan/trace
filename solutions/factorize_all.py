def factorize_all(nums: list[int]) -> list[list[int]]:
    if not nums:
        return []
    N = max(nums)
    spf = list(range(N + 1))                    # spf[x] = smallest prime factor of x
    for p in range(2, isqrt(N) + 1):
        if spf[p] == p:                         # p is prime
            for m in range(p * p, N + 1, p):
                if spf[m] == m:
                    spf[m] = p
    out = []
    for x in nums:
        factors = []
        while x > 1:
            factors.append(spf[x])
            x //= spf[x]
        out.append(factors)
    return out
