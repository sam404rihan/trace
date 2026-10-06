"""
# Dynamic programming (1D)

DP = recursion + remembering answers. If a problem splits into smaller
versions of itself, and the same smaller versions come up again and again,
store each answer once.

## Use it when
- "How many ways...", "minimum cost...", "maximum value...", "is it possible..."
- Each step's choice affects what's possible later (so greedy fails)
- The brute-force recursion is correct but times out

## The 4-step recipe
1. **State:** what does `dp[i]` mean, in words? ("best money robbing houses 0..i")
2. **Transition:** how does `dp[i]` come from smaller ones?
   (`dp[i] = max(dp[i-1], dp[i-2] + nums[i])`)
3. **Base cases:** the smallest states (`dp[0]`, `dp[1]`)
4. **Answer:** which state holds it (`dp[n-1]`, `max(dp)`, ...)

## Top-down: the easiest way in
Write the plain recursion, then add one line:
```
from functools import cache

@cache
def best(i):
    if i < 0:
        return 0
    return max(best(i - 1), best(i - 2) + nums[i])
```

## Bottom-up: a loop, no recursion limit
```
dp = [0] * (n + 1)
for i in range(...):
    dp[i] = ...                  # only uses entries already filled
```
If `dp[i]` only needs the last one or two entries, keep two variables
instead of a list: O(1) space.

## Classic 1D shapes
- Fibonacci-like: `dp[i]` from `dp[i-1]` and `dp[i-2]` (stairs, house robber)
- "Best way to make amount x": `dp[x] = min(dp[x - c] + 1 for c in coins)`
- "Can the prefix s[:i] be built?": `dp[i] = any(dp[j] and s[j:i] in words)`
- Longest increasing subsequence: `dp[i] = 1 + max(dp[j] for j < i if a[j] < a[i])`

## Common mistakes
- Not saying out loud what `dp[i]` means. Most DP bugs start here
- Wrong base case (is `dp[0]` "0 items" or "the first item"?)
- `@cache` on a function whose arguments are lists: lists aren't hashable. Use indexes

Press Run to see the speed-up from remembering.
"""
import time
from functools import cache

houses = [2, 7, 9, 3, 1, 5, 8, 2, 6, 4] * 3


def rob_plain(i):
    if i < 0:
        return 0
    return max(rob_plain(i - 1), rob_plain(i - 2) + houses[i])


@cache
def rob_memo(i):
    if i < 0:
        return 0
    return max(rob_memo(i - 1), rob_memo(i - 2) + houses[i])


def rob_loop(nums):
    two_back = one_back = 0
    for x in nums:
        two_back, one_back = one_back, max(one_back, two_back + x)
    return one_back


for name, fn in [("plain recursion", lambda: rob_plain(len(houses) - 1)),
                 ("with @cache    ", lambda: rob_memo(len(houses) - 1)),
                 ("bottom-up loop ", lambda: rob_loop(houses))]:
    start = time.perf_counter()
    answer = fn()
    print(f"{name}: {answer}   {(time.perf_counter() - start) * 1000:8.2f} ms")

# Bottom-up table for "fewest coins", printed so you can see it fill in
coins, amount = [1, 3, 4], 6
dp = [0] + [float("inf")] * amount
for x in range(1, amount + 1):
    dp[x] = min(dp[x - c] + 1 for c in coins if c <= x)
print("\nfewest coins for each amount 0..6:", dp, "  (greedy would say 3 for 6)")
