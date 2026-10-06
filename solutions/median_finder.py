class MedianFinder:
    def __init__(self):
        self.low = []       # max-heap (negated): the smaller half
        self.high = []      # min-heap: the larger half

    def add_num(self, x: int) -> None:
        heappush(self.low, -x)
        heappush(self.high, -heappop(self.low))     # move low's biggest across, keeping the halves ordered
        if len(self.high) > len(self.low):          # rebalance: low may hold one extra
            heappush(self.low, -heappop(self.high))

    def find_median(self) -> float:
        if len(self.low) > len(self.high):
            return float(-self.low[0])
        return (-self.low[0] + self.high[0]) / 2
