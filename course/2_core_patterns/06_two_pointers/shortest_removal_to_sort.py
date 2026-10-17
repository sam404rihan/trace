"""
Shortest Subarray to Remove to Make Sorted                                    [hard]

Remove one contiguous subarray (possibly empty) from `arr` so that what's left
is non-decreasing. Return the length of the shortest subarray that works.

Example:
    shortest_removal_to_sort([1, 2, 3, 10, 4, 2, 3, 5])  ->  3
        Remove [10, 4, 2] to get [1, 2, 3, 3, 5].
    shortest_removal_to_sort([5, 4, 3, 2, 1])            ->  4
    shortest_removal_to_sort([1, 2, 3])                  ->  0

Aim for:  O(n) with two pointers.
Hint:     What's kept is a sorted prefix plus a sorted suffix. Find the longest sorted prefix
          arr[:L] and the longest sorted suffix arr[R:]. Either keep only one of them, or join
          them: for each i in the prefix, move a pointer j through the suffix to the first
          arr[j] >= arr[i], and remove arr[i + 1:j]. j only ever moves right.
"""


def shortest_removal_to_sort(arr: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(arr):
    n = len(arr)
    best = n
    for i in range(n + 1):
        for j in range(i, n + 1):
            rest = arr[:i] + arr[j:]
            if all(rest[k] <= rest[k + 1] for k in range(len(rest) - 1)):
                best = min(best, j - i)
    return best


def _fast(arr):
    n = len(arr)
    r = n - 1
    while r > 0 and arr[r - 1] <= arr[r]:
        r -= 1
    if r == 0:
        return 0
    best, j = r, r
    for i in range(n):
        if i and arr[i - 1] > arr[i]:
            break
        while j < n and arr[j] < arr[i]:
            j += 1
        best = min(best, j - i - 1)
    return best


def _cases():
    import random
    rng = random.Random(1574)
    out = []
    for _ in range(10):
        arr = [rng.randint(0, 6) for _ in range(rng.randint(1, 10))]
        out.append(((arr,), _brute(arr)))
    big = sorted(rng.randint(0, 10**6) for _ in range(60_000))
    big = big[:30_000] + [rng.randint(0, 10**6) for _ in range(5_000)] + big[30_000:]
    out.append(((big,), _fast(big)))
    return out


USES = ["pointers.two_sequences"]

TESTS = [
    (([1, 2, 3, 10, 4, 2, 3, 5],), 3),
    (([5, 4, 3, 2, 1],), 4),
    (([1, 2, 3],), 0),
    (([1],), 0),
    (([2, 2, 2, 1, 1, 1],), 3),
    (([1, 2, 3, 10, 0, 7, 8, 9],), 2),
] + _cases()
