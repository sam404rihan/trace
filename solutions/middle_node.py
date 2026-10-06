from helpers import ListNode


def middle_node(head: ListNode | None) -> ListNode | None:
    # Fast moves 2 for every 1 of slow; when fast runs out, slow is halfway. O(n), O(1).
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
