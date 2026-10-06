"""
Stack (LIFO) and Queue (FIFO).

    Stack: last in, first out          Queue: first in, first out
      push →  ┌───┐  → pop              enqueue → [ 3 | 2 | 1 ] → dequeue
              │ 3 │ ← top
              │ 2 │
              │ 1 │

In Python:
    stack: a plain list — append() / pop() are O(1) at the end.
    queue: collections.deque — append() / popleft() are O(1).
           Don't use list.pop(0): it's O(n) because everything shifts left.

Where they show up:
    stack — undo, matching brackets, DFS, "next greater element" (monotonic stack)
    queue — BFS, scheduling, buffering

Below: both built from scratch, plus a queue made of two stacks (a classic
interview question with amortised O(1) operations).

Press Run to see the demo at the bottom of this file.
"""


class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        return self._items[-1] if self._items else None

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack(bottom→top: {self._items})"


class Queue:
    """A linked-list queue: enqueue at the tail, dequeue at the head. Both O(1)."""

    class _Node:
        def __init__(self, val):
            self.val = val
            self.next = None

    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def enqueue(self, x):
        node = self._Node(x)
        if self.tail:
            self.tail.next = node
        else:
            self.head = node
        self.tail = node
        self.size += 1

    def dequeue(self):
        if not self.head:
            raise IndexError("dequeue from empty queue")
        node = self.head
        self.head = node.next
        if self.head is None:
            self.tail = None
        self.size -= 1
        return node.val

    def __len__(self):
        return self.size

    def __repr__(self):
        items, node = [], self.head
        while node:
            items.append(node.val)
            node = node.next
        return f"Queue(front→back: {items})"


class QueueFromTwoStacks:
    """Push onto `inbox`. To dequeue, pour inbox into `outbox` (reversing it) only
    when outbox is empty. Each item moves at most once → amortised O(1)."""

    def __init__(self):
        self.inbox, self.outbox = [], []

    def enqueue(self, x):
        self.inbox.append(x)

    def dequeue(self):
        if not self.outbox:
            while self.inbox:
                self.outbox.append(self.inbox.pop())
        if not self.outbox:
            raise IndexError("dequeue from empty queue")
        return self.outbox.pop()


if __name__ == "__main__":
    s = Stack()
    for x in "abc":
        s.push(x)
    print(s, "→ pop:", s.pop(), "→", s)

    q = Queue()
    for x in "abc":
        q.enqueue(x)
    print(q, "→ dequeue:", q.dequeue(), "→", q)

    q2 = QueueFromTwoStacks()
    for x in range(1, 4):
        q2.enqueue(x)
    print("two-stack queue dequeues:", [q2.dequeue() for _ in range(3)])
