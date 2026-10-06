"""
Flatten a Nested List                                                         [easy]

`nested` is a list whose items are integers or other (nested) lists.
Return all the integers in order, in one flat list.

Example:
    flatten_list([1, [2, [3, [4]], 5]])  ->  [1, 2, 3, 4, 5]

Aim for:  O(total items)
Hint:     For each item: if isinstance(item, list), flatten it (recursion!) and
          add its items; otherwise add the item itself.
"""


def flatten_list(nested: list) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, [2, [3, [4]], 5]],), [1, 2, 3, 4, 5]),
    (([],), []),
    (([[[]]],), []),
    (([[1, 2], [3], [[4, [5, 6]]]],), [1, 2, 3, 4, 5, 6]),
    (([7],), [7]),
]
