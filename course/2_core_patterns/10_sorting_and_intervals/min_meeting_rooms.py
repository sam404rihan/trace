"""
Meeting Rooms II                                                              [medium]

Given meeting times [start, end], return the minimum number of rooms needed so
every meeting has a room. A meeting ending at time t frees its room for a
meeting starting at t.

Example:
    min_meeting_rooms([[0, 30], [5, 10], [15, 20]])  ->  2
    min_meeting_rooms([[7, 10], [2, 4]])             ->  1

Aim for:  O(n log n).
Hint:     Sort by start. Keep a min-heap of the end times of rooms in use. For each meeting, if the
          earliest-ending room is free by its start, reuse it (pop). Then push this meeting's end.
          The heap's largest size is the answer. (Or sweep sorted starts and ends with two pointers.)
"""


def min_meeting_rooms(intervals: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(iv):
    points = sorted({x for s, e in iv for x in (s, e)})
    return max((sum(1 for s, e in iv if s <= t < e) for t in points), default=0)


def _make(rng):
    out = []
    for _ in range(rng.randint(0, 10)):
        s = rng.randint(0, 20)
        out.append([s, s + rng.randint(1, 8)])
    return (out,)


def _cases():
    import random
    rng = random.Random(121)
    out = []
    for _ in range(10):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


TESTS = [(([[0, 30], [5, 10], [15, 20]],), 2), (([[7, 10], [2, 4]],), 1), (([[1, 5], [5, 10]],), 1), (([],), 0)] + _cases()
