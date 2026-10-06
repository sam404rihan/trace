"""
Find Minimum in Rotated Sorted Array                                          [medium]

A sorted array of distinct numbers was rotated at some unknown point (for
example [0, 1, 2, 4, 5, 6, 7] became [4, 5, 6, 7, 0, 1, 2]). Return its minimum.

Example:
    find_min_rotated([3, 4, 5, 1, 2])  ->  1

Aim for:  O(log n).
Hint:     Compare nums[mid] with nums[hi]. If nums[mid] > nums[hi], the drop (and the minimum)
          is to the right of mid. Otherwise the minimum is at mid or to its left.
"""


def find_min_rotated(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _cases():
    import random
    rng = random.Random(55)
    out = []
    for _ in range(10):
        a = sorted(rng.sample(range(-1000, 1000), rng.randint(1, 30)))
        k = rng.randrange(len(a))
        r = a[k:] + a[:k]
        out.append(((r,), min(r)))
    return out


TESTS = [(([3, 4, 5, 1, 2],), 1), (([4, 5, 6, 7, 0, 1, 2],), 0), (([11, 13, 15, 17],), 11), (([1],), 1),
         (([2, 1],), 1)] + _cases()
