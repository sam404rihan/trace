"""
Minimum XOR Sum of Two Arrays                                                 [hard]

`a` and `b` have the same length n (at most 14). Reorder `b` however you like
to make (a[0] ^ b[0]) + (a[1] ^ b[1]) + ... + (a[n-1] ^ b[n-1]) as small as
possible. Return that smallest sum.

Example:
    min_xor_sum([1, 2], [2, 3])        ->  2      b as [3, 2]: (1^3) + (2^2) = 2 + 0
    min_xor_sum([1, 0, 3], [5, 3, 4])  ->  8

Aim for:  O(n² · 2^n) with a bitmask DP. Trying every ordering is O(n!): 14! is 87 billion.
Hint:     Pair a[0], a[1], ... in order. The state is a bitmask of which b elements are used;
          its popcount tells you which a element comes next. dp[mask] = best sum for pairing
          a[:popcount(mask)] with exactly the b elements in mask:
          dp[mask | 1 << j] = min(..., dp[mask] + (a[i] ^ b[j])) for each unused j.
"""


def min_xor_sum(a: list[int], b: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(a, b):
    from itertools import permutations
    return min(sum(x ^ y for x, y in zip(a, p)) for p in permutations(b))


def _dp(a, b):
    n = len(a)
    INF = float("inf")
    dp = [INF] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] == INF:
            continue
        i = bin(mask).count("1")
        if i == n:
            continue
        for j in range(n):
            if not mask >> j & 1:
                m2 = mask | 1 << j
                v = dp[mask] + (a[i] ^ b[j])
                if v < dp[m2]:
                    dp[m2] = v
    return dp[-1]


def _cases():
    import random
    rng = random.Random(1879)
    out = []
    for _ in range(8):
        n = rng.randint(1, 6)
        a = [rng.randint(0, 31) for _ in range(n)]
        b = [rng.randint(0, 31) for _ in range(n)]
        out.append(((a, b), _brute(a, b)))
    a = [rng.randint(0, 10**7) for _ in range(12)]
    b = [rng.randint(0, 10**7) for _ in range(12)]
    out.append(((a, b), _dp(a, b)))
    return out


TESTS = [
    (([1, 2], [2, 3]), 2),
    (([1, 0, 3], [5, 3, 4]), 8),
    (([7], [7]), 0),
    (([0, 0, 0], [1, 2, 4]), 7),
] + _cases()
