class _Node:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=None, value=None):
        self.key, self.value, self.prev, self.next = key, value, None, None


class LRUCache:
    """dict for O(1) lookup + doubly linked list for O(1) reordering.
    The list runs oldest (just after head) -> newest (just before tail)."""

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.nodes = {}
        self.head, self.tail = _Node(), _Node()      # sentinels: no edge cases at the ends
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, node):
        node.prev.next, node.next.prev = node.next, node.prev

    def _append(self, node):                         # insert just before tail = most recent
        node.prev, node.next = self.tail.prev, self.tail
        self.tail.prev.next = node
        self.tail.prev = node

    def get(self, key):
        node = self.nodes.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._append(node)
        return node.value

    def put(self, key, value) -> None:
        node = self.nodes.get(key)
        if node:
            node.value = value
            self._unlink(node)
        else:
            node = self.nodes[key] = _Node(key, value)
        self._append(node)
        if len(self.nodes) > self.capacity:
            oldest = self.head.next
            self._unlink(oldest)
            del self.nodes[oldest.key]

    def keys(self) -> list:
        out, node = [], self.head.next
        while node is not self.tail:
            out.append(node.key)
            node = node.next
        return out
