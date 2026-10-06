def min_moves_complementary(nums: list[int], limit: int) -> int:
    n = len(nums)
    diff = [0] * (2 * limit + 2)        # diff over target sums T = 2..2*limit
    for i in range(n // 2):
        a, b = sorted((nums[i], nums[n - 1 - i]))
        diff[2] += 2                    # by default a pair costs 2 moves
        diff[a + 1] -= 1                # one move is enough on [a + 1, b + limit]
        diff[b + limit + 1] += 1
        diff[a + b] -= 1                # and none at exactly a + b
        diff[a + b + 1] += 1
    best, moves = n, 0
    for t in range(2, 2 * limit + 1):
        moves += diff[t]
        best = min(best, moves)
    return best
