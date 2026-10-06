"""
Smallest ship that makes it                                                  [guided]

Packages must ship in the given order. Each day you load packages onto the
ship until the next one would go over its capacity, then sail. Return the
smallest capacity that ships everything within `days` days.

Example:
    ship_capacity([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)  ->  15
        capacity 15: [1-5] [6,7] [8] [9] [10]  = 5 days

This is binary search on the answer: there's no sorted array, but "does
capacity c work?" flips from no to yes exactly once as c grows.
"""


def ship_capacity(weights: list[int], days: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _days_needed(weights, cap):
    used, load = 1, 0
    for w in weights:
        if load + w > cap:
            used, load = used + 1, 0
        load += w
    return used


def _big():
    import random
    rng = random.Random(10)
    weights = [rng.randint(1, 500) for _ in range(50_000)]
    days = 37
    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if _days_needed(weights, mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return weights, days, lo


_W, _D, _CAP = _big()

STEPS = [
    {
        "title": "Can this capacity work?",
        "text": "First write the check: simulate the loading for a capacity c and count the days. Then try "
                "c = max(weights), max + 1, … and return the first one that fits in `days`.",
        "hint": "Start days_used = 1 and load = 0. For each w: if load + w > c, start a new day (load = 0). Then add w. "
                "The smallest possible capacity is max(weights), since the heaviest package must fit.",
        "tests": [
            (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), 15),
            (([3, 2, 2, 4, 1, 4], 3), 6),
            (([1, 2, 3, 1, 1], 4), 3),
        ],
    },
    {
        "title": "Edges",
        "text": "One day means one trip with everything: the capacity is the total. As many days as packages "
                "means one package per day: the capacity is the heaviest.",
        "hint": "The answer always lies between max(weights) and sum(weights). Those two are your search bounds.",
        "tests": [
            (([5, 1, 4], 1), 10),
            (([5, 1, 4], 3), 5),
            (([7], 4), 7),
        ],
    },
    {
        "title": "Search, don't scan",
        "text": "50,000 packages: trying every capacity between max and sum means millions of simulations. The check "
                "is monotonic: if c works, every bigger c works too. So binary search for the first c that works.",
        "hint": "lo, hi = max(w), sum(w). while lo < hi: mid = (lo + hi) // 2; if fits(mid): hi = mid else: lo = mid + 1. "
                "That's about 25 simulations instead of millions.",
        "tests": [
            (([10, 50, 100, 100, 50, 100, 100, 100], 5), 160),
            ((_W, _D), _CAP),
        ],
    },
]
