from itertools import accumulate


def running_sum(nums: list[int]) -> list[int]:
    # One pass with a running total. O(n).
    result, total = [], 0
    for x in nums:
        total += x
        result.append(total)
    return result

    # Shortcut: return list(accumulate(nums))
