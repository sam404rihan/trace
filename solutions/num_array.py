class NumArray:
    def __init__(self, nums: list[int]):
        self.n = len(nums)
        self.vals = list(nums)
        self.tree = [0] * (self.n + 1)          # Fenwick tree, 1-based
        for i, x in enumerate(nums):
            self._add(i + 1, x)

    def _add(self, k, delta):
        while k <= self.n:
            self.tree[k] += delta
            k += k & -k

    def _prefix(self, k):
        s = 0
        while k > 0:
            s += self.tree[k]
            k -= k & -k
        return s

    def update(self, i: int, val: int) -> None:
        self._add(i + 1, val - self.vals[i])    # push the change, not the new value
        self.vals[i] = val

    def sum_range(self, l: int, r: int) -> int:
        return self._prefix(r + 1) - self._prefix(l)
