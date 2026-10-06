def max_chunks_to_sorted(arr: list[int]) -> int:
    n = len(arr)
    suffix_min = [0] * n            # suffix_min[i] = min(arr[i:])
    suffix_min[-1] = arr[-1]
    for i in range(n - 2, -1, -1):
        suffix_min[i] = min(arr[i], suffix_min[i + 1])
    chunks, left_max = 0, float("-inf")
    for i, x in enumerate(arr):
        left_max = max(left_max, x)
        if i == n - 1 or left_max <= suffix_min[i + 1]:     # nothing on the left must move right
            chunks += 1
    return chunks
