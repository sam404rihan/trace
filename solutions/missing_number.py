def missing_number(nums: list[int]) -> int:
    # The full range 0..n sums to n(n+1)/2; whatever's short is the missing number.
    # O(n) time, O(1) space.
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)

    # Set version, O(n) space:
    #   present = set(nums)
    #   return next(i for i in range(n + 1) if i not in present)
    #
    # XOR trick: x ^ x == 0, so XOR-ing all indices and values leaves the missing one.
