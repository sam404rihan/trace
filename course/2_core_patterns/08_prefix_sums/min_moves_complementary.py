"""
Minimum Moves to Make Array Complementary                                     [hard]

`nums` has even length n and every value is between 1 and `limit`. One move
replaces any element with any value from 1 to limit. The array is
"complementary" when nums[i] + nums[n - 1 - i] is the same for every i.
Return the fewest moves needed.

Example:
    min_moves_complementary([1, 2, 4, 3], 4)  ->  1     change 4 to 2: every pair sums to 4
    min_moves_complementary([1, 2, 2, 1], 2)  ->  2
    min_moves_complementary([1, 2, 1, 2], 2)  ->  0

Aim for:  O(n + limit) with a difference array over the possible target sums 2..2*limit.
Hint:     For one pair (a, b) with a <= b and a target T: 0 moves if T == a + b; 1 move if
          a + 1 <= T <= b + limit; otherwise 2. Every pair adds that cost to every T. Start every
          T at 2 per pair, then subtract over ranges with a difference array: -1 on
          [a + 1, b + limit] and one more -1 at exactly a + b. Prefix-sum it and take the min.
"""


def min_moves_complementary(nums: list[int], limit: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums, limit):
    n = len(nums)
    best = n
    for t in range(2, 2 * limit + 1):
        moves = 0
        for i in range(n // 2):
            a, b = sorted((nums[i], nums[n - 1 - i]))
            moves += 0 if a + b == t else 1 if a + 1 <= t <= b + limit else 2
        best = min(best, moves)
    return best


def _fast(nums, limit):
    n = len(nums)
    diff = [0] * (2 * limit + 2)
    for i in range(n // 2):
        a, b = sorted((nums[i], nums[n - 1 - i]))
        diff[2] += 2
        diff[a + 1] -= 1
        diff[b + limit + 1] += 1
        diff[a + b] -= 1
        diff[a + b + 1] += 1
    best, cur = n, 0
    for t in range(2, 2 * limit + 1):
        cur += diff[t]
        best = min(best, cur)
    return best


def _cases():
    import random
    rng = random.Random(1674)
    out = []
    for _ in range(10):
        limit = rng.randint(1, 6)
        nums = [rng.randint(1, limit) for _ in range(2 * rng.randint(1, 5))]
        out.append(((nums, limit), _brute(nums, limit)))
    big = [rng.randint(1, 50_000) for _ in range(100_000)]
    out.append(((big, 50_000), _fast(big, 50_000)))
    return out


USES = ["prefix.sums", "prefix.difference"]

TESTS = [
    (([1, 2, 4, 3], 4), 1),
    (([1, 2, 2, 1], 2), 2),
    (([1, 2, 1, 2], 2), 0),
    (([1, 1], 1), 0),
    (([1, 3], 3), 0),
    (([1, 1, 3, 3], 3), 0),
] + _cases()
