"""
Median of Two Sorted Arrays                                                     [hard]

Return the median of all the numbers in two sorted arrays combined, as a float.
At least one array is non-empty.

Example:
    median_two_sorted([1, 3], [2])     ->  2.0
    median_two_sorted([1, 2], [3, 4])  ->  2.5

Aim for:  O(log(min(m, n))). Merging is O(m + n). It works, but it misses the point.
Hint:     Binary search a cut in the shorter array: take i from a and (m + n + 1) // 2 - i from b.
          The cut is right when a[i-1] <= b[j] and b[j-1] <= a[i]. Use -inf/inf past the ends.
          Then the median comes from the four values around the cut.
"""


def median_two_sorted(a: list[int], b: list[int]) -> float:
    raise NotImplementedError  # replace this line with your solution


def _ref(a, b):
    c = sorted(a + b)
    n = len(c)
    return float(c[n // 2]) if n % 2 else (c[n // 2 - 1] + c[n // 2]) / 2


def _cases():
    import random
    rng = random.Random(56)
    out = []
    for _ in range(12):
        a = sorted(rng.randint(-50, 50) for _ in range(rng.randint(0, 9)))
        b = sorted(rng.randint(-50, 50) for _ in range(rng.randint(0 if a else 1, 9)))
        out.append(((a, b), _ref(a, b)))
    return out


USES = ["bsearch.first_true"]

TESTS = [(([1, 3], [2]), 2.0), (([1, 2], [3, 4]), 2.5), (([], [1]), 1.0), (([2], []), 2.0),
         (([0, 0], [0, 0]), 0.0), (([1, 2, 3, 4, 5], [6, 7, 8]), 4.5)] + _cases()
