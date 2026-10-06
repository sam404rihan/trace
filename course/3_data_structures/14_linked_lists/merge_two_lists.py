"""
Merge Two Sorted Lists                                          [easy] · linked list

`a` and `b` are sorted linked lists. Splice them together into one sorted
linked list and return its head.

Example:
    1 -> 2 -> 4   and   1 -> 3 -> 4   become   1 -> 1 -> 2 -> 3 -> 4 -> 4

Aim for:  O(n + m) time, O(1) extra space (re-use the existing nodes)
Hint:     A "dummy" head node saves you from special-casing the first node.
"""
from helpers import ListNode, build_list, to_list


def merge_two_lists(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(a, b):
    return (build_list(a), build_list(b))


FINISH = to_list

TESTS = [
    (([1, 2, 4], [1, 3, 4]), [1, 1, 2, 3, 4, 4]),
    (([], []), []),
    (([], [0]), [0]),
    (([5], [1, 2, 3]), [1, 2, 3, 5]),
]
