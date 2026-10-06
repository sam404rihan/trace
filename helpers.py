"""
Shared helpers for linked-list and tree problems.

    build_list([1, 2, 3])            -> 1 -> 2 -> 3
    to_list(head)                    -> [1, 2, 3]
    build_tree([2, 1, 3])            -> TreeNode(2) with children 1 and 3
    tree_to_list(root)               -> [2, 1, 3]
    print_tree(root)                 -> draws the tree sideways in the terminal

Trees use LeetCode's level-order format: None marks a missing child,
e.g. [1, None, 2] is 1 with only a right child 2.
"""
from collections import deque


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

    def __repr__(self):
        vals, node, seen = [], self, set()
        while node and id(node) not in seen:
            seen.add(id(node))
            vals.append(repr(node.val))
            node = node.next
        return " -> ".join(vals) + (" -> (cycle)" if node else "")


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self):
        return f"TreeNode({self.val!r})"


def build_list(values, cycle_to=-1):
    """Build a linked list. If cycle_to >= 0, the tail points back to that index."""
    dummy = tail = ListNode()
    nodes = []
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
        nodes.append(tail)
    if nodes and cycle_to >= 0:
        tail.next = nodes[cycle_to]
    return dummy.next


def to_list(head, limit=10_000):
    """Linked list -> Python list. The limit stops runaway loops on cyclic lists."""
    out = []
    while head and len(out) < limit:
        out.append(head.val)
        head = head.next
    return out


def build_tree(values):
    """Level-order list (None = missing child) -> binary tree."""
    if not values or values[0] is None:
        return None
    items = iter(values)
    root = TreeNode(next(items))
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for side in ("left", "right"):
            v = next(items, StopIteration)
            if v is StopIteration:
                return root
            if v is not None:
                child = TreeNode(v)
                setattr(node, side, child)
                queue.append(child)
    return root


def tree_to_list(root):
    """Binary tree -> level-order list, trailing Nones trimmed."""
    out, queue = [], deque([root])
    while queue:
        node = queue.popleft()
        if node:
            out.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
        else:
            out.append(None)
    while out and out[-1] is None:
        out.pop()
    return out


def tree_str(node, prefix="", is_right=None):
    """Sideways drawing of a tree: right subtree above, left subtree below."""
    if node is None:
        return ""
    text = ""
    if node.right:
        text += tree_str(node.right, prefix + ("    " if is_right in (True, None) else "│   "), True)
    branch = {True: "┌── ", False: "└── ", None: ""}[is_right]
    text += prefix + branch + str(node.val) + "\n"
    if node.left:
        text += tree_str(node.left, prefix + ("    " if is_right in (False, None) else "│   "), False)
    return text


def print_tree(root):
    print(tree_str(root) if root else "(empty tree)", end="")
