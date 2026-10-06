def three_sum(nums: list[int]) -> list[list[int]]:
    # Sort, fix nums[i], then two-pointer search the rest. O(n²).
    nums = sorted(nums)
    result = []
    for i in range(len(nums) - 2):
        if nums[i] > 0:
            break                            # everything after is positive too
        if i > 0 and nums[i] == nums[i - 1]:
            continue                         # same first number -> same triplets
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1                # skip duplicate second numbers
    return result
