def reconstruct_itinerary(tickets: list[list[str]]) -> list[str]:
    graph = defaultdict(list)
    for a, b in sorted(tickets, reverse=True):
        graph[a].append(b)              # reverse-sorted, so pop() hands out the smallest
    route, stack = [], ["JFK"]
    while stack:                        # Hierholzer's algorithm, iteratively
        while graph[stack[-1]]:
            stack.append(graph[stack[-1]].pop())
        route.append(stack.pop())       # stuck: this airport is finished
    return route[::-1]
