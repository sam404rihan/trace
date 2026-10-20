"""
LRU cache                                                                     [build]

Build a fixed-size cache that throws out the Least Recently Used entry when
it's full. Browsers, CPUs and databases all have one.

    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.get("a")      ->  1        "a" is now the most recently used
    cache.put("c", 3)               full: evicts "b", the least recently used
    cache.get("b")      ->  -1
    cache.keys()        ->  ["a", "c"]     least recently used first

Rules:
  - get(key) returns the value (and marks the key as used), or -1 if it's missing.
  - put(key, value) inserts or updates, marks the key as used, and evicts the
    least recently used key if that takes the cache over capacity.
  - keys() lists the current keys from least to most recently used. It doesn't count as a use.

Aim for:  O(1) get and put. A dict gives O(1) lookup. A doubly linked list
          (or collections.OrderedDict, which is one inside) gives O(1)
          "move to the most-recent end" and "drop the oldest".
Hint:     OrderedDict: move_to_end(key) on every use, popitem(last=False) to evict.
          Then try writing the linked list yourself.
"""


class LRUCache:
    def __init__(self, capacity: int):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def put(self, key, value) -> None:
        raise NotImplementedError

    def keys(self) -> list:
        raise NotImplementedError


CLASS = "LRUCache"


def _big():
    import random
    from collections import OrderedDict
    rng = random.Random(17)
    cap = 5000
    calls, out, od = [("LRUCache", cap)], [None], OrderedDict()
    for _ in range(150_000):
        key = rng.randint(0, 12_000)
        if rng.random() < 0.5:
            calls.append(("get", key))
            if key in od:
                od.move_to_end(key)
                out.append(od[key])
            else:
                out.append(-1)
        else:
            value = rng.randint(0, 999)
            calls.append(("put", key, value))
            od[key] = value
            od.move_to_end(key)
            if len(od) > cap:
                od.popitem(last=False)
            out.append(None)
    return calls, out


_CALLS, _OUT = _big()

USES = ["list.recency"]

TESTS = [
    ([("LRUCache", 2), ("put", "a", 1), ("put", "b", 2), ("get", "a"), ("put", "c", 3), ("get", "b"), ("keys",)],
     [None, None, None, 1, None, -1, ["a", "c"]]),
    ([("LRUCache", 2), ("put", 1, 1), ("put", 2, 2), ("put", 1, 10), ("put", 3, 3), ("get", 2), ("get", 1), ("keys",)],
     [None, None, None, None, None, -1, 10, [3, 1]]),
    ([("LRUCache", 1), ("put", "x", 1), ("put", "y", 2), ("get", "x"), ("get", "y"), ("keys",)],
     [None, None, None, -1, 2, ["y"]]),
    ([("LRUCache", 3), ("get", "nothing"), ("put", "a", 1), ("keys",), ("put", "b", 2), ("keys",), ("get", "a"), ("keys",)],
     [None, -1, None, ["a"], None, ["a", "b"], 1, ["b", "a"]]),
    (_CALLS, _OUT),
]
