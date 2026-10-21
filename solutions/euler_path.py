def euler_path(n: int, roads: list[list[int]]) -> list[int]:
    # Hierholzer: walk while you can; a place with no roads left is finished and joins the route.
    out = [[] for _ in range(n)]
    for a, b in roads:
        out[a].append(b)
    route, stack = [], [0]
    while stack:
        if out[stack[-1]]:
            stack.append(out[stack[-1]].pop())      # take an unused road
        else:
            route.append(stack.pop())               # stuck here: this place is done
    return route[::-1]
