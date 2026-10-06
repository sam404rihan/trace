from helpers import ListNode


def insert_after(head: ListNode, i: int, val: int) -> ListNode:
    cur = head
    for _ in range(i):
        cur = cur.next
    # New node points at the rest FIRST, so nothing is ever unreachable.
    cur.next = ListNode(val, cur.next)
    return head
