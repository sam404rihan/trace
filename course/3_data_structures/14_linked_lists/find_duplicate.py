"""
Find the Duplicate Number                                                     [medium]

nums has n + 1 numbers, each between 1 and n, so at least one value repeats.
Exactly one value repeats (possibly more than twice). Return it, without
modifying nums and using O(1) extra space.

Example:
    find_duplicate([1, 3, 4, 2, 2])  ->  2
    find_duplicate([3, 3, 3, 3, 3])  ->  3

Aim for:  O(n) time, O(1) space. Floyd's cycle detection on an array.
Hint:     Read each value as a pointer: i → nums[i]. Start at index 0. Because two indexes
          point at the duplicate value, this "linked list" has a cycle, and the duplicate
          is where the cycle starts. Phase 1: fast and slow meet. Phase 2: restart one at 0,
          move both one step at a time, and they meet at the duplicate.
"""


def find_duplicate(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _cases():
    import random
    rng = random.Random(62)
    out = []
    for _ in range(8):
        n = rng.randint(1, 30)
        dup = rng.randint(1, n)
        others = [v for v in range(1, n + 1) if v != dup]
        rng.shuffle(others)
        keep = others[:rng.randint(0, len(others))]
        nums = keep + [dup] * (n + 1 - len(keep))
        rng.shuffle(nums)
        out.append(((nums,), dup))
    return out


USES = ["list.fast_slow", "list.cycle_start"]

TESTS = [(([1, 3, 4, 2, 2],), 2), (([3, 1, 3, 4, 2],), 3), (([3, 3, 3, 3, 3],), 3), (([1, 1],), 1),
         (([2, 5, 9, 6, 9, 3, 8, 9, 7, 1],), 9)] + _cases()
