def cycle_start(head):
    # Phase 1: fast and slow meet inside the loop. Phase 2: from the head and from the
    # meeting point, both one step at a time, they meet where the loop begins. O(n), O(1).
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            slow = head
            while slow is not fast:
                slow, fast = slow.next, fast.next
            return slow
    return None
