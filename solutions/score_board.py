class ScoreBoard:
    def __init__(self, scores: list[int]):
        self.n = len(scores)
        self.P = [0]                            # P[k] = sum of the first k days
        for s in scores:
            self.P.append(self.P[-1] + s)

    def total(self, i: int, j: int) -> int:
        return self.P[j + 1] - self.P[i]

    def average(self, i: int, j: int) -> float:
        return round(self.total(i, j) / (j - i + 1), 2)

    def best_stretch(self, k: int) -> int:
        # Every window of k days is one prefix subtraction.
        return max(self.P[end] - self.P[end - k] for end in range(k, self.n + 1))

    def first_reaching(self, x: int) -> int:
        for d in range(self.n):
            if self.P[d + 1] >= x:
                return d
        return -1
