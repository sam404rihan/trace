"""
Remove Nth Node From End                                                    [medium]

Remove the n-th node from the END of the list and return the head.
(1 <= n <= length of the list)

Example:
    remove_nth_from_end(1 -> 2 -> 3 -> 4 -> 5, 2)  ->  1 -> 2 -> 3 -> 5

Aim for:  O(n), one pass
Hint:     Start two pointers at a dummy node. Move `front` n + 1 steps ahead,
          then move both until front falls off the end. `back.next` is the
          node to remove. The dummy handles removing the head.
"""
from helpers import ListNode, build_list, to_list


def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, n):
    return (build_list(values), n)


FINISH = to_list

USES = ["list.dummy"]

TESTS = [
    (([1, 2, 3, 4, 5], 2), [1, 2, 3, 5]),
    (([1], 1), []),
    (([1, 2], 1), [1]),
    (([1, 2], 2), [2]),
]
