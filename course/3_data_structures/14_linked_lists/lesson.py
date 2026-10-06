"""
# Linked lists

A chain of nodes, each with a value and a pointer to the next: `node.val`,
`node.next`. No indexing: to reach item i you walk i steps. But inserting or
removing a node you're already at is O(1).

## Use it when
You'll mostly meet linked lists because the problem hands you one. The skill
is moving pointers without losing the rest of the list.

## The four tricks that solve nearly everything
- **Dummy head:** `dummy = ListNode(0, head)`. Build or delete from `dummy`,
  return `dummy.next`. No special case for the first node
- **Reverse:** `prev, cur = None, head` then loop: `cur.next, prev, cur = prev, cur, cur.next`
- **Fast and slow pointers:** fast moves 2, slow moves 1
  - When fast hits the end, slow is at the middle
  - If they ever meet, there's a cycle
- **Gap of n:** move one pointer n steps ahead, then move both. When the
  front one hits the end, the back one is n from the end

## Walking safely
```
node = head
while node:              # stop AFTER the last node
    ...
    node = node.next
```
Use `while node and node.next` when you look one node ahead.

## Common mistakes
- Losing the rest of the list: save `nxt = cur.next` before changing `cur.next`
- Comparing nodes with `==` when you mean the same node. Use `is`
- Forgetting to set the new tail's `.next = None`, which creates an accidental cycle

The playground's helpers: `build_list([1, 2, 3])`, `to_list(head)`, `ListNode`.
Press Run to see each trick.
"""
from helpers import ListNode, build_list, to_list

head = build_list([1, 2, 3, 4, 5])
print("list:        ", head)

# Middle with fast and slow pointers
slow = fast = head
while fast and fast.next:
    slow, fast = slow.next, fast.next.next
print("middle:      ", slow.val)

# Reverse in place
prev, cur = None, head
while cur:
    cur.next, prev, cur = prev, cur, cur.next
head = prev
print("reversed:    ", head)

# Delete every even value using a dummy head
dummy = ListNode(0, head)
node = dummy
while node.next:
    if node.next.val % 2 == 0:
        node.next = node.next.next      # skip it
    else:
        node = node.next
print("odds only:   ", to_list(dummy.next))

# Build a new list with a dummy and a tail pointer
dummy = tail = ListNode()
for v in "abc":
    tail.next = ListNode(v)
    tail = tail.next
print("built:       ", dummy.next)
