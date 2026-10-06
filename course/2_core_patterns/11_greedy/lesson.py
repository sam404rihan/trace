"""
# Greedy

At each step, take the choice that looks best right now, and never go back.
When it works, it's the simplest and fastest solution. The skill is knowing
when it works.

## Use it when
- A locally best choice can't hurt later choices
- The problem asks for a max/min and sorting reveals an obvious order
- Examples: most meetings you can attend (sort by END, take whatever fits),
  jump game (track the furthest reachable spot), Kadane's max subarray

## Greedy classics
- **Kadane's algorithm** (max subarray sum): keep a running sum; if it goes
  negative, drop it and start fresh, because a negative prefix never helps
- **Furthest reach:** walk once, keeping `reach = max(reach, i + jump[i])`.
  If you ever stand past `reach`, you're stuck
- **Interval scheduling:** sort by end time, then keep every meeting that
  starts after the last one you kept ended

## How to trust a greedy idea
1. Try to break it with a small counterexample (2–4 items). Greedy fails
   quietly, so spend a minute on this
2. Coin change with coins [1, 3, 4] and amount 6: greedy takes 4+1+1 (3 coins),
   but 3+3 is 2. That's a DP problem, not greedy
3. If you can't break it and there's an "exchange argument" (swapping to the greedy
   choice never makes things worse), go for it

## Common mistakes
- Using greedy when choices interact (knapsack, coin change). Use DP there
- Sorting by the wrong thing (start vs end, value vs ratio)

Press Run to see Kadane's algorithm and the jump game.
"""


def max_subarray(nums):
    best = current = nums[0]
    for x in nums[1:]:
        current = max(x, current + x)   # extend the run, or start fresh at x
        best = max(best, current)
        print(f"  x={x:>3}  current run={current:>3}  best={best}")
    return best


print("max subarray sum:", max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]))


def most_meetings(meetings):
    kept, last_end = [], float("-inf")
    for start, end in sorted(meetings, key=lambda m: m[1]):   # earliest END first
        if start >= last_end:
            kept.append((start, end))
            last_end = end
    return kept


print("most meetings:", most_meetings([(1, 4), (3, 5), (0, 6), (5, 7), (8, 9), (5, 9)]))


def greedy_coins(coins, amount):
    used = []
    for c in sorted(coins, reverse=True):
        while amount >= c:
            amount -= c
            used.append(c)
    return used


print("greedy coins for 6 with [1, 3, 4]:", greedy_coins([1, 3, 4], 6), " but [3, 3] is better!")
