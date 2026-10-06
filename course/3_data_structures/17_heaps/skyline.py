"""
The Skyline Problem                                                           [hard]

Each building is [left, right, height]: a rectangle on flat ground from x = left
to x = right. Return the skyline's outline as "key points" [x, height]: the
points where the outline's height changes, sorted by x. The last key point
always has height 0. Never list two consecutive points with the same height.

Example:
    skyline([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]])
        ->  [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]
    skyline([[0, 2, 3], [2, 5, 3]])  ->  [[0, 3], [5, 0]]

Aim for:  O(n log n) with a max-heap of the buildings currently overhead.
Hint:     Sweep the distinct x values where something starts or ends. At each x, push every
          building starting there as (-height, right). Then pop from the top while the tallest
          building has already ended (right <= x): lazy deletion. The current height is the
          top of the heap (0 if it's empty). Emit [x, height] whenever it differs from the last.
"""


def skyline(buildings: list[list[int]]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def _brute(buildings):
    xs = sorted({b[0] for b in buildings} | {b[1] for b in buildings})
    out = []
    for x in xs:
        h = max((b[2] for b in buildings if b[0] <= x < b[1]), default=0)
        if not out or out[-1][1] != h:
            out.append([x, h])
    return out


def _fast(buildings):
    import heapq
    events = sorted({b[0] for b in buildings} | {b[1] for b in buildings})
    order = sorted(buildings)
    heap, i, out = [], 0, []
    for x in events:
        while i < len(order) and order[i][0] <= x:
            heapq.heappush(heap, (-order[i][2], order[i][1]))
            i += 1
        while heap and heap[0][1] <= x:
            heapq.heappop(heap)
        h = -heap[0][0] if heap else 0
        if not out or out[-1][1] != h:
            out.append([x, h])
    return out


def _cases():
    import random
    rng = random.Random(218)
    out = []
    for _ in range(10):
        bs = []
        for _ in range(rng.randint(1, 8)):
            left = rng.randint(0, 20)
            bs.append([left, left + rng.randint(1, 8), rng.randint(1, 6)])
        out.append(((bs,), _brute(bs)))
    big = []
    for _ in range(20_000):
        left = rng.randint(0, 10**6)
        big.append([left, left + rng.randint(1, 50_000), rng.randint(1, 10**5)])
    out.append(((big,), _fast(big)))
    return out


TESTS = [
    (([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]],),
     [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]]),
    (([[0, 2, 3], [2, 5, 3]],), [[0, 3], [5, 0]]),
    (([[1, 2, 1], [1, 2, 2], [1, 2, 3]],), [[1, 3], [2, 0]]),
    (([[0, 5, 7]],), [[0, 7], [5, 0]]),
    (([[1, 10, 5], [2, 3, 4]],), [[1, 5], [10, 0]]),
] + _cases()
