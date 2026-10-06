def reorder_list(head):
    if not head or not head.next:
        return head
    slow, fast = head, head.next            # 1) find the middle
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
    second, slow.next = slow.next, None     # cut the list in two
    prev = None                             # 2) reverse the second half
    while second:
        second.next, prev, second = prev, second, second.next
    first, second = head, prev              # 3) weave the halves together
    while second:
        nxt1, nxt2 = first.next, second.next
        first.next, second.next = second, nxt1
        first, second = nxt1, nxt2
    return head
