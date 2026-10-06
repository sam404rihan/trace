def candy(ratings: list[int]) -> int:
    n = len(ratings)
    give = [1] * n
    for i in range(1, n):                   # beat the left neighbour where needed
        if ratings[i] > ratings[i - 1]:
            give[i] = give[i - 1] + 1
    for i in range(n - 2, -1, -1):          # and the right one, without losing the left rule
        if ratings[i] > ratings[i + 1]:
            give[i] = max(give[i], give[i + 1] + 1)
    return sum(give)
