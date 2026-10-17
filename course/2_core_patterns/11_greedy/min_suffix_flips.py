"""
Minimum Suffix Flips                                                          [easy]

A row of bulbs starts all off. Pressing switch i flips every bulb from i to the
end of the row: on becomes off and off becomes on. `target` says which bulbs
should end up on ("1") and off ("0"). Return the fewest presses.

Example:
    min_suffix_flips("10111")  ->  3      press 0: 11111, press 1: 10000, press 2: 10111
    min_suffix_flips("000")    ->  0

Aim for:  O(n). The last test has 100,000 bulbs: really flipping the rest of the
          row on every press is O(n²) and times out.
Hint:     Go left to right. The first wrong bulb can only be fixed by its own
          switch: the bulbs to its left are already right, and switches further
          right can't reach it. So that press is forced. Don't flip anything: count
          the presses so far. A bulb is on exactly when that count is odd.
"""


def min_suffix_flips(target: str) -> int:
    raise NotImplementedError  # replace this line with your solution


TEACHES = ["greedy.forced_first"]
USES = []

TESTS = [
    (("10111",), 3),
    (("000",), 0),
    (("101",), 3),
    (("1",), 1),
    (("0",), 0),
    (("00111",), 1),
    (("110011",), 3),
    (("10" * 50_000,), 100_000),
]
