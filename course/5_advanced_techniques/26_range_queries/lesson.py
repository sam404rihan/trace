"""
# Range queries

Prefix sums answer "sum of a[l..r]" in O(1), but only while the array never changes.
When values change, or you need min/max over ranges, reach for a Fenwick tree
(binary indexed tree) or a segment tree. Both do updates and queries in O(log n).

## Use it when
- Many range queries AND point updates mixed together
- "Count of smaller elements after self", inversions, rank queries (Fenwick over values)
- Range min/max with updates (segment tree), or without updates (sparse table)
- 2D sums: prefix sums with inclusion-exclusion

## Fenwick tree (1-indexed)
```
lowbit(i) = i & -i                   # the lowest set bit
add(i, delta):  while i <= n: tree[i] += delta; i += i & -i
prefix(i):      s = 0; while i > 0: s += tree[i]; i -= i & -i
range(l, r) = prefix(r) - prefix(l - 1)
```
tree[i] stores the sum of the lowbit(i) elements ending at i.

## Segment tree (iterative, size 2n)
```
leaves at tree[n + i]; parent p = i // 2 holds combine(tree[2p], tree[2p + 1])
update(i, v): i += n; tree[i] = v; while i > 1: i //= 2; tree[i] = combine(...)
query(l, r) on [l, r): l += n; r += n; walk inwards, taking odd l / odd r nodes
```
Works for any associative combine: sum, min, max, gcd.

## 2D prefix sums
```
P[r+1][c+1] = M[r][c] + P[r][c+1] + P[r+1][c] - P[r][c]
sum(r1..r2, c1..c2) = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1]
```

## Common mistakes
- Fenwick is 1-indexed: index 0 makes `i -= i & -i` loop forever
- Updating with the new value instead of the delta (add val - old)
- Off-by-one between inclusive [l, r] and half-open [l, r)
"""


class Fenwick:
    def __init__(self, n):
        self.tree = [0] * (n + 1)

    def add(self, i, delta):            # i is 1-based
        while i < len(self.tree):
            self.tree[i] += delta
            i += i & -i

    def prefix(self, i):
        s = 0
        while i > 0:
            s += self.tree[i]
            i -= i & -i
        return s


nums = [5, 2, 9, 1, 7, 3]
fw = Fenwick(len(nums))
for i, x in enumerate(nums, 1):
    fw.add(i, x)
print("sum of first 4:", fw.prefix(4))          # 5 + 2 + 9 + 1 = 17
fw.add(3, -9)                                   # nums[2] becomes 0
print("after update:", fw.prefix(4))            # 8
print("tree:", fw.tree)
