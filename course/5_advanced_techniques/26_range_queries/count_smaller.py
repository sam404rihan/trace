"""
Count of Smaller Numbers After Self                                             [hard]

For each position i, count how many numbers to the RIGHT of nums[i] are smaller
than nums[i]. Return the list of counts.

Example:
    count_smaller([5, 2, 6, 1])  ->  [2, 1, 1, 0]

Aim for:  O(n log n). The last test has 100,000 numbers.
Hint:     Walk from the right, with a Fenwick tree over VALUES (compress them to ranks 1..k first).
          For each x: the answer is prefix(rank(x) - 1), the count of smaller values seen so far,
          then add(rank(x), 1). (A merge sort that counts can do it too.)
"""


def count_smaller(nums: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    return [sum(1 for y in nums[i + 1:] if y < x) for i, x in enumerate(nums)]


def _fast(nums):
    ranks = {v: i + 1 for i, v in enumerate(sorted(set(nums)))}
    tree, out = [0] * (len(ranks) + 1), []
    for x in reversed(nums):
        r, s, k = ranks[x], 0, ranks[x] - 1
        while k > 0:
            s += tree[k]
            k -= k & -k
        out.append(s)
        while r < len(tree):
            tree[r] += 1
            r += r & -r
    return out[::-1]


def _cases():
    import random
    rng = random.Random(206)
    out = [(([rng.randint(-5, 5) for _ in range(rng.randint(0, 15))],), None) for _ in range(8)]
    out = [((a[0],), _brute(a[0])) for a, _ in out]
    big = [rng.randint(-10**4, 10**4) for _ in range(100_000)]
    out.append(((big,), _fast(big)))
    return out


USES = ["fenwick.prefix", "fenwick.update", "array.rank_compress"]

TESTS = [(([5, 2, 6, 1],), [2, 1, 1, 0]), (([-1],), [0]), (([-1, -1],), [0, 0]), (([3, 2, 1],), [2, 1, 0])] + _cases()
