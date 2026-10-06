"""
0/1 Knapsack                                                                [medium]

Item i weighs weights[i] and is worth values[i]. Each item can be taken at
most once. Return the highest total value that fits within `capacity`.

Example:
    knapsack([1, 3, 4, 5], [1, 4, 5, 7], 7)  ->  9      items of weight 3 + 4

Aim for:  O(n · capacity) time, then O(capacity) space
Hint:     best[w] = most value with capacity w using the items seen so far.
          For each item, update w from capacity DOWN to its weight:
          best[w] = max(best[w], best[w - weight] + value). Going down keeps
          each item from being used twice.
"""


def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 3, 4, 5], [1, 4, 5, 7], 7), 9),
    (([10, 20, 30], [60, 100, 120], 50), 220),
    (([5], [10], 4), 0),
    (([], [], 10), 0),
    (([2, 2, 2], [3, 3, 3], 4), 6),
]
