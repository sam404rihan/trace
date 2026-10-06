"""
Top visitors in a server log                                                  [build]

Each log line looks like:

    "203.0.113.9 GET /index.html 200"

i.e. `ip method path status`, separated by spaces. Return the k IPs with the
most requests as (ip, count) pairs, most requests first. Break ties by the IP
string in alphabetical order.

Ignore malformed lines: anything without exactly 4 space-separated parts.
If there are fewer than k distinct IPs, return them all.

Example:
    top_visitors(["1.1.1.1 GET / 200", "2.2.2.2 GET / 404", "1.1.1.1 POST /a 200"], 1)
    ->  [("1.1.1.1", 2)]

Aim for:  the last test has 200,000 lines from 20,000 different IPs, so you need
          about O(n log n) or better.
Hint:     Count with a dict (or Counter), then sort the distinct IPs by (-count, ip)
          and slice the first k. heapq.nsmallest(k, ...) also works.
"""


def top_visitors(log_lines: list[str], k: int) -> list[tuple[str, int]]:
    raise NotImplementedError  # replace this line with your solution


def _big():
    import random
    rng = random.Random(11)
    ips = [f"10.{rng.randint(0, 255)}.{rng.randint(0, 255)}.{rng.randint(0, 255)}" for _ in range(20_000)]
    weights = [rng.random() ** 3 for _ in ips]
    lines = []
    for ip in rng.choices(ips, weights, k=200_000):
        lines.append(f"{ip} GET /p/{rng.randint(1, 99)} {rng.choice((200, 200, 404, 500))}")
    counts = {}
    for line in lines:
        ip = line.split()[0]
        counts[ip] = counts.get(ip, 0) + 1
    return lines, sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:10]


_LINES, _TOP = _big()

TESTS = [
    ((["1.1.1.1 GET / 200", "2.2.2.2 GET / 404", "1.1.1.1 POST /a 200"], 1), [("1.1.1.1", 2)]),
    ((["b GET / 200", "a GET / 200", "c GET / 200", "c GET /x 500"], 2), [("c", 2), ("a", 1)]),
    ((["broken line", "", "9.9.9.9 GET / 200 extra", "8.8.8.8 GET / 200"], 5), [("8.8.8.8", 1)]),
    (([], 3), []),
    ((_LINES, 10), _TOP),
]
