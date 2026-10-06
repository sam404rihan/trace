"""
Fewest jumps to the end                                                      [guided]

From index i you can jump forward up to nums[i] steps. Starting at index 0,
return the fewest jumps to reach the last index. You can assume it's always
reachable.

Example:
    min_jumps([2, 3, 1, 1, 4])  ->  2      0 → 1 → 4
"""


def min_jumps(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(6)
    nums = [rng.randint(1, 2000) for _ in range(150_000)]
    jumps, end, far = 0, 0, 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps, end = jumps + 1, far
    return nums, jumps


_NUMS, _JUMPS = _big()

STEPS = [
    {
        "title": "Make it work",
        "text": "Fill best[i] = fewest jumps to reach i. best[0] = 0, and from each i, every j in i+1..i+nums[i] "
                "can be reached in best[i] + 1.",
        "hint": "best = [inf] * n; best[0] = 0; for i: for j in range(i + 1, min(n, i + nums[i] + 1)): "
                "best[j] = min(best[j], best[i] + 1). O(n · jump size).",
        "tests": [
            (([2, 3, 1, 1, 4],), 2),
            (([2, 3, 0, 1, 4],), 2),
            (([1, 1, 1, 1],), 3),
        ],
    },
    {
        "title": "Edges",
        "text": "A single cell needs no jumps. A first jump that clears everything needs one.",
        "hint": "Already at the end: 0.",
        "tests": [
            (([0],), 0),
            (([9, 1, 1, 1],), 1),
            (([1, 2],), 1),
        ],
    },
    {
        "title": "Think in levels",
        "text": "150,000 cells with jumps up to 2,000 is about 150 million updates, too slow. Think of it like BFS: "
                "everything reachable with k jumps is a contiguous range. Walk once, tracking the end of the "
                "current range and the farthest you could reach from inside it. When you hit the end of the range, "
                "you must jump: count it and extend the range to that farthest point.",
        "hint": "jumps = end = far = 0; for i in range(n - 1): far = max(far, i + nums[i]); "
                "if i == end: jumps += 1; end = far. O(n), one pass.",
        "tests": [
            (([1, 4, 1, 1, 1, 1],), 2),
            ((_NUMS,), _JUMPS),
        ],
    },
]
