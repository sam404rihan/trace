def sliding_window_median(nums: list[int], k: int) -> list[float]:
    low, high = [], []              # max-heap (negated) and min-heap
    low_size = high_size = 0        # VALID items in each (stale ones may still sit inside)
    stale = Counter()               # values that left the window but are still in a heap

    def prune(heap, sign):
        while heap and stale[sign * heap[0]]:
            stale[sign * heap[0]] -= 1
            heappop(heap)

    def rebalance():
        nonlocal low_size, high_size
        if low_size > high_size + 1:            # low may hold one extra, never more
            heappush(high, -heappop(low))
            low_size, high_size = low_size - 1, high_size + 1
            prune(low, -1)
        elif low_size < high_size:
            heappush(low, -heappop(high))
            low_size, high_size = low_size + 1, high_size - 1
            prune(high, 1)

    def add(x):
        nonlocal low_size, high_size
        if not low or x <= -low[0]:
            heappush(low, -x)
            low_size += 1
        else:
            heappush(high, x)
            high_size += 1
        rebalance()

    def remove(x):
        nonlocal low_size, high_size
        stale[x] += 1
        if x <= -low[0]:            # it lives on the low side
            low_size -= 1
            if x == -low[0]:
                prune(low, -1)
        else:
            high_size -= 1
            if high and x == high[0]:
                prune(high, 1)
        rebalance()

    def median():
        return float(-low[0]) if k % 2 else (-low[0] + high[0]) / 2

    for x in nums[:k]:
        add(x)
    out = [median()]
    for i in range(k, len(nums)):
        add(nums[i])
        remove(nums[i - k])
        out.append(median())
    return out
