"""
Count pairs below a target                                                   [guided]

`nums` is sorted. Count the pairs i < j with nums[i] + nums[j] < target.

Example:
    count_pairs_below([1, 2, 3, 4], 6)  ->  4      (1,2) (1,3) (1,4) (2,3)

The trick you'll find in step 3: one comparison can count a whole batch of
pairs at once.
"""


def count_pairs_below(nums: list[int], target: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(21)
    nums = sorted(rng.randint(-10**6, 10**6) for _ in range(100_000))
    target = 12_345
    count, left, right = 0, 0, len(nums) - 1
    while left < right:
        if nums[left] + nums[right] < target:
            count += right - left
            left += 1
        else:
            right -= 1
    return nums, target, count


_NUMS, _T, _ANS = _big()

USES = ["pointers.opposite_ends"]

STEPS = [
    {
        "title": "Make it work",
        "text": "Check every pair with two nested loops and count the ones whose sum is below target.",
        "hint": "for i in range(n): for j in range(i + 1, n): ... It's O(n²), which is fine for now.",
        "tests": [
            (([1, 2, 3, 4], 6), 4),
            (([1, 1, 1], 3), 3),
            (([5, 6, 7], 10), 0),
        ],
    },
    {
        "title": "Edges",
        "text": "Empty and single-element lists have no pairs. Negative numbers and duplicates work as normal.",
        "hint": "With fewer than 2 numbers there are 0 pairs.",
        "tests": [
            (([], 5), 0),
            (([3], 10), 0),
            (([-5, -2, 0, 3], 0), 4),
            (([2, 2, 2, 2], 5), 6),
        ],
    },
    {
        "title": "Count in batches",
        "text": "100,000 numbers means about 5 billion pairs. Put left at the start and right at the end. "
                "If nums[left] + nums[right] < target, then left pairs with every index from left + 1 up to right, "
                "because they're all ≤ nums[right]. That's right - left pairs in one go. Then move left. Otherwise move right.",
        "hint": "if nums[left] + nums[right] < target: count += right - left; left += 1  else: right -= 1. O(n).",
        "tests": [
            (([-3, -1, 0, 2, 4, 5], 3), 8),
            ((_NUMS, _T), _ANS),
        ],
    },
]
