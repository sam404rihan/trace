"""
LFU Cache                                                                     [hard]

A cache that holds at most `capacity` keys and, when full, evicts the LEAST
FREQUENTLY used key. Ties go to the least recently used among them.

    get(key)          the value, or -1 if missing. Counts as a use of key.
    put(key, value)   insert or update. Counts as a use of key. If inserting a
                      NEW key into a full cache, first evict as described.

A key's use count starts at 1 when it's inserted. Evicting a key forgets its count.

Example:
    c = LFUCache(2)
    c.put(1, 1); c.put(2, 2)
    c.get(1)        ->  1       key 1 used twice, key 2 once
    c.put(3, 3)                 evicts 2
    c.get(2)        ->  -1
    c.get(3)        ->  3       keys 1 and 3 both used twice now
    c.put(4, 4)                 tie: evicts 1, the least recently used
    c.get(1)        ->  -1

Aim for:  O(1) per call.
Hint:     Keep key -> (value, count), and for each count an OrderedDict of its keys in
          recency order (a doubly linked list does the same job). Track the smallest count.
          On a use, move the key from bucket count to bucket count + 1 (if bucket min_count
          becomes empty, min_count + 1 is the new minimum). Evict the first key of the
          min_count bucket. A new key resets min_count to 1.
"""


class LFUCache:
    def __init__(self, capacity: int):
        raise NotImplementedError

    def get(self, key: int) -> int:
        raise NotImplementedError

    def put(self, key: int, value: int) -> None:
        raise NotImplementedError


CLASS = "LFUCache"


def _naive(ops):
    """Evict by scanning for the smallest (count, last use). O(capacity) per eviction."""
    cap = ops[0][1]
    data, out, clock = {}, [None], 0          # key -> [value, count, last_use]
    for op in ops[1:]:
        clock += 1
        if op[0] == "get":
            if op[1] in data:
                data[op[1]][1] += 1
                data[op[1]][2] = clock
                out.append(data[op[1]][0])
            else:
                out.append(-1)
        else:
            _, key, value = op
            if key in data:
                data[key][0] = value
                data[key][1] += 1
                data[key][2] = clock
            elif cap > 0:
                if len(data) >= cap:
                    victim = min(data, key=lambda k: (data[k][1], data[k][2]))
                    del data[victim]
                data[key] = [value, 1, clock]
            out.append(None)
    return out


def _fast(ops):
    from collections import OrderedDict, defaultdict
    cap = ops[0][1]
    val, cnt, buckets, low, out = {}, {}, defaultdict(OrderedDict), 0, [None]

    def touch(k):
        nonlocal low
        c = cnt[k]
        del buckets[c][k]
        if not buckets[c] and low == c:
            low += 1
        cnt[k] = c + 1
        buckets[c + 1][k] = None

    for op in ops[1:]:
        if op[0] == "get":
            if op[1] in val:
                touch(op[1])
                out.append(val[op[1]])
            else:
                out.append(-1)
        else:
            _, k, v = op
            if k in val:
                val[k] = v
                touch(k)
            elif cap > 0:
                if len(val) >= cap:
                    victim, _ = buckets[low].popitem(last=False)
                    del val[victim], cnt[victim]
                val[k], cnt[k], low = v, 1, 1
                buckets[1][k] = None
            out.append(None)
    return out


def _random_ops(rng, cap, n, keys):
    ops = [("LFUCache", cap)]
    for _ in range(n):
        k = rng.randint(0, keys)
        ops.append(("get", k) if rng.random() < 0.5 else ("put", k, rng.randint(0, 99)))
    return ops


def _cases():
    import random
    rng = random.Random(460)
    out = []
    for _ in range(6):
        ops = _random_ops(rng, rng.randint(1, 4), 40, 7)
        out.append((ops, _naive(ops)))
    ops = _random_ops(rng, 4000, 60_000, 10_000)
    out.append((ops, _fast(ops)))
    return out


TESTS = [
    ([("LFUCache", 2), ("put", 1, 1), ("put", 2, 2), ("get", 1), ("put", 3, 3), ("get", 2), ("get", 3),
      ("put", 4, 4), ("get", 1), ("get", 3), ("get", 4)],
     [None, None, None, 1, None, -1, 3, None, -1, 3, 4]),
    ([("LFUCache", 0), ("put", 0, 0), ("get", 0)], [None, None, -1]),
    ([("LFUCache", 1), ("put", 2, 1), ("get", 2), ("put", 3, 2), ("get", 2), ("get", 3)],
     [None, None, 1, None, -1, 2]),
    ([("LFUCache", 2), ("put", 1, 1), ("put", 1, 5), ("put", 2, 2), ("put", 3, 3), ("get", 1), ("get", 2)],
     [None, None, None, None, None, 5, -1]),
] + _cases()
