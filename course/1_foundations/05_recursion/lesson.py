"""
# Recursion

A recursive function solves a problem by calling itself on a smaller piece.
Trees, graphs, backtracking and DP all build on this, so get comfortable now.

## The recipe
1. **Base case:** the smallest input you can answer directly (empty, 0, a leaf)
2. **Recursive case:** trust that the call on a smaller input works, and
   build your answer from it
3. **Progress:** every call must move toward the base case

```
def total(nums):
    if not nums:                        # base case
        return 0
    return nums[0] + total(nums[1:])    # smaller problem
```

## Tips
- Don't trace every call in your head. Check the base case, then check that
  one step is right assuming the smaller call works
- Pass indexes instead of slices (`solve(i + 1)`, not `solve(nums[1:])`),
  since slices copy and make it O(n²)
- Define a helper inside your function so it can see the inputs without
  passing them around
- `@functools.cache` remembers answers. It turns exponential recursion into
  linear when the same calls repeat (that's dynamic programming)

## Common mistakes
- A missing or wrong base case gives `RecursionError: maximum recursion depth exceeded`
- Forgetting to `return` the recursive result
- Python's default limit is about 1,000 calls deep. For very deep inputs,
  use a loop with your own stack

Press Run to see recursion, the call stack, and the memoisation speed-up.
"""
import time
from functools import cache


def countdown(n, depth=0):
    print("  " * depth + f"countdown({n})")
    if n == 0:                          # base case
        return
    countdown(n - 1, depth + 1)         # smaller problem


countdown(3)


def digit_sum(n):
    if n < 10:
        return n
    return n % 10 + digit_sum(n // 10)


print("digit_sum(9875) =", digit_sum(9875))


def fib_slow(n):                        # each call makes two more: O(2ⁿ)
    return n if n < 2 else fib_slow(n - 1) + fib_slow(n - 2)


@cache                                   # same code, answers remembered: O(n)
def fib_fast(n):
    return n if n < 2 else fib_fast(n - 1) + fib_fast(n - 2)


for fn in (fib_slow, fib_fast):
    start = time.perf_counter()
    value = fn(27)
    print(f"{fn.__name__}(27) = {value}   {(time.perf_counter() - start) * 1000:.1f} ms")
