"""
Reverse part of a list                                                       [guided]

Reverse the nodes from position `left` to position `right` (1-based, both
included) and return the head of the whole list.

Example:
    1 -> 2 -> 3 -> 4 -> 5,  left = 2, right = 4   ->   1 -> 4 -> 3 -> 2 -> 5

You'll start by reversing a whole list, then reverse a section, then make
it safe when the section starts at the head.
"""
from helpers import ListNode, build_list, to_list


def reverse_between(head: ListNode | None, left: int, right: int) -> ListNode | None:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, left, right):
    return build_list(values), left, right


FINISH = to_list

STEPS = [
    {
        "title": "Reverse everything",
        "text": "These tests reverse the whole list (left = 1, right = n). Use prev / curr / nxt: save next, flip the link, "
                "advance both pointers.",
        "hint": "while curr: nxt = curr.next; curr.next = prev; prev = curr; curr = nxt. The new head is prev.",
        "tests": [
            (([1, 2, 3, 4, 5], 1, 5), [5, 4, 3, 2, 1]),
            (([1, 2], 1, 2), [2, 1]),
        ],
    },
    {
        "title": "Reverse a section",
        "text": "Walk to the node just before position left (call it before). Reverse right - left + 1 nodes starting "
                "after it, then reconnect: before.next becomes the reversed section's new first node, and the old "
                "first node (now last) points to whatever came after the section.",
        "hint": "Keep a reference to the section's first node before you reverse it: it becomes the tail you reconnect.",
        "tests": [
            (([1, 2, 3, 4, 5], 2, 4), [1, 4, 3, 2, 5]),
            (([1, 2, 3, 4, 5, 6], 3, 6), [1, 2, 6, 5, 4, 3]),
            (([9, 8, 7, 6], 2, 3), [9, 7, 8, 6]),
        ],
    },
    {
        "title": "Edges",
        "text": "When left = 1 there's no node before the section, so the head itself changes. A dummy node in front "
                "of the head removes that special case. Also: a single node, and left == right.",
        "hint": "dummy = ListNode(0, head); before = dummy; walk left - 1 steps. Return dummy.next.",
        "tests": [
            (([1, 2, 3, 4], 1, 2), [2, 1, 3, 4]),
            (([5], 1, 1), [5]),
            (([1, 2, 3], 2, 2), [1, 2, 3]),
            (([3, 5], 1, 1), [3, 5]),
        ],
    },
]
