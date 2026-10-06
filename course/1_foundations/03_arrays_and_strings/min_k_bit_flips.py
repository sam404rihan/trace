"""
Minimum K Consecutive Bit Flips                                               [hard]

`bits` holds 0s and 1s. One move picks k consecutive bits and flips all of them
(0 becomes 1, 1 becomes 0). Return the fewest moves that turn every bit into 1,
or -1 if it can't be done.

Example:
    min_k_bit_flips([0, 1, 0], 1)              ->  2
    min_k_bit_flips([1, 1, 0], 2)              ->  -1
    min_k_bit_flips([0, 0, 0, 1, 0, 1, 1, 0], 3)  ->  3

Aim for:  O(n). Actually flipping k bits per move is O(n * k), too slow for the big test.
Hint:     Go left to right. The leftmost 0 can only be fixed by a flip that STARTS there, so the
          choice is forced. Instead of flipping k bits, remember where each flip ends: keep a
          running count of active flips (+1 when one starts, -1 when one runs out). A bit is
          currently bits[i] ^ (active % 2).
"""


def min_k_bit_flips(bits: list[int], k: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _slow(bits, k):
    bits = bits[:]
    moves = 0
    for i in range(len(bits)):
        if bits[i] == 0:
            if i + k > len(bits):
                return -1
            for j in range(i, i + k):
                bits[j] ^= 1
            moves += 1
    return moves


def _fast(bits, k):
    ends = [0] * (len(bits) + 1)
    active = moves = 0
    for i, b in enumerate(bits):
        active -= ends[i]
        if b ^ (active & 1) == 0:
            if i + k > len(bits):
                return -1
            active += 1
            ends[i + k] += 1
            moves += 1
    return moves


def _cases():
    import random
    rng = random.Random(995)
    out = []
    for _ in range(8):
        n = rng.randint(1, 14)
        bits = [rng.randint(0, 1) for _ in range(n)]
        k = rng.randint(1, n)
        out.append(((bits, k), _slow(bits, k)))
    # a solvable big case: start from all ones and apply random flips
    n, k = 100_000, 5_000
    big = [1] * n
    diff = [0] * (n + 1)
    for start in rng.sample(range(n - k + 1), 20_000):     # ~20,000 forced flips x 5,000 bits each
        diff[start] ^= 1
        diff[start + k] ^= 1
    cur = 0
    for i in range(n):
        cur ^= diff[i]
        big[i] ^= cur
    out.append(((big, k), _fast(big, k)))
    return out


TESTS = [
    (([0, 1, 0], 1), 2),
    (([1, 1, 0], 2), -1),
    (([0, 0, 0, 1, 0, 1, 1, 0], 3), 3),
    (([1, 1, 1], 2), 0),
    (([0], 1), 1),
    (([0, 0], 3), -1),
    (([0, 0, 1, 1], 2), 1),
] + _cases()
