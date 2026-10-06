class TextEditor:
    def __init__(self):
        self.chars = []        # the text, as a list so typing/deleting at the end is cheap
        self.undos = []        # actions that can be undone, most recent on top
        self.redos = []        # actions that were undone, most recent on top

    def _apply(self, action):
        kind, s = action
        if kind == "type":
            self.chars.extend(s)
        else:
            del self.chars[len(self.chars) - len(s):]

    def _revert(self, action):
        kind, s = action
        self._apply(("delete" if kind == "type" else "type", s))

    def type(self, s: str) -> None:
        if s:
            action = ("type", s)
            self._apply(action)
            self.undos.append(action)
            self.redos.clear()          # a new edit makes the redo history meaningless

    def delete(self, k: int) -> str:
        k = min(k, len(self.chars))
        if k <= 0:
            return ""
        removed = "".join(self.chars[-k:])
        action = ("delete", removed)
        self._apply(action)
        self.undos.append(action)
        self.redos.clear()
        return removed

    def undo(self) -> bool:
        if not self.undos:
            return False
        action = self.undos.pop()
        self._revert(action)
        self.redos.append(action)
        return True

    def redo(self) -> bool:
        if not self.redos:
            return False
        action = self.redos.pop()
        self._apply(action)
        self.undos.append(action)
        return True

    def text(self) -> str:
        return "".join(self.chars)
