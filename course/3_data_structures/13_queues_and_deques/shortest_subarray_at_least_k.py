"""
Shortest Subarray with Sum at Least K                                         [hard]

Return the length of the shortest non-empty contiguous subarray of `nums` whose
sum is at least k, or -1 if there's none. Values CAN be negative, so the usual
two-pointer sliding window doesn't work. k >= 1.

Example:
    shortest_subarray_at_least_k([1], 1)          ->  1
    shortest_subarray_at_least_k([1, 2], 4)       ->  -1
    shortest_subarray_at_least_k([2, -1, 2], 3)   ->  3

Aim for:  O(n) with a monotonic deque over prefix sums.
Hint:     With prefix sums P, you want the closest i < j with P[j] - P[i] >= k. Keep a deque of
          indices with increasing P. For each j: while P[j] - P[front] >= k, record j - front and
          pop the front (a later j can't beat it). Then pop from the back every index with
          P >= P[j] (j is a later AND lower start, so it's always better). Append j.
"""


def shortest_subarray_at_least_k(nums: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums, k):
    best = -1
    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s >= k:
                if best == -1 or j - i + 1 < best:
                    best = j - i + 1
                break
    return best


def _fast(nums, k):
    from collections import deque
    pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    dq, best = deque(), -1
    for j, p in enumerate(pre):
        while dq and p - pre[dq[0]] >= k:
            i = dq.popleft()
            if best == -1 or j - i < best:
                best = j - i
        while dq and pre[dq[-1]] >= p:
            dq.pop()
        dq.append(j)
    return best


def _cases():
    import random
    rng = random.Random(862)
    out = []
    for _ in range(10):
        nums = [rng.randint(-5, 6) for _ in range(rng.randint(1, 14))]
        k = rng.randint(1, 12)
        out.append(((nums, k), _brute(nums, k)))
    big = [rng.randint(-100, 101) for _ in range(100_000)]
    out.append(((big, 3000), _fast(big, 3000)))
    return out


USES = ["prefix.sums", "deque.monotonic"]

TESTS = [
    (([1], 1), 1),
    (([1, 2], 4), -1),
    (([2, -1, 2], 3), 3),
    (([84, -37, 32, 40, 95], 167), 3),
    (([-28, 81, -20, 28, -29], 89), 3),
    (([5, -10, 5, 5], 10), 2),
] + _cases()
