def best_sightseeing_pair(values: list[int]) -> int:
    best_left = values[0] + 0       # best values[i] + i among the viewpoints before j
    best = float("-inf")
    for j in range(1, len(values)):
        best = max(best, best_left + values[j] - j)
        best_left = max(best_left, values[j] + j)
    return best
