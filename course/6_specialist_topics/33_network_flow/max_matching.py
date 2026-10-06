"""
Maximum Bipartite Matching                                                    [medium]

There are n_left applicants and n_right jobs. pairs lists (applicant, job) for every
job an applicant is qualified for. Each applicant takes at most one job and each job
takes at most one applicant. Return the largest number of applicants that can be hired.

Example:
    max_matching(3, 3, [(0, 0), (0, 1), (1, 0), (2, 1)])  ->  2
        applicants 1 and 2 both need jobs 0 and 1 between them, so one of the three misses out

Aim for:  O(V · E) with augmenting paths (Kuhn's algorithm). The last test has 400 + 400 nodes.
Hint:     owner[job] = the applicant holding it, or -1. try(a, seen): for each job j of a not yet in
          seen, mark it; if owner[j] == -1 or try(owner[j], seen) can move that applicant elsewhere,
          give j to a and return True. Call try once per applicant with a fresh seen set.
"""


def max_matching(n_left: int, n_right: int, pairs: list[tuple[int, int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _flow_matching(nl, nr, pairs):
    from collections import deque
    n = nl + nr + 2
    s, t = n - 2, n - 1
    edges = [(s, a, 1) for a in range(nl)] + [(nl + b, t, 1) for b in range(nr)] + [(a, nl + b, 1) for a, b in pairs]
    cap = [dict() for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] = cap[u].get(v, 0) + c
        cap[v].setdefault(u, 0)
    flow = 0
    while True:
        prev = {s: None}
        q = deque([s])
        while q and t not in prev:
            u = q.popleft()
            for v, c in cap[u].items():
                if c > 0 and v not in prev:
                    prev[v] = u
                    q.append(v)
        if t not in prev:
            return flow
        v = t
        while v != s:
            u = prev[v]
            cap[u][v] -= 1
            cap[v][u] += 1
            v = u
        flow += 1


def _cases():
    import random
    rng = random.Random(3305)
    out = []
    for nl, nr, m in ((1, 1, 1), (4, 3, 6), (6, 6, 10), (12, 9, 25), (40, 40, 90)):
        pairs = list({(rng.randrange(nl), rng.randrange(nr)) for _ in range(m)})
        out.append(((nl, nr, pairs), _flow_matching(nl, nr, pairs)))
    nl = nr = 400
    pairs = list({(rng.randrange(nl), rng.randrange(nr)) for _ in range(1600)})
    out.append(((nl, nr, pairs), _flow_matching(nl, nr, pairs)))
    return out


TESTS = [((3, 3, [(0, 0), (0, 1), (1, 0), (2, 1)]), 2), ((2, 2, []), 0), ((3, 1, [(0, 0), (1, 0), (2, 0)]), 1),
         ((3, 3, [(0, 0), (0, 1), (1, 0), (2, 2), (1, 2)]), 3),
         ((4, 4, [(0, 0), (1, 0), (1, 1), (2, 1), (2, 2), (3, 2), (3, 3)]), 4)] + _cases()
