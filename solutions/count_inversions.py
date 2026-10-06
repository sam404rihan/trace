def count_inversions(nums: list[int]) -> int:
    def sort(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, x = sort(a[:mid])
        right, y = sort(a[mid:])
        merged, i, j, inv = [], 0, 0, x + y
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
                inv += len(left) - i        # right[j] jumps ahead of every remaining left element
        return merged + left[i:] + right[j:], inv
    return sort(nums)[1]
