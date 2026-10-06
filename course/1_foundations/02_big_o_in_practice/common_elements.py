"""
Common Elements                                                               [easy]

Return the sorted list of distinct values that appear in both `a` and `b`.

Example:
    common_elements([4, 9, 5], [9, 4, 9, 8, 4])  ->  [4, 9]

Aim for:  O(n + m) plus sorting the answer. The last test has 100,000 items in
          each list, so `x in b` on a list inside a loop will time out.
Hint:     set(a) & set(b)
"""


def common_elements(a: list[int], b: list[int]) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 2, 2, 1], [2, 2]), [2]),
    (([4, 9, 5], [9, 4, 9, 8, 4]), [4, 9]),
    (([], [1]), []),
    (([3, 1, 2], [6, 5, 4]), []),
    ((list(range(100_000)), list(range(50_000, 150_000))), list(range(50_000, 100_000))),
]
