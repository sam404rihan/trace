"""
# Big-O in practice

You don't need the maths. You need to answer one question before you code:
**will my idea be fast enough for this input size?**

## The only table you need
Python does very roughly 10–50 million simple steps per second. So:

- n ≤ 10: anything works, even O(n!) (try every ordering)
- n ≤ 20: O(2ⁿ) is OK (try every subset)
- n ≤ 3,000: O(n²) is OK (two nested loops)
- n ≤ 200,000: you need O(n log n) or O(n) (sort, or one pass with a dict/set)
- n ≥ 10⁹: only O(log n) or O(1) (binary search, a formula)

## Hidden costs in Python
These look like one step but are really a loop:

- `x in some_list` is O(n). `x in some_set` is O(1)
- `list.pop(0)` and `list.insert(0, x)` are O(n). Use `deque`
- `a[i:j]` copies j - i items
- `s += "x"` in a loop can copy the whole string every time. Use `"".join`
- `sorted()` is O(n log n), which is usually fine to do once, but not inside a loop

## How to read your own code
- One loop over n items: O(n)
- A loop inside a loop: O(n²)
- Halving the problem each step (binary search): O(log n)
- Sort first, then one pass: O(n log n)
- Recursion that branches twice per call with no memo: O(2ⁿ). Danger

## Space
Memory counts too. An extra dict of n items is O(n) space. Usually that's a
fine price for turning O(n²) time into O(n).

## Best practice
Write the brute force first if you're stuck. Then ask: what am I searching
for repeatedly? A set or dict usually removes the inner loop.

Press Run to watch the same task done in O(n²) and O(n).
"""
import time


def has_duplicate_slow(nums):
    for i in range(len(nums)):              # O(n²): compare every pair
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False


def has_duplicate_fast(nums):
    seen = set()                            # O(n): one pass, O(1) lookups
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False


for n in (1_000, 2_000, 4_000):
    data = list(range(n))                   # no duplicates: the worst case
    start = time.perf_counter()
    has_duplicate_slow(data)
    slow = time.perf_counter() - start
    start = time.perf_counter()
    has_duplicate_fast(data)
    fast = time.perf_counter() - start
    print(f"n={n:>5}   O(n²): {slow * 1000:7.1f} ms    O(n): {fast * 1000:5.2f} ms")

print("\nDouble n and the O(n²) version takes about 4x as long. The O(n) one only 2x.")

# The hidden O(n): `in` on a list vs a set
items = list(range(100_000))
as_set = set(items)
start = time.perf_counter()
for _ in range(200):
    99_999 in items
list_ms = (time.perf_counter() - start) * 1000
start = time.perf_counter()
for _ in range(200):
    99_999 in as_set
set_ms = (time.perf_counter() - start) * 1000
print(f"200 lookups:  list {list_ms:.1f} ms   set {set_ms:.3f} ms")
