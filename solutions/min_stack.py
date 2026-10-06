class MinStack:
    def __init__(self):
        self.items = []         # (value, minimum of everything at or below this point)

    def push(self, x: int) -> None:
        low = min(x, self.items[-1][1]) if self.items else x
        self.items.append((x, low))

    def pop(self) -> None:
        self.items.pop()

    def top(self) -> int:
        return self.items[-1][0]

    def get_min(self) -> int:
        return self.items[-1][1]
