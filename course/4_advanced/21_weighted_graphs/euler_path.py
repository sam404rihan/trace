"""
One Stroke Through Every Road                                                 [easy]

Places are numbered 0 to n - 1, and each road [a, b] is ONE-WAY from a to b.
There is a route that starts at place 0 and drives along every road exactly
once (it may pass through a place many times). Return one such route as the
list of places in order. Any valid route is accepted.

Example:
    euler_path(3, [[0, 1], [1, 2], [2, 1], [1, 0], [0, 2]])  ->  [0, 1, 2, 1, 0, 2]

Aim for:  O(n + roads). Walking until you're stuck isn't enough: you can get stuck
          with roads still unused (see the tests with loops off the main path).
Hint:     Hierholzer's algorithm. Keep a stack, starting with [0]. Look at the place on top:
          if it still has an unused road, take it and push where it leads. If it has none,
          pop it onto the route. The route comes out backwards, so reverse it at the end.
          Each loop you got stuck before is spliced in where it belongs.
"""


def euler_path(n: int, roads: list[list[int]]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def CHECK(got, expected, args):
    """Any route that starts at 0 and uses every road exactly once."""
    n, roads = args
    if not isinstance(got, list) or not got or got[0] != 0:
        return False
    from collections import Counter
    return Counter(zip(got, got[1:])) == Counter(map(tuple, roads))


def _fast(n, roads):
    out = [[] for _ in range(n)]
    for a, b in roads:
        out[a].append(b)
    route, stack = [], [0]
    while stack:
        if out[stack[-1]]:
            stack.append(out[stack[-1]].pop())
        else:
            route.append(stack.pop())
    return route[::-1]


def _big():
    import random
    rng = random.Random(2102)
    n = 2_000
    walk = [0] + [rng.randrange(n) for _ in range(60_000)]      # one long walk is always one stroke
    roads = [[a, b] for a, b in zip(walk, walk[1:])]
    rng.shuffle(roads)
    return (n, roads), _fast(n, roads)


TEACHES = ["graph.euler"]
USES = ["graph.adjacency"]

TESTS = [
    ((3, [[0, 1], [1, 2], [2, 1], [1, 0], [0, 2]]), [0, 1, 2, 1, 0, 2]),
    ((2, [[0, 1]]), [0, 1]),
    ((1, []), [0]),
    ((4, [[0, 1], [1, 0], [0, 2], [2, 3]]), [0, 1, 0, 2, 3]),
    ((5, [[0, 1], [1, 2], [2, 0], [0, 3], [3, 4], [4, 0]]), [0, 1, 2, 0, 3, 4, 0]),
    ((4, [[0, 1], [1, 3], [1, 2], [2, 1]]), [0, 1, 2, 1, 3]),
    _big(),
]
