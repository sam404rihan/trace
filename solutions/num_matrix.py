class NumMatrix:
    def __init__(self, matrix: list[list[int]]):
        R, C = len(matrix), len(matrix[0])
        P = [[0] * (C + 1) for _ in range(R + 1)]        # P[r][c] = sum of the r×c top-left block
        for r in range(R):
            for c in range(C):
                P[r + 1][c + 1] = matrix[r][c] + P[r][c + 1] + P[r + 1][c] - P[r][c]
        self.P = P

    def sum_region(self, r1: int, c1: int, r2: int, c2: int) -> int:
        P = self.P
        return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]
