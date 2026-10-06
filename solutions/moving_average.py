from collections import deque


def moving_average(stream: list[int], k: int) -> list[float]:
    window, total, out = deque(), 0, []
    for x in stream:
        window.append(x)                # one in...
        total += x
        if len(window) > k:
            total -= window.popleft()   # ...one out
        out.append(round(total / len(window), 2))
    return out
