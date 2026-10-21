"""
Burst Balloons                                                                  [hard]

Bursting balloon i earns left · nums[i] · right coins, where left and right
are its current neighbours (treat missing neighbours as 1). Then it's gone,
and its neighbours become adjacent. Burst all of them. Return the most coins.

Example:
    burst_balloons([3, 1, 5, 8])  ->  167      3·1·5 + 3·5·8 + 1·3·8 + 1·8·1

Aim for:  O(n³) interval DP.
Hint:     Think about the LAST balloon to burst in an interval (l, r), with l and r themselves still
          standing: dp[l][r] = max over k of dp[l][k] + nums[l]·nums[k]·nums[r] + dp[k][r].
          Pad nums with a 1 on each side. Fill short intervals first.
"""


def burst_balloons(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    from itertools import permutations as perms
    best = 0
    for order in perms(range(len(nums))):
        alive, coins = list(range(len(nums))), 0
        for i in order:
            p = alive.index(i)
            left = nums[alive[p - 1]] if p > 0 else 1
            right = nums[alive[p + 1]] if p + 1 < len(alive) else 1
            coins += left * nums[i] * right
            alive.pop(p)
        best = max(best, coins)
    return best


def _make(rng):
    return ([rng.randint(0, 9) for _ in range(rng.randint(0, 6))],)


def _cases():
    import random
    rng = random.Random(113)
    out = []
    for _ in range(8):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


USES = ["dp.interval"]

TESTS = [(([3, 1, 5, 8],), 167), (([1, 5],), 10), (([],), 0), (([7],), 7)] + _cases()
