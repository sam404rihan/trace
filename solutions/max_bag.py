import heapq
from collections import Counter


class MaxBag:
    # Lazy deletion: removals are only counted, and dead values are popped when they reach the top.
    def __init__(self):
        self.heap = []                      # negated: a max-heap
        self.gone = Counter()               # values removed but still inside the heap

    def add(self, x: int) -> None:
        heapq.heappush(self.heap, -x)

    def remove(self, x: int) -> None:
        self.gone[x] += 1

    def max(self) -> int | None:
        while self.heap and self.gone[-self.heap[0]]:
            self.gone[-self.heap[0]] -= 1
            heapq.heappop(self.heap)
        return -self.heap[0] if self.heap else None
