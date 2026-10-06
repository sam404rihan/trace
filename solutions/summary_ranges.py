class SummaryRanges:
    def __init__(self):
        self.starts = []        # disjoint, non-touching intervals [starts[i], ends[i]], sorted
        self.ends = []

    def add_num(self, value: int) -> None:
        i = bisect_right(self.starts, value) - 1        # the interval starting at or before value
        if i >= 0 and self.ends[i] >= value:
            return                                      # already covered
        joins_left = i >= 0 and self.ends[i] == value - 1
        joins_right = i + 1 < len(self.starts) and self.starts[i + 1] == value + 1
        if joins_left and joins_right:                  # value bridges two intervals: merge them
            self.ends[i] = self.ends[i + 1]
            del self.starts[i + 1], self.ends[i + 1]
        elif joins_left:
            self.ends[i] = value
        elif joins_right:
            self.starts[i + 1] = value
        else:
            self.starts.insert(i + 1, value)
            self.ends.insert(i + 1, value)

    def get_intervals(self) -> list[list[int]]:
        return [[s, e] for s, e in zip(self.starts, self.ends)]
