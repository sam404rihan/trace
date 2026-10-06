"""
Where does it land?                                                         [snippet]

An array of length n is rotated right by k places (a negative k rotates left,
and k can be bigger than n). Return the new index of the item that was at
index i.

Example:
    rotate_index(1, 2, 5)   ->  3
    rotate_index(4, 2, 5)   ->  1      walks off the end and wraps around
    rotate_index(0, -1, 5)  ->  4      left by one

Hint:     One expression. Python's % always returns a value in 0..n-1, even for negatives.
"""


def rotate_index(i: int, k: int, n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((1, 2, 5), 3),
    ((4, 2, 5), 1),
    ((0, -1, 5), 4),
    ((3, 12, 5), 0),
    ((2, 0, 7), 2),
    ((0, -13, 6), 5),
]
