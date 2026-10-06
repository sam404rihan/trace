def subsets(nums: list[int]) -> list[list[int]]:
    # Backtracking: for each index, choose "take it" or "leave it". O(n · 2ⁿ).
    result, path = [], []

    def explore(i):
        if i == len(nums):
            result.append(path[:])     # copy! `path` keeps changing afterwards
            return
        path.append(nums[i])           # take nums[i]
        explore(i + 1)
        path.pop()                     # undo, then leave nums[i]
        explore(i + 1)

    explore(0)
    return result

    # Iterative alternative: start with [[]]; for each x, add x to a copy of
    # every subset so far.   result = [[]]; for x in nums: result += [s + [x] for s in result]
