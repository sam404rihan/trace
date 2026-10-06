"""
Insert after a node                                                         [snippet]

Insert a new node with value `val` right after the node at index `i`
(0-based) and return the head. The list has at least i + 1 nodes.

Example:
    1 -> 2 -> 3,  insert_after(head, 0, 9)   ->   1 -> 9 -> 2 -> 3

Each node has .val and .next. Tests are written as plain lists, and the
playground builds the linked list for you.

Hint:     Walk i steps from head. Then the order matters: point the new node at
          cur.next FIRST, then point cur at the new node. The other way round
          loses the rest of the list.
"""
from helpers import ListNode, build_list, to_list


def insert_after(head: ListNode, i: int, val: int) -> ListNode:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, i, val):
    return build_list(values), i, val


FINISH = to_list

TESTS = [
    (([1, 2, 3], 0, 9), [1, 9, 2, 3]),
    (([1, 2, 3], 2, 9), [1, 2, 3, 9]),
    (([5], 0, 6), [5, 6]),
    (([4, 4, 4], 1, 0), [4, 4, 0, 4]),
]
