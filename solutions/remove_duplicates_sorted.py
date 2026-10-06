def remove_duplicates_sorted(nums: list[int]) -> list[int]:
    # Slow pointer = length of the unique prefix; fast pointer scans. O(n), O(1) space.
    slow = 0
    for fast in range(len(nums)):
        if slow == 0 or nums[fast] != nums[slow - 1]:   # differs from the last kept value
            nums[slow] = nums[fast]
            slow += 1
    return nums[:slow]

    # If order didn't matter and space was free: sorted(set(nums))
    # Keeping order without sorting: list(dict.fromkeys(nums))
