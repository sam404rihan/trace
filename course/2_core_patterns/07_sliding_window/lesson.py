"""
# Sliding window

A window is a contiguous stretch `a[left:right + 1]`. Instead of recomputing
every window from scratch (O(n·k)), slide it: add the item entering on the
right, remove the item leaving on the left. O(n).

## Use it when
- The problem says "subarray" or "substring" (contiguous!)
- ...and "longest", "shortest", "maximum sum", "at most k", "without repeating"

## Fixed-size window (size k)
```
window = sum(a[:k])
best = window
for right in range(k, len(a)):
    window += a[right] - a[right - k]     # one in, one out
    best = max(best, window)
```

## Variable-size window
Grow on the right every step. Shrink from the left while the window breaks the rule.
```
left = 0
for right, x in enumerate(a):
    add x to the window state
    while window is invalid:
        remove a[left] from the state
        left += 1
    best = max(best, right - left + 1)
```

## What goes in "window state"?
- A running sum, for sum limits
- A `Counter` or dict of counts, for "at most k distinct" or "anagram of"
- A dict of last-seen index, for "no repeats": jump `left` straight past the old copy

## Common mistakes
- Using it on non-contiguous problems (subsequences are DP, not windows)
- Shrinking with `if` instead of `while`: one step may not be enough
- Variable windows with sums only work when numbers are non-negative. With
  negatives, use prefix sums and a dict (next topic)

Press Run to watch both kinds of window move.
"""


def max_window_sum(nums, k):
    window = sum(nums[:k])
    best = window
    for right in range(k, len(nums)):
        window += nums[right] - nums[right - k]
        print(f"  window {nums[right - k + 1:right + 1]} sum={window}")
        best = max(best, window)
    return best


print("best sum of 3 in a row:", max_window_sum([2, 1, 5, 1, 3, 2], 3))


def longest_with_at_most_two_kinds(fruits):
    """Longest stretch containing at most 2 different values."""
    counts = {}
    left = best = 0
    for right, fruit in enumerate(fruits):
        counts[fruit] = counts.get(fruit, 0) + 1
        while len(counts) > 2:               # invalid: shrink from the left
            counts[fruits[left]] -= 1
            if counts[fruits[left]] == 0:
                del counts[fruits[left]]
            left += 1
        best = max(best, right - left + 1)
    return best


print("longest with 2 kinds:", longest_with_at_most_two_kinds(list("abcbbca")))
