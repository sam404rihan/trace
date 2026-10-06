"""
Car Fleet                                                                     [medium]

Cars drive along a one-lane road towards `target`. Car i starts at position[i]
with speed[i]. A car can't pass the one ahead. When it catches up, it slows
down and they drive on together as one fleet. A car that catches up exactly at
the target also joins that fleet. How many fleets arrive?

Example:
    car_fleet(12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3])  ->  3

Aim for:  O(n log n).
Hint:     Sort cars by position, closest to the target first, and compute each one's arrival
          time (target - pos) / speed. Going back down the road, a car whose time is <= the
          fleet ahead of it merges into that fleet. A slower time starts a new fleet.
          (A stack of times works, but one variable is enough.)
"""


def car_fleet(target: int, position: list[int], speed: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]), 3),
    ((10, [3], [3]), 1),
    ((100, [0, 2, 4], [4, 2, 1]), 1),
    ((10, [6, 8], [3, 2]), 2),
    ((10, [0, 4, 2], [2, 1, 3]), 1),
    ((20, [6, 2, 17], [3, 9, 2]), 2),
    ((10, [], []), 0),
]
