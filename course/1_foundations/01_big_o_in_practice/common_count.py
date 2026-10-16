"""
How many are shared?                                                         [guided]

Return how many elements of `b` also appear somewhere in `a`. Duplicates in `b`
each count. Duplicates in `a` don't matter.

Example:
    common_count([1, 2, 3], [2, 2, 5])  ->  2      (both 2s count, 5 doesn't)

The point of this one is the last step: the same correct idea can be
fast or hopelessly slow depending on one data structure choice.
"""


def common_count(a: list[int], b: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(3)
    a = [rng.randint(0, 400_000) for _ in range(100_000)]
    b = [rng.randint(0, 400_000) for _ in range(100_000)]
    present = set(a)
    return a, b, sum(x in present for x in b)


_A, _B, _ANS = _big()

TEACHES = ["hash.set_lookup"]
USES = []

STEPS = [
    {
        "title": "Make it work",
        "text": "Loop over b and count the elements that are also in a.",
        "hint": "for x in b: if x in a: count += 1. That's correct already. Speed comes later.",
        "tests": [
            (([1, 2, 3], [2, 2, 5]), 2),
            (([5, 6, 7], [7, 6, 5]), 3),
            (([1, 2], [3, 4]), 0),
        ],
    },
    {
        "title": "Edge cases",
        "text": "Empty lists, repeats in a, negative numbers. Your answer should already handle these. Check that it does.",
        "hint": "Repeats in a must not double count. Only b's elements are counted.",
        "tests": [
            (([], [1, 2]), 0),
            (([1, 2], []), 0),
            (([4, 4, 4], [4]), 1),
            (([-1, 0, 1], [-1, -1, 2]), 2),
        ],
    },
    {
        "title": "Make it fast",
        "text": "Now a and b each have 100,000 numbers. `x in a` on a list scans the whole list, so the loop does "
                "100,000 × 100,000 comparisons. Change one thing so each lookup is O(1).",
        "hint": "Build set(a) once before the loop. Membership in a set is a hash lookup, so the whole thing becomes O(n + m).",
        "tests": [
            (([3, 1, 2], [1, 1, 1, 9]), 3),
            ((_A, _B), _ANS),
        ],
    },
]
