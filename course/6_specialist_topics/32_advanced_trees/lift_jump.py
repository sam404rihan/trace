"""
Jump with a lifting table                                                    [snippet]

up is a binary lifting table: up[j][v] is the 2^j-th ancestor of node v, or -1 if
it doesn't exist. Return the k-th ancestor of v (k = 0 means v itself), or -1.

Example:
    parent = [-1, 0, 1, 2, 3]            a path 0 - 1 - 2 - 3 - 4
    up = [[-1, 0, 1, 2, 3], [-1, -1, 0, 1, 2], [-1, -1, -1, -1, 0]]
    lift_jump(up, 4, 3)  ->  1           4 → (jump 1) 3 → (jump 2) 1
    lift_jump(up, 2, 5)  ->  -1

Hint:     For each bit j set in k (k >> j & 1), do v = up[j][v], and stop at -1.
          Any order of the bits works. The jumps just add up to k.
"""


def lift_jump(up: list[list[int]], v: int, k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _table(parent):
    n = len(parent)
    up = [parent[:]]
    while (1 << len(up)) <= n:
        prev = up[-1]
        up.append([prev[prev[v]] if prev[v] != -1 else -1 for v in range(n)])
    return up


def _cases():
    import random
    rng = random.Random(3201)
    out = []
    for _ in range(4):
        n = rng.randint(2, 40)
        parent = [-1] + [rng.randrange(v) for v in range(1, n)]
        up = _table(parent)
        for _ in range(4):
            v, k = rng.randrange(n), rng.randint(0, n)
            w = v
            for _ in range(k):
                w = parent[w] if w != -1 else -1
            out.append(((up, v, k), w))
    return out


_PATH = _table([-1, 0, 1, 2, 3])

TEACHES = ["tree.lift_jump"]
USES = ["bits.shift_mask"]

TESTS = [((_PATH, 4, 3), 1), ((_PATH, 2, 5), -1), ((_PATH, 4, 0), 4), ((_PATH, 4, 4), 0), ((_PATH, 0, 1), -1)] + _cases()
