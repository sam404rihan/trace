"""
Patching Array                                                                [hard]

`nums` is sorted and holds positive integers. Add ("patch in") as few new
positive integers as possible so that every number from 1 to n can be written
as the sum of some of the elements (each element used at most once).
Return the number of patches.

Example:
    patching_array([1, 3], 6)         ->  1      add 2: now 1..6 are all reachable
    patching_array([1, 5, 10], 20)    ->  2      add 2 and 4
    patching_array([1, 2, 2], 5)      ->  0

Aim for:  O(len(nums) + log n). n can be as large as 2**31 - 1.
Hint:     Track `reach`: every number in [1, reach) can already be made. If the next number x
          is <= reach, using it extends that to [1, reach + x). If it's bigger (or nums ran out),
          there's a gap at `reach` itself, and the best patch is reach: it doubles the range.
          Stop once reach > n.
"""


def patching_array(nums: list[int], n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums, n):
    """Breadth-first over how many patches: try every multiset of patches up to size 4."""
    from itertools import combinations_with_replacement

    def covers(values):
        sums = {0}
        for v in values:
            sums |= {s + v for s in sums}
        return all(k in sums for k in range(1, n + 1))

    for count in range(0, 5):
        for extra in combinations_with_replacement(range(1, n + 1), count):
            if covers(list(nums) + list(extra)):
                return count
    return None


def _cases():
    import random
    rng = random.Random(330)
    out = []
    for _ in range(8):
        nums = sorted(rng.randint(1, 10) for _ in range(rng.randint(0, 4)))
        n = rng.randint(1, 14)
        out.append(((nums, n), _brute(nums, n)))
    return out


USES = []

TESTS = [
    (([1, 3], 6), 1),
    (([1, 5, 10], 20), 2),
    (([1, 2, 2], 5), 0),
    (([], 7), 3),
    (([], 8), 4),
    (([2], 1), 1),
    (([1, 2, 31, 33], 2147483647), 28),
    (([1, 2, 4, 8, 16], 31), 0),
] + _cases()
