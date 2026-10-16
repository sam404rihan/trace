from collections import deque


def club_hops(clubs: list[list[str]], start: str, target: str) -> int:
    if start == target:
        return 0
    clubs_of = {}
    for i, club in enumerate(clubs):          # index each person to the clubs they're in
        for person in club:
            clubs_of.setdefault(person, []).append(i)
    used, seen = set(), {start}
    queue = deque([(start, 0)])
    while queue:
        person, hops = queue.popleft()
        for i in clubs_of.get(person, []):
            if i in used:                      # each club is expanded once, however many members it has
                continue
            used.add(i)
            for other in clubs[i]:
                if other == target:
                    return hops + 1
                if other not in seen:
                    seen.add(other)
                    queue.append((other, hops + 1))
    return -1
