def count_bad_pairs(nums: list[int]) -> int:
    seen = Counter()            # key nums[k] - k: equal keys form a good pair
    good = 0
    for k, x in enumerate(nums):
        good += seen[x - k]     # every earlier index with the same key pairs up with k
        seen[x - k] += 1
    n = len(nums)
    return n * (n - 1) // 2 - good
