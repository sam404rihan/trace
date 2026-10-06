"""
Singly linked list — a chain of nodes, each holding a value and a pointer to the next.

    head
     │
    [1] ─→ [2] ─→ [3] ─→ None

Operation               Cost    Why
─────────────────────── ─────── ────────────────────────────────────────────
prepend (add at head)   O(1)    just point a new node at the old head
append (with tail ptr)  O(1)    we keep a pointer to the last node
find / index            O(n)    no random access: you must walk the chain
insert after a node     O(1)    re-link two pointers (finding the node is O(n))
delete by value         O(n)    find it, then re-link around it

vs. a Python list (a dynamic array): O(1) indexing, but inserting at the front
is O(n) because every element shifts over.

Press Run to see the demo at the bottom of this file.
"""


class Node:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next


class LinkedList:
    def __init__(self, values=()):
        self.head = None
        self.tail = None
        self.size = 0
        for v in values:
            self.append(v)

    def prepend(self, val):
        self.head = Node(val, self.head)
        if self.tail is None:
            self.tail = self.head
        self.size += 1

    def append(self, val):
        node = Node(val)
        if self.tail is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node
        self.size += 1

    def find(self, val):
        """Return the first node holding val, or None."""
        node = self.head
        while node:
            if node.val == val:
                return node
            node = node.next
        return None

    def insert_after(self, node, val):
        node.next = Node(val, node.next)
        if node is self.tail:
            self.tail = node.next
        self.size += 1

    def delete(self, val):
        """Remove the first node holding val. Returns True if something was removed."""
        prev, node = None, self.head
        while node and node.val != val:
            prev, node = node, node.next
        if node is None:
            return False
        if prev is None:
            self.head = node.next          # deleting the head
        else:
            prev.next = node.next          # skip over the node
        if node is self.tail:
            self.tail = prev
        self.size -= 1
        return True

    def reverse(self):
        prev, node = None, self.head
        self.tail = self.head
        while node:
            node.next, prev, node = prev, node, node.next
        self.head = prev

    def __iter__(self):
        node = self.head
        while node:
            yield node.val
            node = node.next

    def __len__(self):
        return self.size

    def __repr__(self):
        return " -> ".join(map(repr, self)) + " -> None" if self.head else "(empty)"


if __name__ == "__main__":
    items = LinkedList([1, 2, 3])
    print("start:          ", items)
    items.prepend(0)
    print("prepend(0):     ", items)
    items.append(4)
    print("append(4):      ", items)
    items.insert_after(items.find(2), 2.5)
    print("insert 2.5:     ", items)
    items.delete(0)
    print("delete(0):      ", items)
    items.reverse()
    print("reverse():      ", items)
    print("len:            ", len(items))
