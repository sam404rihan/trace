"""
Text editor with undo and redo                                                [build]

Build the core of a text editor.

    ed = TextEditor()
    ed.type("hello")
    ed.type(" world")
    ed.delete(6)        ->  " world"     returns what was removed
    ed.text()           ->  "hello"
    ed.undo()           ->  True         the delete is undone
    ed.text()           ->  "hello world"
    ed.redo()           ->  True         ... and done again
    ed.text()           ->  "hello"

Rules:
  - type(s) adds s at the end. delete(k) removes the last k characters (or all
    of them if there are fewer) and returns the removed text.
  - undo() reverts the most recent type/delete that hasn't been undone, and returns
    True. With nothing to undo, it returns False.
  - redo() re-applies the most recently undone action. Returns False if there's nothing to redo.
  - Any new type() or delete() clears the redo history.
  - delete(0), or deleting from empty text, removes nothing and isn't recorded.

Aim for:  two stacks of actions (undo and redo). Each action remembers enough to
          reverse itself: ("type", s) or ("delete", removed_text).
"""


class TextEditor:
    def __init__(self):
        raise NotImplementedError

    def type(self, s: str) -> None:
        raise NotImplementedError

    def delete(self, k: int) -> str:
        raise NotImplementedError

    def undo(self) -> bool:
        raise NotImplementedError

    def redo(self) -> bool:
        raise NotImplementedError

    def text(self) -> str:
        raise NotImplementedError


CLASS = "TextEditor"

USES = ["stack.lifo"]

TESTS = [
    ([("TextEditor",), ("type", "hello"), ("type", " world"), ("delete", 6), ("text",), ("undo",), ("text",),
      ("redo",), ("text",)],
     [None, None, None, " world", "hello", True, "hello world", True, "hello"]),
    ([("TextEditor",), ("undo",), ("redo",), ("type", "ab"), ("undo",), ("undo",), ("text",), ("redo",), ("text",)],
     [None, False, False, None, True, False, "", True, "ab"]),
    ([("TextEditor",), ("type", "abc"), ("delete", 10), ("text",), ("undo",), ("type", "d"), ("redo",), ("text",)],
     [None, None, "abc", "", True, None, False, "abcd"]),
    ([("TextEditor",), ("type", "x"), ("delete", 0), ("undo",), ("text",), ("delete", 5), ("undo",), ("text",)],
     [None, None, "", True, "", "", False, ""]),
    ([("TextEditor",), ("type", "a"), ("type", "b"), ("type", "c"), ("undo",), ("undo",), ("redo",), ("text",),
      ("delete", 1), ("delete", 1), ("undo",), ("undo",), ("text",)],
     [None, None, None, None, True, True, True, "ab", "b", "a", True, True, "ab"]),
]
