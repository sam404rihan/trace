def prefix_sums(nums: list[int]) -> list[int]:
    # P[k] = sum of nums[0..k-1]. (itertools.accumulate(nums, initial=0) does the same.)
    P = [0]
    for x in nums:
        P.append(P[-1] + x)
    return P
