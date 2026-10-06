"""
Support ticket queue                                                          [build]

Build the queue behind a help desk.

    q = TicketQueue()
    q.join("ana")       ->  1         joins at the back. Returns their position (1 = next to be served)
    q.join("ben")       ->  2
    q.vip("cy")         ->  1         VIPs skip to the front
    q.serve()           ->  "cy"      the front leaves the queue
    q.position("ben")   ->  2
    q.leave("ana")      ->  True      gives up and leaves
    q.serve()           ->  "ben"
    q.serve()           ->  None      nobody waiting

Rules:
  - join(name) and vip(name) do nothing (but still return the current
    position) if that name is already waiting.
  - position(name) returns -1 for someone who isn't waiting.
  - leave(name) returns False if they weren't waiting.
  - size() returns how many are waiting.

Aim for:  serve(), join() and vip() in O(1) with a deque. position() and leave()
          may scan the queue.
"""
from collections import deque


class TicketQueue:
    def __init__(self):
        raise NotImplementedError

    def join(self, name: str) -> int:
        raise NotImplementedError

    def vip(self, name: str) -> int:
        raise NotImplementedError

    def serve(self) -> str | None:
        raise NotImplementedError

    def position(self, name: str) -> int:
        raise NotImplementedError

    def leave(self, name: str) -> bool:
        raise NotImplementedError

    def size(self) -> int:
        raise NotImplementedError


CLASS = "TicketQueue"


def _big():
    from collections import deque as dq
    calls, out, q = [("TicketQueue",)], [None], dq()
    for i in range(100_000):
        calls.append(("join", f"u{i}"))
        q.append(f"u{i}")
        out.append(len(q))
        if i % 3 == 2:
            calls.append(("serve",))
            out.append(q.popleft())
    calls.append(("size",))
    out.append(len(q))
    return calls, out


_CALLS, _OUT = _big()

TESTS = [
    ([("TicketQueue",), ("join", "ana"), ("join", "ben"), ("vip", "cy"), ("serve",), ("position", "ben"),
      ("leave", "ana"), ("serve",), ("serve",)],
     [None, 1, 2, 1, "cy", 2, True, "ben", None]),
    ([("TicketQueue",), ("join", "a"), ("join", "a"), ("vip", "a"), ("size",), ("position", "zed"), ("leave", "zed")],
     [None, 1, 1, 1, 1, -1, False]),
    ([("TicketQueue",), ("join", "a"), ("join", "b"), ("join", "c"), ("leave", "b"), ("position", "c"),
      ("vip", "d"), ("position", "c"), ("size",)],
     [None, 1, 2, 3, True, 2, 1, 3, 3]),
    ([("TicketQueue",), ("serve",), ("size",)], [None, None, 0]),
    (_CALLS, _OUT),
]
