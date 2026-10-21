"""
Rectangle Area II                                                             [hard]

Each rectangle is [x1, y1, x2, y2] (bottom-left and top-right corners, axis
aligned, x1 < x2 and y1 < y2). Return the total area covered by at least one
rectangle, counting overlaps once, modulo 1_000_000_007. Coordinates go up to
10**9, so you can't paint a grid of unit cells.

Example:
    rectangle_area_ii([[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]])   ->  6
    rectangle_area_ii([[0, 0, 1000000000, 1000000000]])            ->  49

Aim for:  O(n² log n) with a sweep line (O(n log n) with a segment tree, not needed here).
Hint:     Sweep x from left to right. Events: at x1 a rectangle's [y1, y2) starts, at x2 it ends.
          Between two consecutive event x's the covered y-length doesn't change, so add
          covered_length × (x gap). To get covered_length, keep the active y-intervals and
          merge them (sort, then walk), or keep counts per compressed y-cell.
"""

MOD = 1_000_000_007


def rectangle_area_ii(rectangles: list[list[int]]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _grid(rects):
    """Coordinate compression: mark every compressed cell covered by some rectangle."""
    xs = sorted({v for r in rects for v in (r[0], r[2])})
    ys = sorted({v for r in rects for v in (r[1], r[3])})
    total = 0
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            if any(r[0] <= xs[i] and xs[i + 1] <= r[2] and r[1] <= ys[j] and ys[j + 1] <= r[3] for r in rects):
                total += (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])
    return total % MOD


def _sweep(rects):
    events = sorted([(x1, 1, y1, y2) for x1, y1, x2, y2 in rects] + [(x2, -1, y1, y2) for x1, y1, x2, y2 in rects])
    active, total, prev = [], 0, events[0][0]
    for x, kind, y1, y2 in events:
        covered, top = 0, float("-inf")
        for a, b in sorted(active):
            top = max(top, a)
            if b > top:
                covered += b - top
                top = b
        total += covered * (x - prev)
        prev = x
        if kind == 1:
            active.append((y1, y2))
        else:
            active.remove((y1, y2))
    return total % MOD


def _cases():
    import random
    rng = random.Random(850)
    out = []
    for _ in range(10):
        rects = []
        for _ in range(rng.randint(1, 6)):
            x1, y1 = rng.randint(0, 10), rng.randint(0, 10)
            rects.append([x1, y1, x1 + rng.randint(1, 6), y1 + rng.randint(1, 6)])
        out.append(((rects,), _grid(rects)))
    rects = []
    for _ in range(200):
        x1, y1 = rng.randint(0, 10**9 - 10**8), rng.randint(0, 10**9 - 10**8)
        rects.append([x1, y1, x1 + rng.randint(1, 10**8), y1 + rng.randint(1, 10**8)])
    out.append(((rects,), _sweep(rects)))
    return out


USES = ["intervals.merge", "intervals.sort_by_start"]

TESTS = [
    (([[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]],), 6),
    (([[0, 0, 1000000000, 1000000000]],), 49),
    (([[0, 0, 1, 1], [2, 2, 3, 3]],), 2),
    (([[0, 0, 4, 4], [1, 1, 2, 2]],), 16),
    (([[0, 0, 2, 2], [2, 0, 4, 2]],), 8),
] + _cases()
