from helpers import ListNode


def reverse_between(head: ListNode | None, left: int, right: int) -> ListNode | None:
    dummy = ListNode(0, head)           # so "the node before the section" always exists
    before = dummy
    for _ in range(left - 1):
        before = before.next

    first = before.next                 # will end up as the section's tail
    prev, curr = None, first
    for _ in range(right - left + 1):   # plain reversal, for exactly this many nodes
        nxt = curr.next
        curr.next = prev
        prev, curr = curr, nxt

    before.next = prev                  # reconnect the front...
    first.next = curr                   # ...and the back
    return dummy.next
