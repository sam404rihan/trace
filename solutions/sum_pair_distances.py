def sum_pair_distances(xs: list[int]) -> int:
    total = before = 0
    for k, x in enumerate(sorted(xs)):
        total += k * x - before     # x minus each of the k smaller houses, all at once
        before += x
    return total
