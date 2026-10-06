class _Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val, self.left, self.right = val, None, None


class TreeSet:
    def __init__(self):
        self.root = None
        self.count = 0

    def add(self, x: int) -> bool:
        if self.root is None:
            self.root = _Node(x)
            self.count = 1
            return True
        node = self.root
        while True:                     # iterative: no recursion limit on unlucky (sorted) inserts
            if x == node.val:
                return False
            side = "left" if x < node.val else "right"
            nxt = getattr(node, side)
            if nxt is None:
                setattr(node, side, _Node(x))
                self.count += 1
                return True
            node = nxt

    def contains(self, x: int) -> bool:
        node = self.root
        while node:
            if x == node.val:
                return True
            node = node.left if x < node.val else node.right
        return False

    def floor(self, x: int) -> int | None:
        best, node = None, self.root
        while node:
            if node.val <= x:
                best = node.val         # a candidate; anything better is to the right
                node = node.right
            else:
                node = node.left
        return best

    def ceiling(self, x: int) -> int | None:
        best, node = None, self.root
        while node:
            if node.val >= x:
                best = node.val         # a candidate; anything better is to the left
                node = node.left
            else:
                node = node.right
        return best

    def to_list(self) -> list[int]:
        out, stack, node = [], [], self.root
        while stack or node:            # iterative in-order traversal: sorted output
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            out.append(node.val)
            node = node.right
        return out

    def size(self) -> int:
        return self.count
