"""
Max Chunks to Make Sorted                                                     [hard]

Cut `arr` into consecutive chunks, sort each chunk on its own, and put them back
in the same order. The result must equal sorted(arr). What's the largest number
of chunks you can cut it into? Values can repeat.

Example:
    max_chunks_to_sorted([5, 4, 3, 2, 1])  ->  1      only sorting the whole thing works
    max_chunks_to_sorted([2, 1, 3, 4, 4])  ->  4      [2, 1] [3] [4] [4]
    max_chunks_to_sorted([1, 1, 0, 0, 1])  ->  2      [1, 1, 0, 0] [1]

Aim for:  O(n) after one O(n) pass from the right (or O(n log n) with sorting).
Hint:     You can cut after index i exactly when everything on the left is <= everything on the
          right: max(arr[:i + 1]) <= min(arr[i + 1:]). Precompute the suffix minimums, then walk
          from the left keeping a running maximum and count the cut points (the end counts too).
"""


def max_chunks_to_sorted(arr: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(arr):
    n = len(arr)
    best = {0: 0}                               # best[i] = most chunks for arr[:i] that sort correctly
    target = sorted(arr)
    for end in range(1, n + 1):
        for start in range(end):
            if start in best and sorted(arr[start:end]) == target[start:end]:
                best[end] = max(best.get(end, 0), best[start] + 1)
    return best[n]


def _fast(arr):
    suffix_min = arr[:]
    for i in range(len(arr) - 2, -1, -1):
        suffix_min[i] = min(arr[i], suffix_min[i + 1])
    chunks, running = 0, float("-inf")
    for i, x in enumerate(arr):
        running = max(running, x)
        if i == len(arr) - 1 or running <= suffix_min[i + 1]:
            chunks += 1
    return chunks


def _cases():
    import random
    rng = random.Random(768)
    out = []
    for _ in range(8):
        arr = [rng.randint(0, 6) for _ in range(rng.randint(1, 12))]
        out.append(((arr,), _brute(arr)))
    big = sorted(rng.randint(0, 10**6) for _ in range(150_000))
    for _ in range(3000):                       # local disorder only
        i = rng.randrange(len(big) - 3)
        big[i], big[i + 3] = big[i + 3], big[i]
    out.append(((big,), _fast(big)))
    return out


TESTS = [
    (([5, 4, 3, 2, 1],), 1),
    (([2, 1, 3, 4, 4],), 4),
    (([1, 1, 0, 0, 1],), 2),
    (([7],), 1),
    (([1, 2, 3],), 3),
    (([0, 0, 0],), 3),
    (([4, 2, 2, 1, 1],), 1),
] + _cases()
