def bus_routes(routes: list[list[int]], source: int, target: int) -> int:
    if source == target:
        return 0
    buses_at = defaultdict(list)            # stop -> buses that visit it
    for bus, route in enumerate(routes):
        for stop in route:
            buses_at[stop].append(bus)
    boarded = set()
    seen = {source}
    queue = deque([(source, 0)])            # (stop, buses taken to get there)
    while queue:
        stop, taken = queue.popleft()
        for bus in buses_at[stop]:
            if bus in boarded:
                continue                    # its stops were all queued already
            boarded.add(bus)
            for nxt in routes[bus]:
                if nxt == target:
                    return taken + 1
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, taken + 1))
    return -1
