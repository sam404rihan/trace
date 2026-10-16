"""
Fewest steps to a number                                                      [easy]

Start at the number `start`. Each step changes it by +1, by -1, or doubles it.
Return the fewest steps to reach `target`. The number must stay between 0 and
2 * max(start, target) (going outside that range never helps).

Example:
    fewest_steps(1, 10)  ->  4      (1 -> 2 -> 4 -> 5 -> 10)
    fewest_steps(10, 1)  ->  9

Aim for:  O(max(start, target)).
Hint:     The numbers are the nodes, but nobody gives you a neighbour list: you make it.
          The neighbours of x are x + 1, x - 1 and x * 2 (when they stay in range).
          Then it's the usual BFS from start, with a dict of distances.
"""


def fewest_steps(start: int, target: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["bfs.implicit"]
USES = ["bfs.shortest"]

TESTS = [
    ((5, 8), 2),
    ((1, 10), 4),
    ((10, 1), 9),
    ((3, 3), 0),
    ((0, 5), 4),
    ((7, 100), 6),
]
