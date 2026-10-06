"""
Network Delay Time                                                          [medium]

There are n computers labelled 1 to n. times[i] = [u, v, w] means a signal
from u reaches v after w milliseconds (one-way). A signal is sent from
computer k. Return how long until EVERY computer has it, or -1 if some never
get it.

Example:
    network_delay([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2)  ->  2

Aim for:  O(E log V)
Hint:     Dijkstra from k gives the earliest arrival at each computer. The
          answer is the LARGEST of those, unless some computer was never reached.
"""


def network_delay(times: list[list[int]], n: int, k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2), 2),
    (([[1, 2, 1]], 2, 1), 1),
    (([[1, 2, 1]], 2, 2), -1),
    (([[1, 2, 1], [2, 3, 2], [1, 3, 4]], 3, 1), 3),
    (([[1, 2, 5], [1, 3, 1], [3, 2, 1]], 3, 1), 2),
]
