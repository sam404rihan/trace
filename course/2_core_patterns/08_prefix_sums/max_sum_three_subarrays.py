"""
Maximum Sum of 3 Non-Overlapping Subarrays                                    [hard]

Pick three non-overlapping subarrays of `nums`, each exactly k long, with the
largest total sum. Return their start indices in increasing order. If several
choices tie, return the lexicographically smallest list of starts.
All values are positive and len(nums) >= 3 * k.

Example:
    max_sum_three_subarrays([1, 2, 1, 2, 6, 7, 5, 1], 2)  ->  [0, 3, 5]
        [1, 2], [2, 6], [7, 5] sum to 23. [2, 1] at index 1 ties with [1, 2] at 0, but 0 is smaller.
    max_sum_three_subarrays([1, 2, 1, 2, 1, 2, 1, 2, 1], 2)  ->  [0, 2, 4]

Aim for:  O(n).
Hint:     With prefix sums, window[i] = sum(nums[i:i + k]) in O(1). Precompute best_left[i] = the
          start of the best window in window[0..i] (earliest on ties) and best_right[i] = the best
          in window[i..] (earliest on ties, so use >= when scanning right to left). Then try every
          middle start m: best_left[m - k], m, best_right[m + k].
"""


def max_sum_three_subarrays(nums: list[int], k: int) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums, k):
    w = [sum(nums[i:i + k]) for i in range(len(nums) - k + 1)]
    best, pick = -1, None
    for a in range(len(w)):
        for b in range(a + k, len(w)):
            for c in range(b + k, len(w)):
                if w[a] + w[b] + w[c] > best:       # loops run in lexicographic order
                    best, pick = w[a] + w[b] + w[c], [a, b, c]
    return pick


def _fast(nums, k):
    pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    w = [pre[i + k] - pre[i] for i in range(len(nums) - k + 1)]
    m = len(w)
    left, right = [0] * m, [m - 1] * m
    for i in range(1, m):
        left[i] = i if w[i] > w[left[i - 1]] else left[i - 1]
    for i in range(m - 2, -1, -1):
        right[i] = i if w[i] >= w[right[i + 1]] else right[i + 1]
    best = None
    for mid in range(k, m - k):
        a, c = left[mid - k], right[mid + k]
        cand = (w[a] + w[mid] + w[c], [a, mid, c])
        if best is None or cand[0] > best[0]:
            best = cand
    return best[1]


def _cases():
    import random
    rng = random.Random(689)
    out = []
    for _ in range(8):
        k = rng.randint(1, 3)
        nums = [rng.randint(1, 5) for _ in range(rng.randint(3 * k, 3 * k + 7))]
        out.append(((nums, k), _brute(nums, k)))
    big = [rng.randint(1, 1000) for _ in range(60_000)]
    out.append(((big, 500), _fast(big, 500)))
    return out


USES = ["scan.best_so_far", "array.left_right_passes", "prefix.sums"]

TESTS = [
    (([1, 2, 1, 2, 6, 7, 5, 1], 2), [0, 3, 5]),
    (([1, 2, 1, 2, 1, 2, 1, 2, 1], 2), [0, 2, 4]),
    (([4, 5, 10, 6, 11, 17, 4, 11, 1, 3], 1), [4, 5, 7]),
    (([1, 1, 1], 1), [0, 1, 2]),
    (([7, 7, 7, 7, 7, 7], 2), [0, 2, 4]),
] + _cases()
