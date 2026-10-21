"""
Parallel Courses III                                                          [hard]

There are n courses, numbered 0..n-1. Course i takes time[i] months.
relations holds pairs [a, b]: course a must be finished before b starts.
You can take any number of courses at the same time. Return the fewest months
to finish them all. The prerequisites never form a cycle.

Example:
    parallel_courses_iii(3, [[0, 2], [1, 2]], [3, 2, 5])   ->  8
        0 and 1 run together; 2 starts at month 3 and ends at month 8.
    parallel_courses_iii(5, [[0, 4], [1, 4], [2, 4], [3, 4], [1, 2]], [1, 2, 3, 4, 5])  ->  10

Aim for:  O(n + relations) with a topological order.
Hint:     finish[i] = time[i] + max(finish of i's prerequisites, or 0). Process courses in
          topological order (Kahn's algorithm: start with the courses that have no
          prerequisites) so every prerequisite's finish is known before it's needed.
          The answer is the max finish.
"""


def parallel_courses_iii(n: int, relations: list[list[int]], time: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _ref(n, relations, time):
    from functools import cache
    pre = [[] for _ in range(n)]
    for a, b in relations:
        pre[b].append(a)

    @cache
    def finish(i):
        return time[i] + max((finish(p) for p in pre[i]), default=0)
    return max(finish(i) for i in range(n))


def _kahn(n, relations, time):
    from collections import deque
    nxt, indeg = [[] for _ in range(n)], [0] * n
    for a, b in relations:
        nxt[a].append(b)
        indeg[b] += 1
    start = [0] * n
    q = deque(i for i in range(n) if indeg[i] == 0)
    best = 0
    while q:
        i = q.popleft()
        done = start[i] + time[i]
        best = max(best, done)
        for j in nxt[i]:
            start[j] = max(start[j], done)
            indeg[j] -= 1
            if not indeg[j]:
                q.append(j)
    return best


def _cases():
    import random
    rng = random.Random(2050)
    out = []
    for _ in range(10):
        n = rng.randint(2, 10)
        order = rng.sample(range(n), n)         # edges only go forward in this order: no cycles
        pairs = set()
        for _ in range(rng.randint(0, 15)):
            i, j = sorted(rng.sample(range(n), 2))
            pairs.add((order[i], order[j]))
        rel = [list(p) for p in sorted(pairs)]
        time = [rng.randint(1, 9) for _ in range(n)]
        out.append(((n, rel, time), _ref(n, rel, time)))
    # big: a long dependency chain (deep recursion would overflow) plus random extra edges
    n = 20_000
    order = rng.sample(range(n), n)
    rel = [[order[i], order[i + 1]] for i in range(n - 1)]
    for _ in range(20_000):
        i, j = sorted(rng.sample(range(n), 2))
        rel.append([order[i], order[j]])
    time = [rng.randint(1, 10) for _ in range(n)]
    out.append(((n, rel, time), _kahn(n, rel, time)))
    return out


USES = ["graph.adjacency", "graph.topo_kahn"]

TESTS = [
    ((3, [[0, 2], [1, 2]], [3, 2, 5]), 8),
    ((5, [[0, 4], [1, 4], [2, 4], [3, 4], [1, 2]], [1, 2, 3, 4, 5]), 10),
    ((1, [], [7]), 7),
    ((3, [], [4, 9, 2]), 9),
    ((3, [[0, 1], [1, 2]], [1, 1, 1]), 3),
] + _cases()
