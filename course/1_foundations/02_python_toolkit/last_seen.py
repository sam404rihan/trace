"""
Last seen index                                                             [snippet]

Return a dict that maps each value in `items` to the index where it appears
for the last time.

Example:
    last_seen(["a", "b", "a"])  ->  {"a": 2, "b": 1}

Aim for:  one pass, 2–3 lines.
Hint:     Loop with `for i, x in enumerate(items)` and just overwrite d[x] = i.
          Later indexes win automatically.
"""


def last_seen(items: list) -> dict:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((["a", "b", "a"],), {"a": 2, "b": 1}),
    (([5, 5, 5],), {5: 2}),
    (([1, 2, 3],), {1: 0, 2: 1, 3: 2}),
    (([],), {}),
    ((["x", "y", "x", "z", "y"],), {"x": 2, "y": 4, "z": 3}),
]
