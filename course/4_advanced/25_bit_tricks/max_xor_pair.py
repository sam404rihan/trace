"""
Maximum XOR of Two Numbers                                                    [hard]

Return the largest nums[i] ^ nums[j] over all pairs (i may equal j, so a
single number gives 0). All numbers are between 0 and 2**31 - 1.

Example:
    max_xor_pair([3, 10, 5, 25, 2, 8])  ->  28      5 ^ 25
    max_xor_pair([0])                   ->  0
    max_xor_pair([14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70])  ->  127

Aim for:  O(31 n). Trying every pair is O(n²): too slow for 20,000 numbers.
Hint:     Build the answer one bit at a time from the top. Suppose `best` holds the answer's
          high bits so far. Try `candidate = best | the next bit`. Put every number's prefix
          (num >> shift) in a set; the candidate is reachable if some prefix p has
          p ^ (candidate >> shift) in the set too, because a ^ b == c  <=>  a ^ c == b.
          (A binary trie of the numbers works as well.)
"""


def max_xor_pair(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    return max(a ^ b for a in nums for b in nums)


def _fast(nums):
    best = 0
    for shift in range(30, -1, -1):
        cand = best | (1 << shift)
        prefixes = {x >> shift for x in nums}
        if any((p ^ (cand >> shift)) in prefixes for p in prefixes):
            best = cand
    return best


def _cases():
    import random
    rng = random.Random(421)
    out = []
    for _ in range(10):
        nums = [rng.randint(0, 2**rng.randint(1, 31) - 1) for _ in range(rng.randint(1, 12))]
        out.append(((nums,), _brute(nums)))
    big = [rng.randint(0, 2**31 - 1) for _ in range(20_000)]
    out.append(((big,), _fast(big)))
    return out


USES = ["hash.complement", "bits.shift_mask", "bits.xor_cancel"]

TESTS = [
    (([3, 10, 5, 25, 2, 8],), 28),
    (([0],), 0),
    (([14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70],), 127),
    (([1, 1],), 0),
    (([2147483647, 0],), 2147483647),
] + _cases()
