"""
# Advanced dynamic programming

Same recipe as before: name the state, find the last decision, fill in an order where
dependencies come first. What changes is the SHAPE of the state.

## Bitmask DP (n <= ~20)
The state includes a set of chosen items as an integer mask: bit i set = item i used.
```
dp[mask][last] = best way to visit exactly `mask`, ending at `last`
for mask in range(1 << n):           # submasks always come before their supersets
    for last in mask: for nxt not in mask: relax dp[mask | 1 << nxt][nxt]
```
That's O(2^n · n²) instead of n! orderings.

## Interval DP
dp[l][r] = the answer for the slice l..r. Fill by increasing length. Often you choose
the LAST action inside (l, r), such as the last balloon to burst or where the final cut goes.

## Tree DP
Return a small tuple from each child, e.g. (best if I'm taken, best if I'm not),
and combine in postorder. House Robber III is the classic example.

## State machines
Several values per day/step, like holding / sold / resting in the stock problems, or
"j transactions used". Each one updates from the previous step's states.

## Common mistakes
- Bitmask loops that read dp[mask | bit] before it's final (iterate masks upwards)
- Interval DP filled by l then r instead of by length
- Forgetting the "don't take it" option in tree DP
"""


def tsp(dist):
    n = len(dist)
    INF = float("inf")
    dp = [[INF] * n for _ in range(1 << n)]
    dp[1][0] = 0                               # visited {0}, standing at 0
    for mask in range(1 << n):
        for last in range(n):
            if dp[mask][last] == INF:
                continue
            for nxt in range(n):
                if not mask >> nxt & 1:
                    new = mask | 1 << nxt
                    dp[new][nxt] = min(dp[new][nxt], dp[mask][last] + dist[last][nxt])
    full = (1 << n) - 1
    return min(dp[full][last] + dist[last][0] for last in range(n))


print("tour cost:", tsp([[0, 10, 15, 20], [10, 0, 35, 25], [15, 35, 0, 30], [20, 25, 30, 0]]))   # 80
