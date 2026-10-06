"""
Task Scheduler (cooldown)                                                     [medium]

A CPU runs tasks given as letters, one per time unit. Between two runs of the
SAME letter there must be at least n other units (other tasks, or idle).
Return the fewest units needed to run them all.

Example:
    least_interval(["A","A","A","B","B","B"], 2)  ->  8      A B idle A B idle A B
    least_interval(["A","A","A","B","B","B"], 0)  ->  6

Aim for:  O(len(tasks)).
Hint:     The most frequent letter sets the frame: (max_count - 1) blocks of length n + 1, plus
          one final unit for every letter that ties for max_count. If there are more tasks than
          that frame has room for, there are no idle slots, and the answer is just len(tasks).
          (A max-heap simulation also works, and generalises better.)
"""


def least_interval(tasks: list[str], n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _sim(tasks, n):
    counts = {}
    for t in tasks:
        counts[t] = counts.get(t, 0) + 1
    ready_at = {t: 0 for t in counts}
    time = 0
    while counts:
        choices = [t for t in counts if ready_at[t] <= time]
        if choices:
            t = max(choices, key=lambda x: counts[x])
            counts[t] -= 1
            ready_at[t] = time + n + 1
            if counts[t] == 0:
                del counts[t]
        time += 1
    return time


def _cases():
    import random
    rng = random.Random(72)
    out = []
    for _ in range(10):
        tasks = [rng.choice("ABCDE") for _ in range(rng.randint(1, 20))]
        n = rng.randint(0, 4)
        out.append(((tasks, n), _sim(tasks, n)))
    return out


TESTS = [((["A", "A", "A", "B", "B", "B"], 2), 8), ((["A", "A", "A", "B", "B", "B"], 0), 6),
         ((["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2), 16), ((["A"], 5), 1)] + _cases()
