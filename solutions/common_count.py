def common_count(a: list[int], b: list[int]) -> int:
    # The only change from the slow version: a set, so each `in` is O(1) instead of O(len(a)).
    present = set(a)
    return sum(1 for x in b if x in present)
