class FencePlanner:
    def __init__(self):
        self.posts = []
        self.hull = []                      # counterclockwise corners of the current fence
        self.stale = False

    @staticmethod
    def _cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    def _rebuild(self):
        pts = sorted(set(self.posts))
        if len(pts) <= 2:
            self.hull = pts
        else:
            lower, upper = [], []
            for p in pts:
                while len(lower) >= 2 and self._cross(lower[-2], lower[-1], p) <= 0:
                    lower.pop()
                lower.append(p)
            for p in reversed(pts):
                while len(upper) >= 2 and self._cross(upper[-2], upper[-1], p) <= 0:
                    upper.pop()
                upper.append(p)
            self.hull = lower[:-1] + upper[:-1]
        self.stale = False

    def _current(self):
        if self.stale:
            self._rebuild()
        return self.hull

    def add(self, x: int, y: int) -> None:
        self.posts.append((x, y))
        if not self.stale and not (len(self.hull) >= 3 and self.encloses(x, y)):
            self.stale = True               # only a post outside the fence can move it

    def area(self) -> float:
        h = self._current()
        if len(h) < 3:
            return 0.0
        return abs(sum(self._cross((0, 0), h[i], h[(i + 1) % len(h)]) for i in range(len(h)))) / 2

    def perimeter(self) -> float:
        h = self._current()
        if len(h) < 2:
            return 0.0
        return sum(math.dist(h[i], h[(i + 1) % len(h)]) for i in range(len(h)))

    def encloses(self, x: int, y: int) -> bool:
        h, pt = self._current(), (x, y)
        if not h:
            return False
        if len(h) == 1:
            return h[0] == pt
        if len(h) == 2:
            a, b = h
            return (self._cross(a, b, pt) == 0 and min(a[0], b[0]) <= x <= max(a[0], b[0])
                    and min(a[1], b[1]) <= y <= max(a[1], b[1]))
        return all(self._cross(h[i], h[(i + 1) % len(h)], pt) >= 0 for i in range(len(h)))
