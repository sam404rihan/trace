"""
Merge two log files                                                           [build]

Two servers each wrote a log, already sorted by time. Each line looks like
"HH:MM:SS message". Merge them into one log in time order.

Rules:
  - When two lines have the same time, the line from `a` goes first.
  - If a line is exactly the same as the line just written, skip it
    (both servers sometimes log the same event).

Example:
    merge_logs(["09:00:01 boot", "09:00:05 ready"],
               ["09:00:01 boot", "09:00:03 disk ok"])
    ->  ["09:00:01 boot", "09:00:03 disk ok", "09:00:05 ready"]

Aim for:  O(n + m) with two pointers, like the merge step of merge sort.
          Times have a fixed width, so comparing line[:8] as strings works.
Hint:     Walk i through a and j through b. Take from a while a[i][:8] <= b[j][:8].
          Before appending, compare with out[-1] if out isn't empty.
"""


def merge_logs(a: list[str], b: list[str]) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(8)

    def log(n):
        t = sorted(rng.randint(0, 86_399) for _ in range(n))
        return [f"{s // 3600:02}:{s // 60 % 60:02}:{s % 60:02} event{rng.randint(1, 3)}" for s in t]
    a, b = log(80_000), log(80_000)
    out, i, j = [], 0, 0
    while i < len(a) or j < len(b):
        if j == len(b) or (i < len(a) and a[i][:8] <= b[j][:8]):
            line, i = a[i], i + 1
        else:
            line, j = b[j], j + 1
        if not out or out[-1] != line:
            out.append(line)
    return a, b, out


_A, _B, _OUT = _big()

USES = ["pointers.two_sequences"]

TESTS = [
    ((["09:00:01 boot", "09:00:05 ready"], ["09:00:01 boot", "09:00:03 disk ok"]),
     ["09:00:01 boot", "09:00:03 disk ok", "09:00:05 ready"]),
    ((["10:00:00 a1", "10:00:00 a2"], ["10:00:00 b1"]), ["10:00:00 a1", "10:00:00 a2", "10:00:00 b1"]),
    (([], ["00:00:01 x", "00:00:01 x"]), ["00:00:01 x"]),
    ((["23:59:59 last"], []), ["23:59:59 last"]),
    ((["08:00:00 a", "12:00:00 c"], ["09:00:00 b", "13:00:00 d"]), ["08:00:00 a", "09:00:00 b", "12:00:00 c", "13:00:00 d"]),
    ((_A, _B), _OUT),
]
