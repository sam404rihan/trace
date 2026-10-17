"""
Partition Labels                                                              [medium]

Cut s into as many pieces as possible so that each letter appears in at most
one piece. Return the sizes of the pieces, in order.

Example:
    partition_labels("ababcbacadefegdehijhklij")  ->  [9, 7, 8]

Aim for:  O(n), two passes.
Hint:     Record the LAST index of every letter. Walk the string, stretching the current piece's end
          to the last index of each letter you see. When i reaches that end, cut.
"""


def partition_labels(s: str) -> list[int]:
    raise NotImplementedError  # replace this line with your solution


def _brute(s):
    sizes, start = [], 0
    for i in range(1, len(s) + 1):
        if set(s[start:i]).isdisjoint(s[i:]):
            sizes.append(i - start)
            start = i
    return sizes


def _make(rng):
    return ("".join(rng.choice("abcdef") for _ in range(rng.randint(1, 20))),)


def _cases():
    import random
    rng = random.Random(118)
    out = []
    for _ in range(10):
        args = _make(rng)
        out.append((args, _brute(*args)))
    return out


USES = ["greedy.farthest_reach"]

TESTS = [(("ababcbacadefegdehijhklij",), [9, 7, 8]), (("eccbbbbdec",), [10]), (("abc",), [1, 1, 1]), (("a",), [1])] + _cases()
