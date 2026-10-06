from helpers import ListNode


def remove_nth_from_end(head: ListNode | None, n: int) -> ListNode | None:
    # Keep a gap of n nodes between two pointers. The dummy makes removing the
    # head the same as removing any other node. One pass, O(1) space.
    dummy = ListNode(0, head)
    front = back = dummy
    for _ in range(n + 1):
        front = front.next
    while front:
        front = front.next
        back = back.next
    back.next = back.next.next           # back sits just before the node to remove
    return dummy.next
