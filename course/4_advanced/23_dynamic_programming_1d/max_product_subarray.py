"""
Maximum Product Subarray                                                      [medium]

Return the largest product of any non-empty contiguous subarray.

Example:
    max_product_subarray([2, 3, -2, 4])  ->  6
    max_product_subarray([-2, 3, -4])    ->  24

Aim for:  O(n), one pass.
Hint:     A negative number turns the smallest product into the largest. So track BOTH the max and
          the min product of a subarray ending here. For each x, the new candidates are x, max·x
          and min·x.
"""


def max_product_subarray(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    best = nums[0]
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            best = max(best, p)
    return best


def _make(rng):
    return ([rng.randint(-4, 4) for _ in range(rng.randint(1, 14))],)


def _cases():
    import random
    rng = random.Random(105)
    out = []
    for _ in range(10):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


USES = ["greedy.kadane"]

TESTS = [(([2, 3, -2, 4],), 6), (([-2, 0, -1],), 0), (([-2, 3, -4],), 24), (([-3],), -3), (([0, 2],), 2)] + _cases()
