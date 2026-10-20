"""
Smash the stones                                                             [guided]

Each turn, take the two heaviest stones and smash them together. If they
weigh the same, both are destroyed. Otherwise the heavier one survives with
weight (heavier − lighter). Keep going until at most one stone is left.
Return its weight, or 0 if none are left.

Example:
    last_stone([2, 7, 4, 1, 8, 1])  ->  1
        8,7 → 1   then 4,2 → 2   then 2,1 → 1   then 1,1 → 0   leaves [1]
"""
import heapq


def last_stone(stones: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(19)
    stones = [rng.randint(1, 10**9) for _ in range(60_000)]
    h = [-s for s in stones]
    heapq.heapify(h)
    while len(h) > 1:
        a, b = -heapq.heappop(h), -heapq.heappop(h)
        if a != b:
            heapq.heappush(h, -(a - b))
    return stones, (-h[0] if h else 0)


_STONES, _LAST = _big()

TEACHES = ["heap.max_negate"]
USES = []

STEPS = [
    {
        "title": "Make it work",
        "text": "Simulate it directly: sort the list, take the two biggest from the end, push back the difference if it isn't 0, repeat.",
        "hint": "while len(stones) > 1: stones.sort(); a = stones.pop(); b = stones.pop(); if a != b: stones.append(a - b)",
        "tests": [
            (([2, 7, 4, 1, 8, 1],), 1),
            (([10, 4],), 6),
            (([3, 3, 3],), 3),
        ],
    },
    {
        "title": "Edges",
        "text": "One stone, two equal stones, no stones at all.",
        "hint": "Return stones[0] if one is left, else 0.",
        "tests": [
            (([5],), 5),
            (([6, 6],), 0),
            (([],), 0),
        ],
    },
    {
        "title": "Use a heap",
        "text": "With 60,000 stones, sorting before every smash costs n log n each time, for up to n smashes. You only ever "
                "need the two biggest. heapq is a min-heap, so store negated weights to get a max-heap.",
        "hint": "h = [-s for s in stones]; heapify(h). Then pop twice, push -(a - b) if a != b. O(n log n) total. "
                "Or skip the negating: heapify_max(h), heappop_max(h), heappush_max(h, x) are preloaded.",
        "tests": [
            (([1, 1, 2, 2, 9],), 3),
            ((_STONES,), _LAST),
        ],
    },
]
