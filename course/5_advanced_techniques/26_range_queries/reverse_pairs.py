"""
Reverse Pairs                                                                 [hard]

Count the pairs i < j with nums[i] > 2 * nums[j]. Values can be negative.

Example:
    reverse_pairs([1, 3, 2, 3, 1])     ->  2       (3, 1) twice
    reverse_pairs([2, 4, 3, 5, 1])     ->  3       (4, 1), (3, 1), (5, 1)

Aim for:  O(n log n). Checking every pair is too slow for 30,000 numbers.
Hint:     Two ways. (1) Merge sort: before merging two sorted halves, count with two pointers
          how many (left value, right value r) pairs have left value > 2 * r. (2) A Fenwick tree
          over the sorted distinct values: walk left to right, asking "how many earlier values
          are greater than 2 * nums[j]?" (find the rank of 2 * nums[j] with bisect).
"""


def reverse_pairs(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    return sum(nums[i] > 2 * nums[j] for i in range(len(nums)) for j in range(i + 1, len(nums)))


def _fast(nums):
    import bisect
    vals = sorted(set(nums))
    tree = [0] * (len(vals) + 1)
    total = 0
    for seen, x in enumerate(nums):
        k = bisect.bisect_right(vals, 2 * x)        # values <= 2x occupy ranks 1..k
        i, at_most = k, 0
        while i:
            at_most += tree[i]
            i -= i & -i
        total += seen - at_most
        i = bisect.bisect_left(vals, x) + 1
        while i <= len(vals):
            tree[i] += 1
            i += i & -i
    return total


def _cases():
    import random
    rng = random.Random(493)
    out = []
    for _ in range(10):
        nums = [rng.randint(-10, 10) for _ in range(rng.randint(0, 14))]
        out.append(((nums,), _brute(nums)))
    big = [rng.randint(-2**31, 2**31 - 1) for _ in range(30_000)]
    out.append(((big,), _fast(big)))
    return out


TESTS = [
    (([1, 3, 2, 3, 1],), 2),
    (([2, 4, 3, 5, 1],), 3),
    (([],), 0),
    (([5, -5],), 1),
    (([-5, -5],), 1),
    (([2147483647, 2147483647, 2147483647],), 0),
] + _cases()
