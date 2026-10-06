from helpers import ListNode


def reverse_list(head: ListNode | None) -> ListNode | None:
    # Iterative: flip each .next pointer as we walk. O(n) time, O(1) space.
    prev = None
    current = head
    while current:
        nxt = current.next     # remember the rest of the list
        current.next = prev    # flip the pointer
        prev = current         # step forward
        current = nxt
    return prev


def reverse_list_recursive(head: ListNode | None) -> ListNode | None:
    # Recursive: reverse the rest, then hook head on at the end. O(n) stack space.
    if head is None or head.next is None:
        return head
    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head
