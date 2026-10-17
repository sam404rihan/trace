"""
Trapping Rain Water                                                             [hard]

`height` is an elevation map where every bar is 1 wide. Return how much rain
water it traps after raining.

Example:
    trap_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])  ->  6
    trap_rain_water([4, 2, 0, 3, 2, 5])                    ->  9

Aim for:  O(n) time and O(1) space. The last test has 200,000 bars.
Hint:     Water above bar i = min(tallest bar to its left, tallest bar to its right) - height[i].
          Two pointers: keep left_max and right_max. Whichever side has the smaller max is
          already decided, so settle that side and move its pointer inward.
"""


def trap_rain_water(height: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(h):
    return sum(max(0, min(max(h[:i + 1]), max(h[i:])) - h[i]) for i in range(len(h)))


def _fast(h):
    l, r, lm, rm, w = 0, len(h) - 1, 0, 0, 0
    while l < r:
        if h[l] < h[r]:
            lm = max(lm, h[l]); w += lm - h[l]; l += 1
        else:
            rm = max(rm, h[r]); w += rm - h[r]; r -= 1
    return w


def _cases():
    import random
    rng = random.Random(48)
    out = []
    for _ in range(6):
        h = [rng.randint(0, 8) for _ in range(rng.randint(0, 25))]
        out.append(((h,), _brute(h)))
    big = [rng.randint(0, 10**6) for _ in range(200_000)]
    out.append(((big,), _fast(big)))
    return out


USES = ["array.left_right_passes", "pointers.opposite_ends"]

TESTS = [
    (([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), 6),
    (([4, 2, 0, 3, 2, 5],), 9),
    (([],), 0),
    (([3, 2, 1],), 0),
    (([2, 0, 2],), 2),
] + _cases()
