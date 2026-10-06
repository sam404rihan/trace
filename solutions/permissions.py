READ, WRITE, EXEC, ADMIN = 1, 2, 4, 8
BIT = {"r": READ, "w": WRITE, "x": EXEC, "a": ADMIN}


class Permissions:
    def __init__(self):
        self.masks = {}                     # user -> int, one bit per permission

    @staticmethod
    def _bits(letters):
        bits = 0
        for ch in letters:
            bits |= BIT[ch]
        return bits

    def grant(self, user: str, letters: str) -> None:
        self.masks[user] = self.masks.get(user, 0) | self._bits(letters)     # turn bits on

    def revoke(self, user: str, letters: str) -> None:
        self.masks[user] = self.masks.get(user, 0) & ~self._bits(letters)    # turn bits off

    def has(self, user: str, letters: str) -> bool:
        need = self._bits(letters)
        return self.masks.get(user, 0) & need == need                        # all of them on?

    def describe(self, user: str) -> str:
        m = self.masks.get(user, 0)
        return "".join(ch if m & BIT[ch] else "-" for ch in "rwxa")

    def users_with(self, letters: str) -> list[str]:
        return sorted(u for u in self.masks if self.has(u, letters))

    def mask(self, user: str) -> int:
        return self.masks.get(user, 0)
