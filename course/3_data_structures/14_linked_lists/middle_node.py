"""
Middle of the Linked List                                                     [easy]

Return the middle node of the list. With two middle nodes (even length),
return the second one.

Example:
    1 -> 2 -> 3 -> 4 -> 5          middle is 3   (test shows [3, 4, 5])
    1 -> 2 -> 3 -> 4 -> 5 -> 6     middle is 4   (test shows [4, 5, 6])

The tests print the list starting from the node you return.

Aim for:  O(n) time, O(1) space, one pass
Hint:     Fast and slow pointers: fast moves two steps for every one of slow.
"""
from helpers import ListNode, build_list, to_list


def middle_node(head: ListNode | None) -> ListNode | None:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_list(values),)


FINISH = to_list

TESTS = [
    (([1, 2, 3, 4, 5],), [3, 4, 5]),
    (([1, 2, 3, 4, 5, 6],), [4, 5, 6]),
    (([1],), [1]),
    (([1, 2],), [2]),
]
