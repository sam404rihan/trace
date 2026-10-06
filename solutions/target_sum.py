def target_sum(nums: list[int], target: int) -> int:
    totals = {0: 1}                         # reachable sum -> number of sign choices reaching it
    for x in nums:
        nxt = defaultdict(int)
        for t, ways in totals.items():
            nxt[t + x] += ways
            nxt[t - x] += ways
        totals = nxt
    return totals.get(target, 0)
