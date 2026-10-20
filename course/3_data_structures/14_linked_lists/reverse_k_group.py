"""
Reverse Nodes in k-Group                                                        [hard]

Reverse the list k nodes at a time and return the new head. If fewer than k
nodes are left at the end, leave them as they are. Relink the nodes. Don't just
swap values.

Example:
    1 → 2 → 3 → 4 → 5,  k = 2   ->   2 → 1 → 4 → 3 → 5
    1 → 2 → 3 → 4 → 5,  k = 3   ->   3 → 2 → 1 → 4 → 5

Aim for:  O(n) time, O(1) extra space.
Hint:     A dummy node before the head, and group_prev = the node before the current group.
          Check that k nodes exist ahead. Reverse exactly those k. Then reconnect: group_prev.next
          becomes the group's new first node, and the group's old first node (now its last)
          becomes the next group_prev.
"""
from helpers import ListNode, build_list, to_list



def reverse_k_group(head: ListNode | None, k: int) -> ListNode | None:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values, k):
    return build_list(values), k


FINISH = to_list


def _ref(v, k):
    out = []
    for i in range(0, len(v), k):
        chunk = v[i:i + k]
        out += chunk[::-1] if len(chunk) == k else chunk
    return out


USES = ["list.reverse", "list.dummy"]

TESTS = [((v, k), _ref(v, k)) for v, k in (([1, 2, 3, 4, 5], 2), ([1, 2, 3, 4, 5], 3), ([1, 2, 3, 4, 5], 1),
                                           ([1, 2, 3, 4, 5], 5), ([1, 2], 3), ([], 2), (list(range(20)), 4),
                                           (list(range(23)), 6))]
