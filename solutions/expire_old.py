from collections import deque


def expire_old(q: deque, now: int, window: int) -> int:
    while q and q[0] <= now - window:   # oldest first, so stop at the first one still inside
        q.popleft()                     # O(1) on a deque (a list's pop(0) would be O(n))
    return len(q)
