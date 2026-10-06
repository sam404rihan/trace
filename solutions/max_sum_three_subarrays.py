def max_sum_three_subarrays(nums: list[int], k: int) -> list[int]:
    prefix = [0, *accumulate(nums)]
    window = [prefix[i + k] - prefix[i] for i in range(len(nums) - k + 1)]
    m = len(window)

    best_left = [0] * m                 # best_left[i]: earliest best window start in 0..i
    for i in range(1, m):
        best_left[i] = i if window[i] > window[best_left[i - 1]] else best_left[i - 1]
    best_right = [m - 1] * m            # best_right[i]: earliest best window start in i..m-1
    for i in range(m - 2, -1, -1):
        best_right[i] = i if window[i] >= window[best_right[i + 1]] else best_right[i + 1]

    best_total, answer = -1, []
    for mid in range(k, m - k):         # middle window; the others must not overlap it
        a, c = best_left[mid - k], best_right[mid + k]
        total = window[a] + window[mid] + window[c]
        if total > best_total:          # strict: an earlier mid wins ties
            best_total, answer = total, [a, mid, c]
    return answer
