"""
Find K-th Smallest Pair Distance                                              [hard]

The distance of a pair (nums[i], nums[j]) with i < j is |nums[i] - nums[j]|.
Of all n * (n - 1) / 2 pair distances, return the k-th smallest (1-based).

Example:
    smallest_distance_pair([1, 3, 1], 1)  ->  0      distances are 2, 0, 2
    smallest_distance_pair([1, 6, 1], 3)  ->  5
    smallest_distance_pair([1, 1, 1], 2)  ->  0

Aim for:  O(n log n + n log(max - min)). Listing every distance is O(n²): too slow for 30,000.
Hint:     Binary search on the distance d itself. After sorting, count the pairs with distance
          <= d in O(n) with two pointers: for each right end, move left forward while
          nums[right] - nums[left] > d, then add right - left. Find the smallest d with
          count >= k.
"""


def smallest_distance_pair(nums: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums, k):
    d = sorted(abs(nums[i] - nums[j]) for i in range(len(nums)) for j in range(i + 1, len(nums)))
    return d[k - 1]


def _fast(nums, k):
    nums = sorted(nums)

    def count(d):
        c = left = 0
        for right in range(len(nums)):
            while nums[right] - nums[left] > d:
                left += 1
            c += right - left
        return c
    lo, hi = 0, nums[-1] - nums[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if count(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return lo


def _cases():
    import random
    rng = random.Random(719)
    out = []
    for _ in range(10):
        nums = [rng.randint(0, 30) for _ in range(rng.randint(2, 12))]
        k = rng.randint(1, len(nums) * (len(nums) - 1) // 2)
        out.append(((nums, k), _brute(nums, k)))
    big = [rng.randint(0, 10**6) for _ in range(30_000)]
    out.append(((big, 200_000_000), _fast(big, 200_000_000)))
    return out


TESTS = [
    (([1, 3, 1], 1), 0),
    (([1, 6, 1], 3), 5),
    (([1, 1, 1], 2), 0),
    (([9, 10, 7, 10, 6, 1, 5, 4, 9, 8], 18), 2),
    (([62, 100, 4], 2), 58),
] + _cases()
