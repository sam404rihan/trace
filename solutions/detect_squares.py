class DetectSquares:
    def __init__(self):
        self.points = Counter()                 # (x, y) -> how many times it was added

    def add(self, point: list[int]) -> None:
        self.points[tuple(point)] += 1

    def count(self, point: list[int]) -> int:
        x, y = point
        total = 0
        for (px, py), n in self.points.items():
            # (px, py) as the diagonally opposite corner: equal, non-zero side lengths
            if abs(px - x) == abs(py - y) != 0:
                total += n * self.points[(x, py)] * self.points[(px, y)]
        return total
