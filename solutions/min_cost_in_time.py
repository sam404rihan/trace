def min_cost_in_time(max_time: int, edges: list[list[int]], fees: list[int]) -> int:
    n = len(fees)
    graph = defaultdict(list)
    for x, y, minutes in edges:
        graph[x].append((y, minutes))
        graph[y].append((x, minutes))
    fastest = [float("inf")] * n            # quickest arrival at each city among popped states
    heap = [(fees[0], 0, 0)]                # (cost so far, time so far, city)
    while heap:
        cost, time, city = heappop(heap)
        if city == n - 1:
            return cost                     # popped in cost order: this is the cheapest
        if time >= fastest[city]:
            continue                        # a cheaper state got here at least as fast
        fastest[city] = time
        for nxt, minutes in graph[city]:
            if time + minutes <= max_time:
                heappush(heap, (cost + fees[nxt], time + minutes, nxt))
    return -1
