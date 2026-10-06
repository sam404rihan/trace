def largest_factor_component(nums: list[int]) -> int:
    parent = {}                     # union-find over ("num", x) and ("prime", p) nodes

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    for x in nums:
        rest, p = x, 2
        while p * p <= rest:            # trial division: x's prime factors
            if rest % p == 0:
                union(("num", x), ("prime", p))
                while rest % p == 0:
                    rest //= p
            p += 1
        if rest > 1:                    # what's left is a prime factor too
            union(("num", x), ("prime", rest))

    sizes = Counter(find(("num", x)) for x in nums)
    return max(sizes.values())
