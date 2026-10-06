"""
One house at a time                                                         [snippet]

House robber: you can't rob two neighbouring houses. Walking left to right,
you only need two numbers:

    prev2 = the best total for the houses up to two houses back
    prev1 = the best total for the houses up to the previous one

A house worth x comes next. Return the best total including it.

Example:
    robber_step(4, 5, 3)   ->  7       rob it: 4 + 3 = 7 beats skipping it (5)
    robber_step(4, 9, 3)   ->  9       skip it: 9 beats 4 + 3

Hint:     Two choices. Skip this house (keep prev1), or rob it (prev2 + x, since the
          neighbour must have been skipped). This one line is the whole recurrence.
"""


def robber_step(prev2: int, prev1: int, x: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((4, 5, 3), 7),
    ((4, 9, 3), 9),
    ((0, 0, 6), 6),
    ((2, 7, 5), 7),
    ((10, 10, 1), 11),
]
