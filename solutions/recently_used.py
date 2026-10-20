from collections import OrderedDict


class RecentlyUsed:
    # An OrderedDict is a dict plus a doubly linked list: O(1) lookup, O(1) move to the end.
    def __init__(self):
        self.order = OrderedDict()          # least recently used first

    def use(self, key: str) -> None:
        self.order[key] = None
        self.order.move_to_end(key)

    def oldest(self) -> str | None:
        return next(iter(self.order), None)

    def drop_oldest(self) -> str | None:
        return self.order.popitem(last=False)[0] if self.order else None
