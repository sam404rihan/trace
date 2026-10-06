"""
Min Stack                                                                     [medium]

Build a stack that also reports its minimum, with EVERY operation in O(1).

    s = MinStack()
    s.push(-2); s.push(0); s.push(-3)
    s.get_min()   ->  -3
    s.pop()
    s.top()       ->  0
    s.get_min()   ->  -2

pop, top and get_min are only called on a non-empty stack.

Hint:     Store pairs (value, minimum so far) on the stack. The minimum below any element
          never changes while that element is on the stack.
"""


class MinStack:
    def __init__(self):
        raise NotImplementedError

    def push(self, x: int) -> None:
        raise NotImplementedError

    def pop(self) -> None:
        raise NotImplementedError

    def top(self) -> int:
        raise NotImplementedError

    def get_min(self) -> int:
        raise NotImplementedError


CLASS = "MinStack"


def _cases():
    import random
    rng = random.Random(52)
    out = []
    for size in (60, 200_000):
        ops, ref, res = [("MinStack",)], [], [None]
        for _ in range(size):
            if ref and rng.random() < 0.35:
                op = rng.choice(["pop", "top", "get_min"])
                ops.append((op,))
                if op == "pop":
                    ref.pop(); res.append(None)
                elif op == "top":
                    res.append(ref[-1][0])
                else:
                    res.append(ref[-1][1])
            else:
                x = rng.randint(-1000, 1000)
                ops.append(("push", x))
                ref.append((x, min(x, ref[-1][1]) if ref else x))
                res.append(None)
        out.append((ops, res))
    return out


TESTS = [
    ([("MinStack",), ("push", -2), ("push", 0), ("push", -3), ("get_min",), ("pop",), ("top",), ("get_min",)],
     [None, None, None, None, -3, None, 0, -2]),
    ([("MinStack",), ("push", 5), ("push", 5), ("pop",), ("get_min",), ("push", 1), ("get_min",), ("pop",), ("get_min",)],
     [None, None, None, None, 5, None, 1, None, 5]),
] + _cases()
