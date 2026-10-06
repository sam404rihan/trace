"""
Linked List Cycle                                               [easy] · linked list

Return True if the linked list loops back on itself somewhere.

Each test is (values, pos): the tail node points back to the node at index
`pos`, or nowhere if pos is -1. Your function only receives the head.

Example:
    3 -> 2 -> 0 -> -4
         ^__________|       has_cycle(head)  ->  True

Aim for:  O(n) time, O(1) space
Hint:     A set of visited nodes works but costs O(n) space. Try two pointers
          that move at different speeds (Floyd's "tortoise and hare").
"""
from helpers import ListNode, build_list


def has_cycle(head: ListNode | None) -> bool:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, pos):
    return (build_list(values, cycle_to=pos),)


TESTS = [
    (([3, 2, 0, -4], 1), True),
    (([1, 2], 0), True),
    (([1], 0), True),
    (([1], -1), False),
    (([], -1), False),
    (([1, 2, 3, 4, 5], -1), False),
]
