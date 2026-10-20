"""
Largest Rectangle in Histogram                                                [easy]

Bars of width 1 have the given heights. Return the area of the largest
rectangle that fits entirely inside the histogram.

Example:
    largest_rectangle([2, 1, 5, 6, 2, 3])  ->  10       the bars 5 and 6, height 5, width 2
    largest_rectangle([2, 4])              ->  4

Aim for:  O(n) with a monotonic stack. The big tests have up to 200,000 bars.
Hint:     Keep a stack of indexes with increasing heights. When a lower bar arrives, pop: the popped
          bar's rectangle can't extend past this point, and it extends left to just after the bar
          now on top of the stack. width = i - stack[-1] - 1 (or i if the stack is empty).
"""


def largest_rectangle(heights: list[int]) -> int:
    raise NotImplementedError  # replace this line with your solution


def _brute(h):
    best = 0
    for i in range(len(h)):
        low = h[i]
        for j in range(i, len(h)):
            low = min(low, h[j])
            best = max(best, low * (j - i + 1))
    return best


def _fast(h):
    st, best = [], 0
    for i, x in enumerate(h + [0]):
        while st and h[st[-1]] >= x:
            top = st.pop()
            best = max(best, h[top] * (i if not st else i - st[-1] - 1))
        st.append(i)
    return best


def _cases():
    import random
    rng = random.Random(53)
    out = []
    for _ in range(6):
        h = [rng.randint(0, 9) for _ in range(rng.randint(1, 20))]
        out.append(((h,), _brute(h)))
    big = [rng.randint(0, 10**4) for _ in range(200_000)]
    out.append(((big,), _fast(big)))
    return out


TEACHES = ["stack.span"]
USES = ["stack.monotonic"]

TESTS = [(([2, 1, 5, 6, 2, 3],), 10), (([2, 4],), 4), (([1],), 1), (([0, 0],), 0), (([3, 3, 3],), 9),
         (([6, 2, 5, 4, 5, 1, 6],), 12)] + _cases() + [((list(range(1, 100_001)),), 2_500_050_000)]
