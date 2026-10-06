from collections import Counter, deque


def first_unique_char(s: str) -> int:
    # Count everything, then take the first character seen exactly once. O(n).
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1


def first_unique_char_stream(s: str) -> int:
    # Queue version: works even if characters arrive one at a time (a stream).
    counts, queue = Counter(), deque()
    for i, ch in enumerate(s):
        counts[ch] += 1
        queue.append((ch, i))
        while queue and counts[queue[0][0]] > 1:   # front repeated: it can never be the answer
            queue.popleft()
    return queue[0][1] if queue else -1
