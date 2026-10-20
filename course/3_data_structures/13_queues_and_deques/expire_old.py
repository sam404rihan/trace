"""
Expire old events                                                           [snippet]

`q` is a collections.deque of event times, oldest on the left. Remove every
event that is too old for the window (now - window, now], then return how
many events are left.

Example:
    expire_old(deque([1, 4, 7, 9]), 10, 5)  ->  2      only 7 and 9 are inside (5, 10]

Hint:     while q and q[0] <= now - window: q.popleft()
          Old events are always at the front, because times only go up.
"""
from collections import deque


def expire_old(q: deque, now: int, window: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(times, now, window):
    return deque(times), now, window


USES = ["window.variable"]

TESTS = [
    (([1, 4, 7, 9], 10, 5), 2),
    (([1, 2, 3], 3, 10), 3),
    (([1, 2, 3], 100, 10), 0),
    (([], 5, 5), 0),
    (([5, 6], 10, 5), 1),
]
