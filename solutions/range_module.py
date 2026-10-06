class RangeModule:
    def __init__(self):
        self.starts = []        # covered intervals [starts[i], ends[i]), sorted and not touching
        self.ends = []

    def _span(self, left, right):
        """Indices i..j-1 of the intervals that overlap or touch [left, right)."""
        i = bisect_left(self.ends, left)        # first interval ending at or after left
        j = bisect_right(self.starts, right)    # first interval starting after right
        return i, j

    def add_range(self, left: int, right: int) -> None:
        i, j = self._span(left, right)
        if i < j:                               # merge everything it touches into one interval
            left = min(left, self.starts[i])
            right = max(right, self.ends[j - 1])
        self.starts[i:j] = [left]
        self.ends[i:j] = [right]

    def remove_range(self, left: int, right: int) -> None:
        i, j = self._span(left, right)
        new_starts, new_ends = [], []
        for s, e in zip(self.starts[i:j], self.ends[i:j]):
            if s < left:                        # keep the piece sticking out on the left
                new_starts.append(s)
                new_ends.append(min(e, left))
            if e > right:                       # and the piece sticking out on the right
                new_starts.append(max(s, right))
                new_ends.append(e)
        self.starts[i:j] = new_starts
        self.ends[i:j] = new_ends

    def query_range(self, left: int, right: int) -> bool:
        i = bisect_right(self.starts, left) - 1     # the interval that starts at or before left
        return i >= 0 and self.ends[i] >= right
