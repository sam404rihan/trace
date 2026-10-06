from itertools import accumulate


def range_sums(nums: list[int], queries: list[list[int]]) -> list[int]:
    # Build prefix sums once (O(n)); every query is then one subtraction (O(1)).
    prefix = [0, *accumulate(nums)]
    return [prefix[r + 1] - prefix[l] for l, r in queries]
