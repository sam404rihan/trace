"""
Moving average of a stream                                                   [guided]

For each position i, return the average of the last k values seen so far
(fewer at the start, when fewer than k exist), rounded to 2 decimals.

Example:
    moving_average([10, 20, 30, 40], 3)  ->  [10.0, 15.0, 20.0, 30.0]
"""


def moving_average(stream: list[int], k: int) -> list[float]:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    from collections import deque
    rng = random.Random(16)
    stream = [rng.randint(0, 1000) for _ in range(200_000)]
    k, q, total, out = 2000, deque(), 0, []
    for x in stream:
        q.append(x)
        total += x
        if len(q) > k:
            total -= q.popleft()
        out.append(round(total / len(q), 2))
    return stream, k, out


_STREAM, _K, _OUT = _big()

STEPS = [
    {
        "title": "Make it work",
        "text": "For each i, average the slice stream[max(0, i - k + 1) : i + 1].",
        "hint": "round(sum(window) / len(window), 2)",
        "tests": [
            (([10, 20, 30, 40], 3), [10.0, 15.0, 20.0, 30.0]),
            (([1, 2, 3, 4, 5], 2), [1.0, 1.5, 2.5, 3.5, 4.5]),
        ],
    },
    {
        "title": "Edges",
        "text": "k = 1 just repeats the stream. A k longer than the stream averages everything so far. An empty stream gives [].",
        "hint": "These should work already if your window logic is right.",
        "tests": [
            (([4, 8], 1), [4.0, 8.0]),
            (([1, 2, 4], 10), [1.0, 1.5, 2.33]),
            (([], 3), []),
        ],
    },
    {
        "title": "Keep a running total",
        "text": "200,000 values with k = 2,000: re-summing each window is 400 million additions. Keep a deque of the "
                "window and a running total. Add the newcomer, and if the window is too long, subtract the one that falls out.",
        "hint": "q.append(x); total += x; if len(q) > k: total -= q.popleft(). O(1) per value.",
        "tests": [
            (([5, 5, 5, 5], 2), [5.0, 5.0, 5.0, 5.0]),
            ((_STREAM, _K), _OUT),
        ],
    },
]
