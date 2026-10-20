"""
Recently Used Order                                                           [easy]

Keep keys in the order they were last used:

    use(key)        mark key as the most recently used (adding it if it's new)
    oldest()        the least recently used key, or None if there are none
    drop_oldest()   remove the least recently used key and return it (None if empty)

Example:
    r = RecentlyUsed()
    r.use("a"); r.use("b"); r.use("a")
    r.oldest()        ->  "b"       "a" was used again after "b"
    r.drop_oldest()   ->  "b"
    r.oldest()        ->  "a"

Aim for:  O(1) for every call. The last test makes 200,000 calls: keeping the keys
          in a list and calling list.remove on every use is O(n) and times out.
Hint:     A dict finds a key's place in O(1), and a doubly linked list moves it to
          the end in O(1). collections.OrderedDict is both at once: move_to_end(key)
          on a use, next(iter(d)) for the oldest, popitem(last=False) to drop it.
"""


class RecentlyUsed:
    def __init__(self):
        raise NotImplementedError

    def use(self, key: str) -> None:
        raise NotImplementedError

    def oldest(self) -> str | None:
        raise NotImplementedError

    def drop_oldest(self) -> str | None:
        raise NotImplementedError


CLASS = "RecentlyUsed"


def _big():
    import random
    from collections import OrderedDict
    rng = random.Random(1403)
    d, ops, res = OrderedDict(), [("RecentlyUsed",)], [None]
    for _ in range(200_000):
        r = rng.random()
        if r < 0.8:
            key = f"k{rng.randrange(60_000)}"
            d[key] = None
            d.move_to_end(key)
            ops.append(("use", key))
            res.append(None)
        elif r < 0.9:
            ops.append(("oldest",))
            res.append(next(iter(d)) if d else None)
        else:
            ops.append(("drop_oldest",))
            res.append(d.popitem(last=False)[0] if d else None)
    return ops, res


TEACHES = ["list.recency"]
USES = []

TESTS = [
    ([("RecentlyUsed",), ("use", "a"), ("use", "b"), ("use", "a"), ("oldest",), ("drop_oldest",), ("oldest",)],
     [None, None, None, None, "b", "b", "a"]),
    ([("RecentlyUsed",), ("oldest",), ("drop_oldest",)], [None, None, None]),
    ([("RecentlyUsed",), ("use", "x"), ("drop_oldest",), ("oldest",), ("use", "x"), ("use", "y"), ("use", "z"),
      ("use", "y"), ("drop_oldest",), ("drop_oldest",), ("oldest",)],
     [None, None, "x", None, None, None, None, None, "x", "z", "y"]),
    _big(),
]
