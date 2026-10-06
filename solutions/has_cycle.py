from helpers import ListNode


def has_cycle(head: ListNode | None) -> bool:
    # Floyd's tortoise and hare: in a cycle the fast pointer laps the slow one.
    # O(n) time, O(1) space.
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:       # `is` compares node identity, not value
            return True
    return False
