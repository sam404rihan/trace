def permutations(nums: list[int]) -> list[list[int]]:
    # Fill one slot at a time with any unused number, then backtrack. O(n · n!).
    result, path = [], []
    used = [False] * len(nums)

    def explore():
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            explore()
            path.pop()                 # undo the choice...
            used[i] = False            # ...so the next branch starts clean

    explore()
    return result
