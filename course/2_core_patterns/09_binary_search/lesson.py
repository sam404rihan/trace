"""
# Binary search

Halve the search space every step: a million items take about 20 steps.
It works on anything where a yes/no question flips exactly once.

## Use it when
- The list is sorted and you need a value, or where it would go
- "Find the minimum/maximum X such that ..." where bigger X only makes
  things easier. This is **binary search on the answer**
- O(log n) is required, or n is huge (10⁹)

## Template: find the first index where `ok(i)` is True
This one template covers almost everything. No off-by-one guessing.
```
lo, hi = 0, len(a)            # the answer is somewhere in [lo, hi]
while lo < hi:
    mid = (lo + hi) // 2
    if ok(mid):
        hi = mid              # mid might be the answer: keep it
    else:
        lo = mid + 1          # mid is definitely not it
return lo                     # len(a) means "never True"
```
For "find target in sorted a", use `ok(i) = a[i] >= target`, then check `a[lo] == target`.

## Binary search on the answer
Don't search the list, search the range of possible answers:
```
lo, hi = smallest_possible, largest_possible
while lo < hi:
    mid = (lo + hi) // 2
    if works(mid): hi = mid
    else: lo = mid + 1
```
"Minimum speed to finish in h hours", "smallest capacity to ship in d days",
"integer square root". Write `works(x)`, and the search is the easy part.

## Python shortcuts
- `bisect_left(a, x)`: first index with `a[i] >= x`
- `bisect_right(a, x)`: first index with `a[i] > x`
- `bisect_right(a, x) - bisect_left(a, x)`: how many copies of x
- `insort(a, x)` inserts keeping a sorted (but the insert itself is O(n))

## Common mistakes
- `lo = mid` instead of `lo = mid + 1`: infinite loop when `hi = lo + 1`
- Mixing up `while lo < hi` and `while lo <= hi` templates. Pick one and stick with it
- Forgetting the list must be sorted

Press Run to see the template find things.
"""
from bisect import bisect_left, bisect_right


def first_true(lo, hi, ok):
    """Smallest x in [lo, hi) with ok(x) True, or hi if none."""
    steps = 0
    while lo < hi:
        mid = (lo + hi) // 2
        steps += 1
        if ok(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo, steps


a = [1, 3, 3, 3, 5, 8, 13]
index, steps = first_true(0, len(a), lambda i: a[i] >= 5)
print(f"first index with a[i] >= 5: {index} ({steps} steps)")

# Binary search on the answer: smallest x with x * x >= 1_000_000_007
x, steps = first_true(0, 10**9, lambda x: x * x >= 1_000_000_007)
print(f"smallest x with x² >= 1e9+7: {x}   found in {steps} steps out of a billion options")

print("bisect_left(a, 3) =", bisect_left(a, 3), "  bisect_right(a, 3) =", bisect_right(a, 3),
      "  so 3 appears", bisect_right(a, 3) - bisect_left(a, 3), "times")
