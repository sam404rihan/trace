def min_xor_sum(a: list[int], b: list[int]) -> int:
    n = len(a)
    full = (1 << n) - 1
    best = [inf] * (1 << n)         # best[mask]: a[:popcount(mask)] paired with the b's in mask
    best[0] = 0
    for mask in range(full):
        if best[mask] == inf:
            continue
        i = bin(mask).count("1")    # the next a to pair
        for j in range(n):
            if not mask & (1 << j):
                nxt = mask | (1 << j)
                best[nxt] = min(best[nxt], best[mask] + (a[i] ^ b[j]))
    return best[full]
