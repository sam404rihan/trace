def longest_consecutive(nums: list[int]) -> int:
    present = set(nums)
    best = 0
    for x in present:
        if x - 1 in present:        # not the start of a run: someone else will count it
            continue
        y = x
        while y in present:         # walk to the end of this run
            y += 1
        best = max(best, y - x)
    return best                     # each number is touched at most twice: O(n)
