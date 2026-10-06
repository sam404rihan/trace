from collections import deque


class TicketQueue:
    def __init__(self):
        self.q = deque()
        self.waiting = set()        # O(1) "is this person already in line?"

    def join(self, name: str) -> int:
        if name not in self.waiting:
            self.q.append(name)
            self.waiting.add(name)
            return len(self.q)      # just joined at the back: O(1)
        return self.position(name)

    def vip(self, name: str) -> int:
        if name not in self.waiting:
            self.q.appendleft(name)
            self.waiting.add(name)
            return 1
        return self.position(name)

    def serve(self) -> str | None:
        if not self.q:
            return None
        name = self.q.popleft()
        self.waiting.discard(name)
        return name

    def position(self, name: str) -> int:
        if name not in self.waiting:
            return -1
        return self.q.index(name) + 1

    def leave(self, name: str) -> bool:
        if name not in self.waiting:
            return False
        self.q.remove(name)
        self.waiting.discard(name)
        return True

    def size(self) -> int:
        return len(self.q)
