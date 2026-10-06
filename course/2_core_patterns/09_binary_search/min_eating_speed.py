"""
Koko Eating Bananas                                                         [medium]

There are piles of bananas; piles[i] is the size of pile i. Each hour Koko
picks one pile and eats `speed` bananas from it (if the pile has fewer, she
finishes it and waits for the next hour). Return the minimum integer speed
that lets her finish every pile within `h` hours. (len(piles) <= h)

Example:
    min_eating_speed([3, 6, 7, 11], 8)  ->  4

Aim for:  O(n log max(piles))
Hint:     Binary search on the answer. For a given speed, the hours needed
          are sum(ceil(p / speed)). Faster speed = fewer hours, so find the
          first speed that fits in h. Ceiling without floats: (p + speed - 1) // speed
"""


def min_eating_speed(piles: list[int], h: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([3, 6, 7, 11], 8), 4),
    (([30, 11, 23, 4, 20], 5), 30),
    (([30, 11, 23, 4, 20], 6), 23),
    (([1, 1, 1, 1], 4), 1),
    (([1_000_000_000], 2), 500_000_000),
]
