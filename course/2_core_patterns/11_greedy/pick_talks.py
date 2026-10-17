"""
Plan your conference day                                                      [build]

Talks are (name, start, end). You want to attend as many complete talks as
possible, one at a time. A talk can start exactly when the previous one ends.

Return the names of the talks you attend, in time order, chosen greedily:
  - Always pick the talk that ENDS earliest among those that start at or after
    the end of your last talk.
  - If several end at the same time, pick the alphabetically first name.

Example:
    pick_talks([("Keynote", 9, 12), ("Rust", 9, 10), ("Go", 10, 11), ("SQL", 11, 13)])
    ->  ["Rust", "Go", "SQL"]

Why greedy works here: the talk that ends first leaves the most time for the
rest. Any schedule can swap its first talk for that one without losing a talk.

Hint:     Sort by (end, name). Walk through once, keeping the end time of your last talk.
"""


def pick_talks(talks: list[tuple[str, int, int]]) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(13)
    talks = []
    for i in range(60_000):
        s = rng.randint(0, 500_000)
        talks.append((f"t{i:05}", s, s + rng.randint(1, 400)))
    last, out = -1, []
    for name, s, e in sorted(talks, key=lambda t: (t[2], t[0])):
        if s >= last:
            out.append(name)
            last = e
    return talks, out


_TALKS, _PICKS = _big()

USES = ["intervals.earliest_end"]

TESTS = [
    (([("Keynote", 9, 12), ("Rust", 9, 10), ("Go", 10, 11), ("SQL", 11, 13)],), ["Rust", "Go", "SQL"]),
    (([("B", 1, 3), ("A", 2, 3), ("C", 3, 4)],), ["A", "C"]),
    (([("Long", 0, 100), ("Short", 50, 51)],), ["Short"]),
    (([],), []),
    (([("x", 1, 2), ("y", 1, 2), ("z", 2, 3), ("w", 0, 1)],), ["w", "x", "z"]),
    ((_TALKS,), _PICKS),
]
