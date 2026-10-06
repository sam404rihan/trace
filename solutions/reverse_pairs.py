def reverse_pairs(nums: list[int]) -> int:
    def sort_count(a):
        """Return (sorted a, reverse pairs inside a): merge sort that counts on the way."""
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, cl = sort_count(a[:mid])
        right, cr = sort_count(a[mid:])
        count, i = cl + cr, 0
        for r in right:                     # both halves sorted: i only moves forward
            while i < len(left) and left[i] <= 2 * r:
                i += 1
            count += len(left) - i          # left[i:] are all > 2 * r
        merged, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged += left[i:] + right[j:]
        return merged, count

    return sort_count(nums)[1]
