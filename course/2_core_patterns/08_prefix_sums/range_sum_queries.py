"""
Answer range-sum queries                                                     [guided]

For each query (i, j), return the sum of nums[i..j], both ends included.

Example:
    range_sum_queries([2, 4, -1, 3], [(0, 1), (1, 3), (2, 2)])  ->  [6, 6, -1]
"""


def range_sum_queries(nums: list[int], queries: list[tuple[int, int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(12)
    n = 100_000
    nums = [rng.randint(-1000, 1000) for _ in range(n)]
    queries = []
    for _ in range(100_000):
        i = rng.randint(0, n - 1)
        queries.append((i, rng.randint(i, n - 1)))
    P = [0]
    for x in nums:
        P.append(P[-1] + x)
    return nums, queries, [P[j + 1] - P[i] for i, j in queries]


_NUMS, _QS, _ANS = _big()

USES = ["prefix.sums"]

STEPS = [
    {
        "title": "Make it work",
        "text": "For each query, add up nums[i..j]. Slicing is fine: sum(nums[i:j + 1]).",
        "hint": "Mind the + 1: the slice end is exclusive, but j is included.",
        "tests": [
            (([2, 4, -1, 3], [(0, 1), (1, 3), (2, 2)]), [6, 6, -1]),
            (([1, 2, 3, 4, 5], [(0, 4), (4, 4)]), [15, 5]),
        ],
    },
    {
        "title": "Edges",
        "text": "Single-element arrays, ranges covering everything, negatives, and no queries at all.",
        "hint": "No queries means an empty result list.",
        "tests": [
            (([7], [(0, 0)]), [7]),
            (([-3, -3, -3], [(0, 2), (1, 2)]), [-9, -6]),
            (([1, 2], []), []),
        ],
    },
    {
        "title": "Precompute once",
        "text": "100,000 numbers and 100,000 queries: summing each range from scratch adds up to billions of additions. "
                "Build the prefix array once, then answer every query with one subtraction.",
        "hint": "P = [0]; for x in nums: P.append(P[-1] + x). Then sum(i..j) = P[j + 1] - P[i]. O(n + q).",
        "tests": [
            (([5, -2, 9], [(0, 2), (1, 1), (0, 0)]), [12, -2, 5]),
            ((_NUMS, _QS), _ANS),
        ],
    },
]
