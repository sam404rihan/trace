"""
House Robber II                                                               [medium]

Same as House Robber (no two adjacent houses), but the houses stand in a
CIRCLE: the first and last are neighbours too. Return the most you can take.

Example:
    house_robber_ii([2, 3, 2])      ->  3
    house_robber_ii([1, 2, 3, 1])   ->  4

Hint:     The first and last house can't both be robbed. So run plain House Robber twice:
          once without the last house, once without the first. Take the better result.
          (A single house is a special case.)
"""


def house_robber_ii(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    n, best = len(nums), 0
    for mask in range(1 << n):
        picks = [i for i in range(n) if mask >> i & 1]
        if all((b - a) != 1 for a, b in zip(picks, picks[1:])) and not (n > 1 and 0 in picks and n - 1 in picks):
            best = max(best, sum(nums[i] for i in picks))
    return best


def _make(rng):
    return ([rng.randint(0, 20) for _ in range(rng.randint(1, 12))],)


def _cases():
    import random
    rng = random.Random(102)
    out = []
    for _ in range(10):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


USES = ["dp.recurrence"]

TESTS = [(([2, 3, 2],), 3), (([1, 2, 3, 1],), 4), (([1, 2, 3],), 3), (([7],), 7), (([5, 1],), 5)] + _cases()
