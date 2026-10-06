from collections import deque


def build_order(n: int, deps: list[tuple[int, int]]) -> list[int]:
    indeg = [0] * n
    after = [[] for _ in range(n)]          # a -> everything that waits on a
    for a, b in deps:
        after[a].append(b)
        indeg[b] += 1
    ready = deque(x for x in range(n) if indeg[x] == 0)
    order = []
    while ready:
        x = ready.popleft()
        order.append(x)
        for y in after[x]:
            indeg[y] -= 1
            if indeg[y] == 0:               # its last prerequisite just got built
                ready.append(y)
    return order if len(order) == n else []  # leftovers are stuck in a cycle
