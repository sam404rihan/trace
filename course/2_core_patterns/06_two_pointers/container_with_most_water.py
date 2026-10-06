"""
Container With Most Water                                    [medium] · two pointers

`height[i]` is the height of a vertical line at x = i. Pick two lines that,
together with the x-axis, hold the most water. Return that amount:
    width * min(left height, right height)

Example:
    container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7])  ->  49   (lines 1 and 8)

Aim for:  O(n) time
Hint:     Start with the widest container. Moving the taller line inwards can
          never help — so which pointer should move?
"""


def container_with_most_water(height: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 8, 6, 2, 5, 4, 8, 3, 7],), 49),
    (([1, 1],), 1),
    (([4, 3, 2, 1, 4],), 16),
    (([1, 2, 1],), 2),
]
