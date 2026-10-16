from collections import deque


def fewest_steps(start: int, target: int) -> int:
    limit = 2 * max(start, target)
    dist, queue = {start: 0}, deque([start])
    while queue:
        x = queue.popleft()
        if x == target:
            return dist[x]
        for nxt in (x + 1, x - 1, x * 2):   # the neighbours are generated, not given
            if 0 <= nxt <= limit and nxt not in dist:
                dist[nxt] = dist[x] + 1
                queue.append(nxt)
    return -1
