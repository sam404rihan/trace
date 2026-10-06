"""
Route planner                                                                 [build]

Roads connect cities in both directions and take some minutes to drive.
Return (minutes, route): the fastest total time from start to end, and the
list of cities along one fastest route (start and end included). If end
can't be reached, return (-1, []).

    route_planner([("A", "B", 5), ("B", "C", 5), ("A", "C", 15)], "A", "C")
    ->  (10, ["A", "B", "C"])

Rules:
  - Any fastest route is accepted. The tests check that the route really
    uses existing roads and that its total matches the best time.
  - start == end gives (0, [start]).
  - Several roads can connect the same two cities. The fastest one counts.

Hint:     Dijkstra on an adjacency dict, plus a `prev` dict: whenever dist[v] improves
          through u, set prev[v] = u. At the end, walk prev back from `end` and reverse.
"""


def route_planner(roads: list[tuple[str, str, int]], start: str, end: str) -> tuple[int, list[str]]:
    raise NotImplementedError  # replace this line with your solution


def _best(roads, start, end):
    import heapq
    adj = {}
    for a, b, w in roads:
        adj.setdefault(a, []).append((b, w))
        adj.setdefault(b, []).append((a, w))
    dist = {start: 0}
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == end:
            return d
        if d > dist.get(u, float("inf")):
            continue
        for v, w in adj.get(u, []):
            if d + w < dist.get(v, float("inf")):
                dist[v] = d + w
                heapq.heappush(pq, (d + w, v))
    return -1


def CHECK(got, expected, args):
    roads, start, end = args
    best = _best(roads, start, end)
    if not (isinstance(got, (tuple, list)) and len(got) == 2):
        return False
    minutes, route = got
    if best == -1:
        return minutes == -1 and list(route) == []
    if minutes != best or not route or route[0] != start or route[-1] != end:
        return False
    fastest = {}
    for a, b, w in roads:
        for key in ((a, b), (b, a)):
            fastest[key] = min(fastest.get(key, float("inf")), w)
    total = 0
    for a, b in zip(route, route[1:]):
        if (a, b) not in fastest:
            return False
        total += fastest[(a, b)]
    return total == best


def _big():
    import random
    rng = random.Random(29)
    cities = [f"C{i}" for i in range(4000)]
    roads = [(cities[i], cities[rng.randrange(i)], rng.randint(5, 90)) for i in range(1, len(cities))]
    roads += [(rng.choice(cities), rng.choice(cities), rng.randint(5, 90)) for _ in range(16_000)]
    return roads


_BIG = _big()
_CASES = [
    ([("A", "B", 5), ("B", "C", 5), ("A", "C", 15)], "A", "C"),
    ([("Oslo", "Bergen", 400), ("Oslo", "Trondheim", 450), ("Bergen", "Trondheim", 600)], "Bergen", "Trondheim"),
    ([("A", "B", 1)], "A", "Z"),
    ([("A", "B", 1)], "B", "B"),
    ([("A", "B", 9), ("A", "B", 2), ("B", "C", 2), ("A", "C", 7)], "A", "C"),
    ([("x", "y", 3), ("y", "z", 3), ("z", "w", 3), ("x", "w", 10), ("y", "w", 5)], "x", "w"),
    (_BIG, "C0", "C3999"),
]


def _describe(roads, start, end):
    best = _best(roads, start, end)
    return (-1, []) if best == -1 else f"({best}, any fastest route)"


TESTS = [(case, _describe(*case)) for case in _CASES]
