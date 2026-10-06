r"""
Binary min-heap — a complete binary tree stored in a plain list, where every
parent is <= its children. So the smallest item is always at index 0.

    list:  [1, 3, 2, 7, 4, 5]          tree:        1
                                                   / \
    children of i:  2i + 1, 2i + 2               3   2
    parent of i:    (i - 1) // 2                / \  /
                                               7  4 5

Operation   Cost       How
peek        O(1)       it's heap[0]
push        O(log n)   add at the end, "sift up" while smaller than parent
pop         O(log n)   move the last item to the root, "sift down" to the smaller child
heapify     O(n)       sift down every non-leaf, from the bottom up

Python's `heapq` module does exactly this on a list. For a max-heap, push
negated values: heappush(h, -x).

Used for: top-k problems, Dijkstra, merging sorted lists, scheduling, heap sort.

Press Run to see the demo at the bottom of this file.
"""


class MinHeap:
    def __init__(self, values=()):
        self.items = list(values)
        # Heapify: leaves are already valid heaps, so start at the last parent.
        for i in range(len(self.items) // 2 - 1, -1, -1):
            self._sift_down(i)

    def push(self, val):
        self.items.append(val)
        self._sift_up(len(self.items) - 1)

    def pop(self):
        if not self.items:
            raise IndexError("pop from empty heap")
        last = self.items.pop()
        if not self.items:
            return last
        smallest, self.items[0] = self.items[0], last
        self._sift_down(0)
        return smallest

    def peek(self):
        return self.items[0] if self.items else None

    def _sift_up(self, i):
        while i > 0:
            parent = (i - 1) // 2
            if self.items[i] >= self.items[parent]:
                break
            self.items[i], self.items[parent] = self.items[parent], self.items[i]
            i = parent

    def _sift_down(self, i):
        n = len(self.items)
        while True:
            smallest = i
            for child in (2 * i + 1, 2 * i + 2):
                if child < n and self.items[child] < self.items[smallest]:
                    smallest = child
            if smallest == i:
                return
            self.items[i], self.items[smallest] = self.items[smallest], self.items[i]
            i = smallest

    def __len__(self):
        return len(self.items)

    def __str__(self):
        """Draw the heap level by level."""
        if not self.items:
            return "(empty)"
        lines, level, start = [], 0, 0
        while start < len(self.items):
            count = 2 ** level
            row = self.items[start:start + count]
            gap = 2 ** (4 - min(level, 4))
            lines.append(" " * (gap // 2) + (" " * gap).join(f"{x:>2}" for x in row))
            start += count
            level += 1
        return "\n".join(lines)


if __name__ == "__main__":
    heap = MinHeap([9, 4, 7, 1, 8, 2, 6, 3, 5])
    print("heapify([9, 4, 7, 1, 8, 2, 6, 3, 5]) →", heap.items, "\n")
    print(heap, "\n")
    heap.push(0)
    print("push(0) sifts it all the way up →", heap.items)
    print("pop() repeatedly gives sorted order:", [heap.pop() for _ in range(len(heap))])
