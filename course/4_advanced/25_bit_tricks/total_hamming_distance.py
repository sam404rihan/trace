"""
Total Hamming Distance                                                        [hard]

The Hamming distance between two numbers is the number of bit positions where
they differ. Return the sum of the Hamming distances over every pair of
numbers in `nums` (each pair once). Numbers are between 0 and 10**9.

Example:
    total_hamming_distance([4, 14, 2])  ->  6
        4 = 0100, 14 = 1110, 2 = 0010:  (4, 14) differ in 2 bits, (4, 2) in 2, (14, 2) in 2.
    total_hamming_distance([4, 14, 4])  ->  4

Aim for:  O(30 n). Comparing every pair is O(n²): too slow for 30,000 numbers.
Hint:     Count each bit position on its own. If `ones` numbers have that bit set and
          n - ones don't, exactly ones * (n - ones) pairs differ there. Add that up for all 30 bits.
"""


def total_hamming_distance(nums: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(nums):
    return sum(bin(nums[i] ^ nums[j]).count("1") for i in range(len(nums)) for j in range(i + 1, len(nums)))


def _fast(nums):
    n = len(nums)
    return sum(ones * (n - ones) for ones in (sum(x >> b & 1 for x in nums) for b in range(30)))


def _cases():
    import random
    rng = random.Random(477)
    out = []
    for _ in range(10):
        nums = [rng.randint(0, 64) for _ in range(rng.randint(1, 12))]
        out.append(((nums,), _brute(nums)))
    big = [rng.randint(0, 10**9) for _ in range(30_000)]
    out.append(((big,), _fast(big)))
    return out


TESTS = [
    (([4, 14, 2],), 6),
    (([4, 14, 4],), 4),
    (([7],), 0),
    (([0, 0, 0],), 0),
    (([0, 1023],), 10),
] + _cases()
