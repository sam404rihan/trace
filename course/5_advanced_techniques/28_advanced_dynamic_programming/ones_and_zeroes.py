"""
Ones and Zeroes                                                               [medium]

Each string in strs is made of "0"s and "1"s. Pick as many strings as possible
while using at most m zeros and n ones in total. Return the largest count.

Example:
    ones_and_zeroes(["10", "0001", "111001", "1", "0"], 5, 3)  ->  4      "10", "0001", "1", "0"

Aim for:  O(len(strs) · m · n): 0/1 knapsack with TWO capacities.
Hint:     dp[z][o] = most strings fitting in z zeros and o ones. For each string (zeros a, ones b),
          loop z from m down to a and o from n down to b: dp[z][o] = max(dp[z][o], dp[z-a][o-b] + 1).
"""


def ones_and_zeroes(strs: list[str], m: int, n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(strs, m, n):
    best = 0
    for mask in range(1 << len(strs)):
        pick = [strs[i] for i in range(len(strs)) if mask >> i & 1]
        if sum(s.count("0") for s in pick) <= m and sum(s.count("1") for s in pick) <= n:
            best = max(best, len(pick))
    return best


def _cases():
    import random
    rng = random.Random(309)
    out = []
    for _ in range(10):
        strs = ["".join(rng.choice("01") for _ in range(rng.randint(1, 4))) for _ in range(rng.randint(1, 10))]
        m, n = rng.randint(0, 6), rng.randint(0, 6)
        out.append(((strs, m, n), _brute(strs, m, n)))
    return out


TESTS = [((["10", "0001", "111001", "1", "0"], 5, 3), 4), ((["10", "0", "1"], 1, 1), 2), ((["111"], 0, 2), 0)] + _cases()
