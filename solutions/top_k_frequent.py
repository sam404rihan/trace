from collections import Counter


def top_k_frequent(nums: list[int], k: int) -> list[int]:
    # Bucket sort by frequency: buckets[c] = values that appear c times. O(n).
    counts = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]
    for value, count in counts.items():
        buckets[count].append(value)

    result = []
    for count in range(len(buckets) - 1, 0, -1):   # most frequent first
        for value in buckets[count]:
            result.append(value)
            if len(result) == k:
                return result
    return result

    # Heap version, O(n log k): return heapq.nlargest(k, counts, key=counts.get)
