def rotate_array(nums: list[int], k: int) -> list[int]:
    # O(1) extra space: three reversals.
    #   [1 2 3 4 5 6 7], k=3
    #   reverse all      -> [7 6 5 4 3 2 1]
    #   reverse first k  -> [5 6 7 4 3 2 1]
    #   reverse the rest -> [5 6 7 1 2 3 4]
    n = len(nums)
    k %= n                               # rotating by n changes nothing

    def reverse(lo, hi):
        while lo < hi:
            nums[lo], nums[hi] = nums[hi], nums[lo]
            lo += 1
            hi -= 1

    reverse(0, n - 1)
    reverse(0, k - 1)
    reverse(k, n - 1)
    return nums

    # Slicing version, O(n) extra space:  nums[:] = nums[-k:] + nums[:-k]
