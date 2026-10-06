def subsets_ii(nums):
    nums = sorted(nums)
    out, path = [], []

    def backtrack(start):
        out.append(path[:])                 # every node of the tree is a subset
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue                    # skip duplicate choices at this depth
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return out
