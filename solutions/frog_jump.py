def frog_jump(stones: list[int]) -> bool:
    jumps = {p: set() for p in stones}  # stone -> sizes of the jumps that can land on it
    jumps[0].add(0)
    for p in stones:                    # in order: every jump onto p comes from an earlier stone
        for k in jumps[p]:
            for step in (k - 1, k, k + 1):
                if step > 0 and p + step in jumps:
                    jumps[p + step].add(step)
    return bool(jumps[stones[-1]])
