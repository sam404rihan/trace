"""
Extend or restart                                                           [snippet]

You're scanning for the maximum-sum subarray. `cur` is the best sum of a run
that ends just before x. Return the best sum of a run that ends AT x.

Example:
    extend_or_restart(4, -1)   ->  3      extending (4 - 1) beats starting over at -1
    extend_or_restart(-3, 2)   ->  2      a negative run only drags 2 down: restart

This one line is the heart of Kadane's algorithm.

Hint:     Either the run continues (cur + x) or a new run starts here (x). Take the better one.
"""


def extend_or_restart(cur: int, x: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((4, -1), 3),
    ((-3, 2), 2),
    ((0, 5), 5),
    ((-1, -2), -2),
    ((10, 10), 20),
]
