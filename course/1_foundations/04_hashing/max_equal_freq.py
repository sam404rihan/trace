"""
Maximum Equal Frequency                                                       [hard]

Return the length of the longest prefix of `nums` from which you can remove
EXACTLY one element so that every number left in it appears the same number of
times. (Removing the only element leaves nothing, which counts as equal.)

Example:
    max_equal_freq([2, 2, 1, 1, 5, 3, 3, 5])                  ->  7
        Take [2, 2, 1, 1, 5, 3, 3] and remove the 5: every number appears twice.
    max_equal_freq([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5])   ->  13

Aim for:  O(n), with two hash maps updated in O(1) per element.
Hint:     Keep count[x] (how often x appears) and freq[c] (how many numbers appear c times).
          After adding nums[i], the prefix works if one of these holds (m = the max count):
          every number appears once; or one number appears m times and all others m - 1;
          or one number appears once and all others m times.
"""


def max_equal_freq(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    from collections import Counter
    best = 0
    for length in range(1, len(nums) + 1):
        c = Counter(nums[:length])
        for x in list(c):
            c[x] -= 1
            if len({v for v in c.values() if v}) <= 1:
                best = length
            c[x] += 1
    return best


def _fast(nums):
    count, freq, best, top = {}, {}, 0, 0
    for i, x in enumerate(nums, 1):
        c = count.get(x, 0)
        if c:
            freq[c] -= 1
        count[x] = c + 1
        freq[c + 1] = freq.get(c + 1, 0) + 1
        top = max(top, c + 1)
        if top == 1 or freq[top] * top + freq.get(top - 1, 0) * (top - 1) == i and freq[top] == 1 \
                or freq[top] * top + 1 == i:
            best = i
    return best


def _cases():
    import random
    rng = random.Random(1224)
    out = []
    for _ in range(10):
        nums = [rng.randint(1, 4) for _ in range(rng.randint(2, 16))]
        out.append(((nums,), _brute(nums)))
    big = [rng.randint(1, 3000) for _ in range(100_000)]
    out.append(((big,), _fast(big)))
    return out


USES = []

TESTS = [
    (([2, 2, 1, 1, 5, 3, 3, 5],), 7),
    (([1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5],), 13),
    (([1, 1],), 2),
    (([1, 2],), 2),
    (([1, 1, 1, 1],), 4),
    (([1, 2, 3, 4, 5, 6],), 6),
    (([1, 1, 2, 2, 3, 3],), 5),
] + _cases()
