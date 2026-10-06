"""
Subsets II                                                                    [medium]

nums may contain duplicates. Return every DISTINCT subset (including the
empty one). Order doesn't matter: the tests sort your answer before comparing.

Example:
    subsets_ii([1, 2, 2])  ->  [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]

Hint:     Sort nums. Backtrack: record the current path at every node. When choosing the next number,
          skip a value equal to the previous one at the same depth, like Combination Sum II.
"""


def subsets_ii(nums: list[int]) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


def FINISH(result):
    return sorted(sorted(s) for s in result)


def _brute(nums):
    found = set()
    n = len(nums)
    for mask in range(1 << n):
        found.add(tuple(sorted(nums[i] for i in range(n) if mask >> i & 1)))
    return sorted(list(x) for x in found)


def _cases():
    import random
    rng = random.Random(82)
    return [((v,), _brute(v)) for v in ([rng.randint(0, 3) for _ in range(rng.randint(0, 8))] for _ in range(8))]


TESTS = [(([1, 2, 2],), [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]), (([0],), [[], [0]]), (([],), [[]]),
         (([4, 4, 4, 1, 4],), _brute([4, 4, 4, 1, 4]))] + _cases()
