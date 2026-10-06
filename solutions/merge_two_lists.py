from helpers import ListNode


def merge_two_lists(a: ListNode | None, b: ListNode | None) -> ListNode | None:
    # A dummy node means the first real node isn't a special case. O(n + m).
    dummy = tail = ListNode()
    while a and b:
        if a.val <= b.val:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b         # one list is empty; attach what's left of the other
    return dummy.next
