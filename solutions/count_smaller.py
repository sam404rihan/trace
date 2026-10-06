def count_smaller(nums: list[int]) -> list[int]:
    rank = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}   # compress values to 1..k
    tree = [0] * (len(rank) + 1)                                  # Fenwick tree of counts per value
    out = []
    for x in reversed(nums):
        k, smaller = rank[x] - 1, 0
        while k > 0:                                              # how many seen values are < x
            smaller += tree[k]
            k -= k & -k
        out.append(smaller)
        k = rank[x]
        while k < len(tree):                                      # record x as seen
            tree[k] += 1
            k += k & -k
    return out[::-1]
