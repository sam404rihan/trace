class MaxArray:
    # Iterative segment tree: leaves at size..size+n-1, node i holds the max of nodes 2i and 2i+1.
    def __init__(self, nums: list[int]):
        n, size = len(nums), 1
        while size < n:
            size *= 2
        self.size = size
        self.tree = [float("-inf")] * (2 * size)
        self.tree[size:size + n] = nums
        for i in range(size - 1, 0, -1):
            self.tree[i] = max(self.tree[2 * i], self.tree[2 * i + 1])

    def update(self, i: int, val: int) -> None:
        k = self.size + i
        self.tree[k] = val
        k //= 2
        while k:                                    # every block containing i gets a new max
            self.tree[k] = max(self.tree[2 * k], self.tree[2 * k + 1])
            k //= 2

    def max_range(self, l: int, r: int) -> int:
        lo, hi, best = l + self.size, r + self.size + 1, float("-inf")
        while lo < hi:                              # take the blocks that sit fully inside [l, r]
            if lo & 1:
                best = max(best, self.tree[lo])
                lo += 1
            if hi & 1:
                hi -= 1
                best = max(best, self.tree[hi])
            lo //= 2
            hi //= 2
        return best
