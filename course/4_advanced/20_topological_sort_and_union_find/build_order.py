"""
Build order                                                                  [guided]

There are n packages, numbered 0 to n − 1. Each pair (a, b) in `deps` means
"a must be built before b". Return any order that respects every pair, as a
list of all n packages. If no such order exists (there's a cycle), return [].

Example:
    build_order(4, [(0, 1), (1, 2), (0, 3)])  ->  [0, 1, 3, 2]   (or [0, 3, 1, 2], or [0, 1, 2, 3])

Any valid order is accepted: the tests check your list, not a fixed answer.
"""


def build_order(n: int, deps: list[tuple[int, int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _valid(order, n, deps):
    if sorted(order) != list(range(n)):
        return False
    pos = {x: i for i, x in enumerate(order)}
    return all(pos[a] < pos[b] for a, b in deps)


def _has_order(n, deps):
    indeg = [0] * n
    out = [[] for _ in range(n)]
    for a, b in deps:
        out[a].append(b)
        indeg[b] += 1
    ready = [x for x in range(n) if indeg[x] == 0]
    done = 0
    while ready:
        x = ready.pop()
        done += 1
        for y in out[x]:
            indeg[y] -= 1
            if indeg[y] == 0:
                ready.append(y)
    return done == n


def CHECK(got, expected, args):
    n, deps = args
    if not _has_order(n, deps):
        return got == []
    return isinstance(got, list) and _valid(got, n, deps)


def _big():
    import random
    rng = random.Random(26)
    n = 30_000
    perm = list(range(n))
    rng.shuffle(perm)
    deps = []
    for _ in range(90_000):
        i, j = sorted(rng.sample(range(n), 2))
        deps.append((perm[i], perm[j]))
    return n, deps


_BN, _BDEPS = _big()

TEACHES = ["graph.topo_kahn"]
USES = ["graph.adjacency"]

STEPS = [
    {
        "title": "Take what's ready",
        "text": "Count each package's prerequisites (its in-degree). Start with the packages that have none. Each time "
                "you build one, decrease the count of everything that depended on it, and any package whose count hits 0 becomes ready.",
        "hint": "Kahn's algorithm: indeg list + adjacency list + a queue of ready packages. Append each one you pop to the answer.",
        "tests": [
            ((3, [(0, 1), (1, 2)]), "a valid order"),
            ((4, [(0, 1), (1, 2), (0, 3)]), "a valid order"),
            ((5, [(4, 0), (3, 0), (0, 1), (2, 1)]), "a valid order"),
        ],
    },
    {
        "title": "Disconnected and unconstrained",
        "text": "Packages with no dependencies at all still belong in the order, and the graph can be in several pieces.",
        "hint": "Start the queue with EVERY package whose in-degree is 0, not just one.",
        "tests": [
            ((3, []), "a valid order"),
            ((6, [(0, 1), (2, 3), (4, 5)]), "a valid order"),
            ((1, []), "a valid order"),
        ],
    },
    {
        "title": "Detect cycles",
        "text": "If packages wait on each other in a loop, Kahn's algorithm runs out of ready packages before it has built "
                "all n. When your order is shorter than n, return []. The last test is a big valid graph: 30,000 packages and 90,000 rules.",
        "hint": "return order if len(order) == n else []",
        "tests": [
            ((2, [(0, 1), (1, 0)]), []),
            ((4, [(0, 1), (1, 2), (2, 3), (3, 1)]), []),
            ((3, [(0, 0)]), []),
            ((_BN, _BDEPS), "a valid order"),
        ],
    },
]
