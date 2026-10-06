import heapq
import itertools


class TaskScheduler:
    def __init__(self):
        self.heap = []                      # (-priority, arrival number, name)
        self.counter = itertools.count()    # breaks ties in arrival order
        self.waiting = {}                   # name -> its live heap entry

    def _clean_top(self):
        # Lazy deletion: drop cancelled/replaced entries only when they reach the top.
        while self.heap and self.waiting.get(self.heap[0][2]) is not self.heap[0]:
            heapq.heappop(self.heap)

    def add(self, name: str, priority: int) -> None:
        entry = (-priority, next(self.counter), name)
        self.waiting[name] = entry
        heapq.heappush(self.heap, entry)

    def peek(self) -> str | None:
        self._clean_top()
        return self.heap[0][2] if self.heap else None

    def next(self) -> str | None:
        self._clean_top()
        if not self.heap:
            return None
        _, _, name = heapq.heappop(self.heap)
        del self.waiting[name]
        return name

    def cancel(self, name: str) -> bool:
        return self.waiting.pop(name, None) is not None

    def size(self) -> int:
        return len(self.waiting)
