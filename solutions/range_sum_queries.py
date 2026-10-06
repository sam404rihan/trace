def range_sum_queries(nums: list[int], queries: list[tuple[int, int]]) -> list[int]:
    P = [0]                         # P[k] = sum of the first k numbers
    for x in nums:
        P.append(P[-1] + x)
    return [P[j + 1] - P[i] for i, j in queries]     # each query is O(1)
