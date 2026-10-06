"""
# Prefix sums

Store running totals once, and the sum of any range becomes one subtraction.

```
prefix[i] = a[0] + a[1] + ... + a[i-1]        (prefix[0] = 0)
sum(a[l..r]) = prefix[r + 1] - prefix[l]
```

## Use it when
- You answer many "sum from l to r" questions on the same list
- The problem asks about subarrays whose sum equals / is divisible by something
- The numbers can be negative, which rules out a sliding window

## Pattern 1: many range queries
Build `prefix` in O(n), then each query costs O(1) instead of O(n).

## Pattern 2: prefix sum + dict
"How many subarrays sum to k?" A subarray `(i, j]` sums to k when
`prefix[j] - prefix[i] == k`, i.e. `prefix[i] == prefix[j] - k`.
So walk once, keeping a Counter of prefix sums seen so far:
```
seen = Counter({0: 1})       # the empty prefix
total = count = 0
for x in a:
    total += x
    count += seen[total - k]
    seen[total] += 1
```

## Python shortcuts
- `prefix = [0, *accumulate(a)]` builds it in one line
- The same idea works for products, XOR, and counts ("how many vowels in s[l..r]")
- 2D version: `P[r+1][c+1] = grid[r][c] + P[r][c+1] + P[r+1][c] - P[r][c]`

## Common mistakes
- Off-by-one. The leading 0 in `prefix` makes the formula uniform, so always include it
- Forgetting `seen[0] = 1`, which misses subarrays that start at index 0

Press Run to see both patterns.
"""
from collections import Counter
from itertools import accumulate

a = [3, -1, 4, 1, 5, 9]
prefix = [0, *accumulate(a)]
print("list:  ", a)
print("prefix:", prefix)
for l, r in [(0, 2), (1, 4), (3, 5)]:
    print(f"  sum a[{l}..{r}] = prefix[{r + 1}] - prefix[{l}] = {prefix[r + 1] - prefix[l]}")


def count_subarrays_with_sum(nums, k):
    seen = Counter({0: 1})
    total = count = 0
    for x in nums:
        total += x
        count += seen[total - k]     # earlier prefixes that make a sum of k up to here
        seen[total] += 1
    return count


print("subarrays of [1, 2, 3, -2, 2] summing to 3:", count_subarrays_with_sum([1, 2, 3, -2, 2], 3))
