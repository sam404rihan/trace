"""
Count Inversions                                                              [medium]

An inversion is a pair i < j with nums[i] > nums[j]. Count them. It measures
how far from sorted the list is.

Example:
    count_inversions([2, 4, 1, 3, 5])  ->  3        (2,1) (4,1) (4,3)

Aim for:  O(n log n). The last test has 100,000 numbers.
Hint:     Merge sort. While merging two sorted halves, whenever you take an element from the RIGHT
          half, every element still waiting in the left half is bigger: add len(left) - i.
          (A Fenwick tree over values works too.)
"""


def count_inversions(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] > nums[j])


def _fast(nums):
    def sort(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, x = sort(a[:mid])
        right, y = sort(a[mid:])
        merged, i, j, inv = [], 0, 0, x + y
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1; inv += len(left) - i
        return merged + left[i:] + right[j:], inv
    return sort(nums)[1]


def _cases():
    import random
    rng = random.Random(207)
    out = []
    for _ in range(8):
        a = [rng.randint(0, 9) for _ in range(rng.randint(0, 15))]
        out.append(((a,), _brute(a)))
    big = [rng.randint(0, 10**9) for _ in range(100_000)]
    out.append(((big,), _fast(big)))
    return out


TESTS = [(([2, 4, 1, 3, 5],), 3), (([1, 2, 3],), 0), (([3, 2, 1],), 3), (([],), 0), (([2, 2],), 0)] + _cases()
