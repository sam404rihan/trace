"""
Range Minimum Queries                                                         [medium]

The array never changes. Answer many queries "minimum of nums[l..r]"
(inclusive), and return the answers in order.

Example:
    range_min_queries([4, 2, 7, 1, 9], [(0, 2), (3, 4), (2, 2)])  ->  [2, 1, 7]

Aim for:  O(n log n) setup, O(1) per query: a sparse table. The last test has 100,000 queries.
Hint:     table[j][i] = min of the 2^j elements starting at i:
          table[j][i] = min(table[j-1][i], table[j-1][i + 2^(j-1)]).
          For [l, r], take k = floor(log2(r - l + 1)), then min(table[k][l], table[k][r - 2^k + 1]).
          The two blocks overlap, and that's fine for min.
"""


def range_min_queries(nums: list[int], queries: list[tuple[int, int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _fast(nums, qs):
    table = [nums[:]]
    j = 1
    while (1 << j) <= len(nums):
        prev, half = table[-1], 1 << (j - 1)
        table.append([min(prev[i], prev[i + half]) for i in range(len(nums) - (1 << j) + 1)])
        j += 1
    out = []
    for l, r in qs:
        k = (r - l + 1).bit_length() - 1
        out.append(min(table[k][l], table[k][r - (1 << k) + 1]))
    return out


def _cases():
    import random
    rng = random.Random(208)
    out = []
    for _ in range(6):
        nums = [rng.randint(-50, 50) for _ in range(rng.randint(1, 15))]
        qs = []
        for _ in range(8):
            l = rng.randrange(len(nums))
            qs.append((l, rng.randint(l, len(nums) - 1)))
        out.append(((nums, qs), [min(nums[l:r + 1]) for l, r in qs]))
    nums = [rng.randint(-10**9, 10**9) for _ in range(100_000)]
    qs = []
    for _ in range(100_000):
        l = rng.randrange(len(nums))
        qs.append((l, rng.randint(l, len(nums) - 1)))
    out.append(((nums, qs), _fast(nums, qs)))
    return out


TESTS = [(([4, 2, 7, 1, 9], [(0, 2), (3, 4), (2, 2)]), [2, 1, 7]), (([5], [(0, 0)]), [5])] + _cases()
