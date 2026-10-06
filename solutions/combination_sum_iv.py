def combination_sum_iv(nums: list[int], target: int) -> int:
    ways = [1] + [0] * target                   # ways[t]: ordered sequences summing to t
    for t in range(1, target + 1):              # amounts outside: every order is counted
        for x in nums:
            if x <= t:
                ways[t] += ways[t - x]          # x is the last number of the sequence
    return ways[target]
