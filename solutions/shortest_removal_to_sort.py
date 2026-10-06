def shortest_removal_to_sort(arr: list[int]) -> int:
    n = len(arr)
    right = n - 1                           # arr[right:] is the longest sorted suffix
    while right > 0 and arr[right - 1] <= arr[right]:
        right -= 1
    if right == 0:
        return 0                            # already sorted
    best = right                            # keep only the suffix
    j = right
    for i in range(n):                      # keep arr[:i + 1] from the sorted prefix
        if i and arr[i - 1] > arr[i]:
            break
        while j < n and arr[j] < arr[i]:    # first suffix element that can follow arr[i]
            j += 1
        best = min(best, j - i - 1)         # remove arr[i + 1:j]
    return best
