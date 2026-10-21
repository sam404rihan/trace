def cheapest_team(people: list[list[int]], costs: list[int], k: int) -> int:
    # Bitmask DP: best[mask] = cheapest team knowing the skills in mask. Hiring only adds bits,
    # so going through the masks in increasing order handles every team.
    full, inf = (1 << k) - 1, float("inf")
    masks = [sum(1 << s for s in skills) for skills in people]
    best = [inf] * (1 << k)
    best[0] = 0
    for mask in range(1 << k):
        if best[mask] == inf:
            continue
        for m, c in zip(masks, costs):
            if best[mask] + c < best[mask | m]:
                best[mask | m] = best[mask] + c
    return best[full] if best[full] < inf else -1
