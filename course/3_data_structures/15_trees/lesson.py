r"""
# Trees

A binary tree node has `val`, `left` and `right`. Almost every tree problem
is one of two walks: **depth-first** (recursion) or **breadth-first** (a queue,
level by level).

## DFS: let the children answer first
Most tree answers follow one shape:
```
def solve(node):
    if node is None:
        return BASE            # what an empty tree gives: 0, True, None...
    left = solve(node.left)
    right = solve(node.right)
    return combine(node.val, left, right)
```
- Height: `1 + max(left, right)`, base 0
- Count nodes: `1 + left + right`
- Same tree: values equal and both sides the same

## Passing info DOWN instead
Sometimes the child needs something from above (a running sum, allowed range,
depth). Pass it as an argument: `walk(node.left, total + node.val)`.

## Answer isn't what you return?
For "diameter" or "max path", return one thing (the height) and update a
`best` variable from the outer scope (`nonlocal best`) with another.

## BFS: level by level
```
queue = deque([root])
while queue:
    for _ in range(len(queue)):    # exactly one level
        node = queue.popleft()
        ...
        if node.left: queue.append(node.left)
        if node.right: queue.append(node.right)
```
Use BFS for "level order", "right side view", "minimum depth", "closest".

## Traversal orders (DFS)
- Pre-order (node, left, right): copying or serialising a tree
- In-order (left, node, right): gives SORTED order in a BST
- Post-order (left, right, node): when children must be finished first

## Common mistakes
- Forgetting the `None` base case
- Treating a node with one child as a leaf. A leaf has BOTH children `None`
- Deep trees (a 10,000-long chain) can blow Python's recursion limit.
  An explicit stack avoids that

Build test trees with `build_tree([3, 9, 20, None, None, 15, 7])` and draw
them with `print_tree(root)`. Press Run.
"""
from collections import deque

from helpers import build_tree, print_tree

root = build_tree([3, 9, 20, None, None, 15, 7])
print_tree(root)


def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))


def count(node):
    return 0 if node is None else 1 + count(node.left) + count(node.right)


def inorder(node):
    return inorder(node.left) + [node.val] + inorder(node.right) if node else []


print("height:", height(root), " nodes:", count(root), " in-order:", inorder(root))


def levels(root):
    out, queue = [], deque([root] if root else [])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            for child in (node.left, node.right):
                if child:
                    queue.append(child)
        out.append(level)
    return out


print("levels:", levels(root))


def root_to_leaf_paths(node, path=()):
    """Info flows DOWN: the path so far is passed to each child."""
    if node is None:
        return []
    path = path + (node.val,)
    if node.left is None and node.right is None:
        return [path]
    return root_to_leaf_paths(node.left, path) + root_to_leaf_paths(node.right, path)


print("root-to-leaf paths:", root_to_leaf_paths(root))
