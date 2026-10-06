"""
Reverse Linked List                                             [easy] · linked list

Reverse a singly linked list and return the new head.

Example:
    1 -> 2 -> 3 -> 4 -> 5   becomes   5 -> 4 -> 3 -> 2 -> 1

Each node has .val and .next (see ListNode in helpers.py). The tests are
written as plain lists; the playground turns them into linked lists for you.

Aim for:  O(n) time, O(1) space. Then try it recursively too.
Hint:     Walk the list keeping three pointers: prev, current, next.
"""
from helpers import ListNode, build_list, to_list


def reverse_list(head: ListNode | None) -> ListNode | None:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_list(values),)


FINISH = to_list

TESTS = [
    (([1, 2, 3, 4, 5],), [5, 4, 3, 2, 1]),
    (([1, 2],), [2, 1]),
    (([7],), [7]),
    (([],), []),
]
