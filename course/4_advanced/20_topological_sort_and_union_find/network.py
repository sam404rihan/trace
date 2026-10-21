"""
Network of friends                                                            [build]

Build the connectivity tracker behind a social network, using union-find.

    net = Network()
    net.add("ana"); net.add("ben"); net.add("cy"); net.add("dee")
    net.connect("ana", "ben")      ->  True       two groups merged
    net.connect("ben", "ana")      ->  False      already connected
    net.connected("ana", "cy")     ->  False
    net.groups()                   ->  3          {ana, ben} {cy} {dee}
    net.largest()                  ->  2
    net.size_of("ben")             ->  2

Rules:
  - add(name) creates a person in a group of their own (doing nothing if they exist).
  - connect(a, b) adds a and b if needed, merges their groups, and returns True
    if two different groups were merged.
  - connected(a, b) is False if either person is unknown.
  - size_of(name) is 0 for unknown people.

Aim for:  near O(1) per operation: union by size + path compression, plus
          running counters for groups() and largest(). largest() only ever grows,
          because there's no disconnect.
"""


class Network:
    def __init__(self):
        raise NotImplementedError

    def add(self, name: str) -> None:
        raise NotImplementedError

    def connect(self, a: str, b: str) -> bool:
        raise NotImplementedError

    def connected(self, a: str, b: str) -> bool:
        raise NotImplementedError

    def groups(self) -> int:
        raise NotImplementedError

    def largest(self) -> int:
        raise NotImplementedError

    def size_of(self, name: str) -> int:
        raise NotImplementedError


CLASS = "Network"


def _big():
    import random
    rng = random.Random(27)
    n = 60_000
    parent, size = list(range(n)), [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    calls, out = [("Network",)], [None]
    for i in range(n):
        calls.append(("add", f"p{i}"))
        out.append(None)
    groups, largest = n, 1
    for _ in range(120_000):
        a, b = rng.randrange(n), rng.randrange(n)
        if rng.random() < 0.6:
            calls.append(("connect", f"p{a}", f"p{b}"))
            ra, rb = find(a), find(b)
            if ra != rb:
                if size[ra] < size[rb]:
                    ra, rb = rb, ra
                parent[rb] = ra
                size[ra] += size[rb]
                groups -= 1
                largest = max(largest, size[ra])
            out.append(ra != rb)
        else:
            calls.append(("connected", f"p{a}", f"p{b}"))
            out.append(find(a) == find(b))
    calls += [("groups",), ("largest",)]
    out += [groups, largest]
    return calls, out


_CALLS, _OUT = _big()

USES = ["uf.find", "uf.union"]

TESTS = [
    ([("Network",), ("add", "ana"), ("add", "ben"), ("add", "cy"), ("add", "dee"), ("connect", "ana", "ben"),
      ("connect", "ben", "ana"), ("connected", "ana", "cy"), ("groups",), ("largest",), ("size_of", "ben")],
     [None, None, None, None, None, True, False, False, 3, 2, 2]),
    ([("Network",), ("connect", "x", "y"), ("connect", "y", "z"), ("connected", "x", "z"), ("groups",), ("largest",),
      ("connected", "x", "ghost"), ("size_of", "ghost")],
     [None, True, True, True, 1, 3, False, 0]),
    ([("Network",), ("groups",), ("largest",), ("add", "solo"), ("add", "solo"), ("groups",), ("largest",)],
     [None, 0, 0, None, None, 1, 1]),
    ([("Network",), ("connect", "a", "b"), ("connect", "c", "d"), ("connect", "e", "f"), ("connect", "b", "c"),
      ("largest",), ("connect", "f", "a"), ("groups",), ("size_of", "e")],
     [None, True, True, True, True, 4, True, 1, 6]),
    (_CALLS, _OUT),
]
