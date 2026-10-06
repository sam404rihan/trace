"""
Reorder List                                                                  [medium]

Rearrange L0 → L1 → … → Ln into L0 → Ln → L1 → Ln-1 → L2 → … by relinking the
nodes (don't change their values). Return the head.

Example:
    1 → 2 → 3 → 4 → 5   becomes   1 → 5 → 2 → 4 → 3

Aim for:  O(n) time, O(1) extra space.
Hint:     Three moves you already know. Find the middle (fast and slow pointers), reverse
          the second half, then merge the two halves by alternating nodes.
"""
from helpers import ListNode, build_list, to_list



def reorder_list(head: ListNode | None) -> ListNode | None:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_list(values),)


FINISH = to_list


def _ref(v):
    out, i, j = [], 0, len(v) - 1
    while i <= j:
        out.append(v[i])
        if i != j:
            out.append(v[j])
        i, j = i + 1, j - 1
    return out


TESTS = [((v,), _ref(v)) for v in ([1, 2, 3, 4], [1, 2, 3, 4, 5], [1], [], [1, 2], list(range(1, 12)), [7, 7, 8, 8, 9])]
