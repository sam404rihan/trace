class PriceBoard:
    """Iterative segment tree. Each node holds the sum and (max, -index) of its range,
    so max() picks the larger price and, on a tie, the smaller index."""

    def __init__(self, prices: list[int]):
        n = len(prices)
        size = 1
        while size < n:
            size *= 2
        self.size = size
        self.sum = [0] * (2 * size)
        self.best = [(float("-inf"), 0)] * (2 * size)
        for i, p in enumerate(prices):
            self.sum[size + i] = p
            self.best[size + i] = (p, -i)
        for i in range(size - 1, 0, -1):
            self._pull(i)

    def _pull(self, i):
        self.sum[i] = self.sum[2 * i] + self.sum[2 * i + 1]
        self.best[i] = max(self.best[2 * i], self.best[2 * i + 1])

    def update(self, i: int, price: int) -> None:
        k = self.size + i
        self.sum[k], self.best[k] = price, (price, -i)
        k //= 2
        while k:                                # fix every ancestor
            self._pull(k)
            k //= 2

    def _query(self, l, r):
        lo, hi = l + self.size, r + self.size + 1
        total, best = 0, (float("-inf"), 0)
        while lo < hi:                          # climb, taking the nodes that sit fully inside [l, r]
            if lo & 1:
                total += self.sum[lo]
                best = max(best, self.best[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                total += self.sum[hi]
                best = max(best, self.best[hi])
            lo //= 2
            hi //= 2
        return total, best

    def max_in(self, l: int, r: int) -> int:
        return self._query(l, r)[1][0]

    def sum_in(self, l: int, r: int) -> int:
        return self._query(l, r)[0]

    def argmax(self, l: int, r: int) -> int:
        return -self._query(l, r)[1][1]
