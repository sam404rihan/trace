"""
Bus Routes                                                                    [hard]

routes[i] lists the stops bus i visits, over and over, in a loop. You start at
stop `source` (not on a bus yet) and want to reach stop `target`. Return the
fewest buses you must take, or -1 if it's impossible. 0 if you're already there.

Example:
    bus_routes([[1, 2, 7], [3, 6, 7]], 1, 6)                         ->  2
        Bus 0 to stop 7, then bus 1 to stop 6.
    bus_routes([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12)  ->  -1

Aim for:  O(total stops on all routes). BFS where each step boards a whole bus.
Hint:     Map each stop to the buses that visit it. BFS over buses (or stops), counting buses
          taken. When you board a bus, every stop on it is reachable with the same count; mark
          the bus as used so you never scan its stops again. That last part is what keeps it
          linear: without it, big routes get rescanned over and over.
"""


def bus_routes(routes: list[list[int]], source: int, target: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(routes, source, target):
    from collections import deque
    if source == target:
        return 0
    at = {}
    for b, r in enumerate(routes):
        for s in r:
            at.setdefault(s, []).append(b)
    used, seen = set(), {source}
    q = deque([(source, 0)])
    while q:
        stop, n = q.popleft()
        for b in at.get(stop, []):
            if b in used:
                continue
            used.add(b)
            for s in routes[b]:
                if s == target:
                    return n + 1
                if s not in seen:
                    seen.add(s)
                    q.append((s, n + 1))
    return -1


def _cases():
    import random
    rng = random.Random(815)
    out = []
    for _ in range(10):
        routes = [sorted(set(rng.sample(range(12), rng.randint(1, 4)))) for _ in range(rng.randint(1, 6))]
        s, t = rng.randrange(12), rng.randrange(12)
        out.append(((routes, s, t), _ref(routes, s, t)))
    # big: a chain of buses that all share one huge hub route
    routes = [list(range(0, 100_000))] + [[100_000 + i, 100_000 + i + 1] for i in range(2000)] \
        + [[i * 50, 100_000 + (i % 2000)] for i in range(2000)]
    out.append(((routes, 100_000, 102_000), _ref(routes, 100_000, 102_000)))
    return out


USES = ["graph.adjacency", "bfs.shortest"]

TESTS = [
    (([[1, 2, 7], [3, 6, 7]], 1, 6), 2),
    (([[7, 12], [4, 5, 15], [6], [15, 19], [9, 12, 13]], 15, 12), -1),
    (([[1, 2, 3]], 2, 2), 0),
    (([[1, 2, 3]], 1, 3), 1),
    (([[1, 7], [3, 5]], 5, 5), 0),
    (([[1, 2], [3, 4]], 1, 4), -1),
] + _cases()
