"""
Bottleneck of a path                                                         [snippet]

cap[u][v] is how much more flow the edge u -> v can carry (a dict of dicts). path is
a list of nodes from the source to the sink. Return the most you can push along the
whole path: the smallest spare capacity on any of its edges.

Example:
    cap = {"s": {"a": 7}, "a": {"b": 3}, "b": {"t": 9}}
    bottleneck(cap, ["s", "a", "b", "t"])  ->  3

Hint:     min(cap[u][v] for u, v in zip(path, path[1:])), or itertools.pairwise(path).
          Every augmenting-path algorithm pushes exactly this much, then updates each edge.
"""


def bottleneck(cap: dict, path: list) -> int:
    raise NotImplementedError  # replace this line with your solution


def _cases():
    import random
    rng = random.Random(3301)
    out = []
    for _ in range(6):
        k = rng.randint(2, 9)
        path = list(range(k))
        cap = {}
        for u, v in zip(path, path[1:]):
            cap.setdefault(u, {})[v] = rng.randint(1, 100)
            for _ in range(2):
                cap[u][rng.randint(20, 30)] = rng.randint(1, 5)        # other edges, not on the path
        out.append(((cap, path), min(cap[u][v] for u, v in zip(path, path[1:]))))
    return out


TESTS = [(({"s": {"a": 7}, "a": {"b": 3}, "b": {"t": 9}}, ["s", "a", "b", "t"]), 3),
         (({"s": {"t": 4, "a": 1}}, ["s", "t"]), 4),
         (({0: {1: 5, 2: 1}, 1: {2: 8, 0: 0}, 2: {3: 6}}, [0, 1, 2, 3]), 5)] + _cases()
