"""
One pointer step                                                            [snippet]

`nums` is sorted. You're in the middle of a pair-sum search with pointers
`left` and `right`. Make exactly one move and return the new (left, right):

  - sum too small  -> move left one step right
  - sum too big    -> move right one step left
  - sum == target  -> don't move, return them as they are

Example:
    pointer_step([1, 3, 5, 8], 0, 3, 7)   ->  (0, 2)     1 + 8 = 9 is too big
    pointer_step([1, 3, 5, 8], 0, 3, 11)  ->  (1, 3)     1 + 8 = 9 is too small

Hint:     This is the whole two-pointer idea in one decision. Too small means
          nums[left] can't pair with anything, because nums[right] is already the biggest left.
"""


def pointer_step(nums: list[int], left: int, right: int, target: int) -> tuple[int, int]:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    (([1, 3, 5, 8], 0, 3, 7), (0, 2)),
    (([1, 3, 5, 8], 0, 3, 11), (1, 3)),
    (([1, 3, 5, 8], 1, 2, 8), (1, 2)),
    (([-4, -1, 2, 6], 0, 3, 2), (0, 3)),
    (([-4, -1, 2, 6], 1, 3, 0), (1, 2)),
]
