"""
Min Cost Climbing Stairs                                                        [easy]

cost[i] is what you pay when you step ON stair i. After paying, you can climb
1 or 2 stairs. You may start on stair 0 or stair 1. Return the minimum total
cost to reach the top, which is one step past the last stair.

Example:
    min_cost_stairs([10, 15, 20])                          ->  15
    min_cost_stairs([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]) ->  6

Hint:     dp[i] = cheapest way to stand at stair i = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2]),
          with dp[0] = dp[1] = 0. The answer is dp[n]. Two variables are enough.
"""


def min_cost_stairs(cost: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(cost):
    n = len(cost)

    def best(i):                    # cheapest cost to reach the top from standing at i
        if i >= n:
            return 0
        return cost[i] + min(best(i + 1), best(i + 2))
    return min(best(0), best(1))


def _make(rng):
    return ([rng.randint(0, 20) for _ in range(rng.randint(2, 15))],)


def _cases():
    import random
    rng = random.Random(101)
    out = []
    for _ in range(8):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


TESTS = [(([10, 15, 20],), 15), (([1, 100, 1, 1, 1, 100, 1, 1, 100, 1],), 6), (([0, 0],), 0), (([5, 3],), 3)] + _cases()
