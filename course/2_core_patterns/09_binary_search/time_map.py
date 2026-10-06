"""
Key-value store with history                                                  [build]

Build a store that remembers every value a key has ever had, and can answer
"what was the value at time t?". Config systems and databases do this.

    tm = TimeMap()
    tm.set("theme", "light", 1)
    tm.set("theme", "dark", 4)
    tm.get("theme", 3)    ->  "light"     the latest set at or before time 3
    tm.get("theme", 4)    ->  "dark"
    tm.get("theme", 0)    ->  ""          nothing set yet
    tm.get("font", 5)     ->  ""          unknown key

Rules:
  - For each key, set() is called with strictly increasing timestamps.
  - get(key, t) returns the value from the latest set() with timestamp <= t, or "".
  - history(key, t1, t2) returns the values set in [t1, t2] (both ends included), in time order.

Aim for:  O(log n) per get. Per key, keep a list of timestamps (it's sorted for free,
          because they only increase) and binary search it.
Hint:     bisect.bisect_right(times, t) - 1 is the index of the latest time <= t.
"""
import bisect


class TimeMap:
    def __init__(self):
        raise NotImplementedError

    def set(self, key: str, value: str, t: int) -> None:
        raise NotImplementedError

    def get(self, key: str, t: int) -> str:
        raise NotImplementedError

    def history(self, key: str, t1: int, t2: int) -> list[str]:
        raise NotImplementedError


CLASS = "TimeMap"


def _big():
    import random
    rng = random.Random(15)
    calls, out = [("TimeMap",)], [None]
    store = {}
    t = 0
    for _ in range(40_000):
        t += rng.randint(1, 3)
        key = f"k{rng.randint(0, 9)}"
        calls.append(("set", key, f"v{t}", t))
        out.append(None)
        store.setdefault(key, []).append((t, f"v{t}"))
    for _ in range(40_000):
        key, q = f"k{rng.randint(0, 9)}", rng.randint(0, t)
        calls.append(("get", key, q))
        entries = store.get(key, [])
        best = ""
        lo, hi = 0, len(entries)
        while lo < hi:
            mid = (lo + hi) // 2
            if entries[mid][0] <= q:
                lo = mid + 1
            else:
                hi = mid
        if lo:
            best = entries[lo - 1][1]
        out.append(best)
    return calls, out


_CALLS, _OUT = _big()

TESTS = [
    ([("TimeMap",), ("set", "theme", "light", 1), ("set", "theme", "dark", 4),
      ("get", "theme", 3), ("get", "theme", 4), ("get", "theme", 0), ("get", "font", 5)],
     [None, None, None, "light", "dark", "", ""]),
    ([("TimeMap",), ("set", "a", "x", 10), ("set", "a", "y", 20), ("set", "a", "z", 30),
      ("history", "a", 10, 25), ("history", "a", 31, 40), ("history", "b", 0, 99), ("get", "a", 1000)],
     [None, None, None, None, ["x", "y"], [], [], "z"]),
    ([("TimeMap",), ("set", "k", "1", 5), ("set", "j", "2", 6), ("get", "k", 6), ("get", "j", 5), ("history", "k", 5, 5)],
     [None, None, None, "1", "", ["1"]]),
    (_CALLS, _OUT),
]
