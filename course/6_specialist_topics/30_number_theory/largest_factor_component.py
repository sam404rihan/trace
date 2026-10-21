"""
Largest Component Size by Common Factor                                       [hard]

`nums` holds distinct positive integers. Connect two numbers when they share a
common factor greater than 1. Return the size of the largest connected group
(connections chain: if 4 links to 6 and 6 links to 15, all three are one group).

Example:
    largest_factor_component([4, 6, 15, 35])        ->  4
    largest_factor_component([20, 50, 9, 63])       ->  2
    largest_factor_component([2, 3, 6, 7, 4, 12, 21, 39])  ->  8

Aim for:  O(n √max) with union-find. Comparing every pair with gcd is O(n²): too slow for 10,000.
Hint:     Don't link numbers to each other; link each number to its prime factors. Put numbers
          and primes in one union-find (offset the primes, or key everything in a dict). Find a
          number's prime factors by trial division up to its square root. In the end, count how
          many numbers share each root.
"""


def largest_factor_component(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    from math import gcd
    n = len(nums)
    seen, best = [False] * n, 0
    for s in range(n):
        if seen[s]:
            continue
        seen[s], stack, size = True, [s], 0
        while stack:
            i = stack.pop()
            size += 1
            for j in range(n):
                if not seen[j] and gcd(nums[i], nums[j]) > 1:
                    seen[j] = True
                    stack.append(j)
        best = max(best, size)
    return best


def _fast(nums):
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for x in nums:
        y, p = x, 2
        while p * p <= y:
            if y % p == 0:
                parent[find(("n", x))] = find(("p", p))
                while y % p == 0:
                    y //= p
            p += 1
        if y > 1:
            parent[find(("n", x))] = find(("p", y))
    counts = {}
    for x in nums:
        r = find(("n", x))
        counts[r] = counts.get(r, 0) + 1
    return max(counts.values())


def _cases():
    import random
    rng = random.Random(952)
    out = []
    for _ in range(10):
        nums = rng.sample(range(1, 60), rng.randint(1, 12))
        out.append(((nums,), _brute(nums)))
    big = rng.sample(range(1, 100_001), 10_000)
    out.append(((big,), _fast(big)))
    return out


USES = ["uf.find", "uf.union", "nt.trial_division"]

TESTS = [
    (([4, 6, 15, 35],), 4),
    (([20, 50, 9, 63],), 2),
    (([2, 3, 6, 7, 4, 12, 21, 39],), 8),
    (([1],), 1),
    (([1, 2, 3, 5],), 1),
    (([99, 68, 70, 77, 35, 52, 53, 25, 62],), 8),
] + _cases()
