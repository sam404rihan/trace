from collections import deque


class RateLimiter:
    def __init__(self, limit: int, window: int):
        self.limit = limit
        self.window = window
        self.allowed = deque()          # timestamps of allowed requests, oldest at the front

    def _expire(self, t):
        # Times only go forward, so expired requests are always at the front.
        while self.allowed and self.allowed[0] <= t - self.window:
            self.allowed.popleft()

    def allow(self, t: int) -> bool:
        self._expire(t)
        if len(self.allowed) < self.limit:
            self.allowed.append(t)
            return True
        return False

    def count(self, t: int) -> int:
        self._expire(t)
        return len(self.allowed)
