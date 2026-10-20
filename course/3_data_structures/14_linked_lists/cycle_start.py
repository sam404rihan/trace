"""
Where the Cycle Starts                                                        [easy]

The linked list may loop back on itself. Return the node where the loop
begins (the first node you would reach twice), or None if there's no loop.

Each test is (values, pos): the tail points back to the node at index pos,
or nowhere if pos is -1. Values are all different, and the test reads the
value of the node you return.

Example:
    3 -> 2 -> 0 -> -4
         ^__________|       cycle_start(head)  ->  the node holding 2

Aim for:  O(n) time, O(1) space. A set of visited nodes works, but uses O(n) space.
Hint:     First move fast and slow pointers until they meet, as in "Linked List
          Cycle". Then put one pointer back at the head and move both one step
          at a time: they meet exactly where the loop begins.
"""
from helpers import ListNode, build_list


def cycle_start(head: ListNode | None) -> ListNode | None:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, pos):
    return (build_list(values, cycle_to=pos),)


def FINISH(node):
    return None if node is None else node.val


TEACHES = ["list.cycle_start"]
USES = ["list.fast_slow"]

TESTS = [
    (([3, 2, 0, -4], 1), 2),
    (([1, 2], 0), 1),
    (([1], 0), 1),
    (([1], -1), None),
    (([], -1), None),
    (([1, 2, 3, 4, 5], -1), None),
    ((list(range(10)), 7), 7),
    ((list(range(10_000)), 3_000), 3_000),
]
