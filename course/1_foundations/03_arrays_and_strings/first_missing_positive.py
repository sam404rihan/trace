"""
First Missing Positive                                                        [hard]

Return the smallest positive integer that is NOT in `nums`. The list is
unsorted and may hold negatives, zeros and repeats.

The catch: use O(n) time and only O(1) extra memory. No set, no sorting.
You may rearrange `nums` itself.

Example:
    first_missing_positive([3, 4, -1, 1])      ->  2
    first_missing_positive([1, 2, 0])          ->  3
    first_missing_positive([7, 8, 9, 11, 12])  ->  1

Aim for:  O(n) time, O(1) extra space.
Hint:     The answer is between 1 and n + 1, so only values 1..n matter. Use the list as its own
          lookup table: keep swapping nums[i] into its home slot nums[i] - 1 while it's in range
          and the home slot doesn't already hold it. Then the first index k with nums[k] != k + 1
          gives the answer k + 1.
"""


def first_missing_positive(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    seen = set(nums)
    k = 1
    while k in seen:
        k += 1
    return k


def _cases():
    import random
    rng = random.Random(41)
    out = []
    for _ in range(8):
        n = rng.randint(0, 20)
        nums = [rng.randint(-3, n + 2) for _ in range(n)]
        out.append(((nums,), _brute(nums)))
    big = list(range(1, 200_001))
    rng.shuffle(big)
    gone = big.pop(rng.randrange(len(big)))
    big.append(-gone)
    out.append(((big,), gone))
    return out


USES = []

TESTS = [
    (([3, 4, -1, 1],), 2),
    (([1, 2, 0],), 3),
    (([7, 8, 9, 11, 12],), 1),
    (([],), 1),
    (([1],), 2),
    (([2],), 1),
    (([1, 1],), 2),
    (([2, 2, 2, 1],), 3),
] + _cases()
