def product_except_self(nums: list[int]) -> list[int]:
    # answer[i] = (product left of i) * (product right of i). Two passes, O(n).
    n = len(nums)
    answer = [1] * n

    left = 1
    for i in range(n):              # answer[i] = product of nums[:i]
        answer[i] = left
        left *= nums[i]

    right = 1
    for i in range(n - 1, -1, -1):  # multiply in the product of nums[i+1:]
        answer[i] *= right
        right *= nums[i]
    return answer
