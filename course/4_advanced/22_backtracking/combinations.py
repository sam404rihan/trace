"""
All k-combinations                                                           [guided]

Return every way to choose k different numbers from 1..n, each as an
increasing list, with the lists in lexicographic order.

Example:
    combinations(4, 2)  ->  [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]

Write it with backtracking: choose, explore, un-choose. No itertools.
"""


def combinations(n: int, k: int) -> list[list[int]]:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["bt.core"]
USES = ["recursion.trust"]

STEPS = [
    {
        "title": "Choose, explore, un-choose",
        "text": "Write a helper backtrack(start, path). If path has k numbers, record a copy. Otherwise, for each x from "
                "start to n: append x, recurse with start = x + 1, then pop x.",
        "hint": "out.append(path[:]) - copy it! path keeps changing after you record it.",
        "tests": [
            ((4, 2), [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]),
            ((3, 1), [[1], [2], [3]]),
            ((3, 3), [[1, 2, 3]]),
        ],
    },
    {
        "title": "Edges",
        "text": "k = 0 has exactly one combination: the empty one. k > n has none.",
        "hint": "If your base case is 'len(path) == k', then k = 0 records [] immediately.",
        "tests": [
            ((3, 0), [[]]),
            ((2, 5), []),
            ((1, 1), [[1]]),
        ],
    },
    {
        "title": "Prune dead branches",
        "text": "combinations(30, 28) has only 435 answers, but an unpruned search wanders down hundreds of millions of "
                "paths that can never reach 28 numbers (start with 5, and only 26 numbers are left). Stop as soon as there "
                "aren't enough numbers left to fill the path.",
        "hint": "Loop x only up to n - (k - len(path)) + 1. Or: if len(path) + (n - start + 1) < k: return.",
        "tests": [
            ((5, 3), [[1, 2, 3], [1, 2, 4], [1, 2, 5], [1, 3, 4], [1, 3, 5], [1, 4, 5], [2, 3, 4], [2, 3, 5], [2, 4, 5], [3, 4, 5]]),
            ((26, 2), [[a, b] for a in range(1, 27) for b in range(a + 1, 27)]),
            ((30, 28), [[x for x in range(1, 31) if x not in (a, b)] for a in range(30, 0, -1) for b in range(30, a, -1)]),
        ],
    },
]
