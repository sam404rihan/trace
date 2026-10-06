r"""
# Binary search trees

A BST is a binary tree with one rule: everything in a node's LEFT subtree is
smaller, everything in its RIGHT subtree is larger. So a search only ever goes
one way at each node, like binary search.

```
        8
      /   \
     3     10          search 6: 8 -> left -> 3 -> right -> 6
    / \      \
   1   6      14
```

## What the rule gives you
- **Search / insert:** walk down, going left if smaller, right if larger. O(height)
- **In-order traversal gives the values in sorted order.** This is the big one:
  "k-th smallest", "validate", "closest value" often reduce to walking in-order
- **Min:** keep going left. **Max:** keep going right
- **Lowest common ancestor of p and q:** the first node whose value lies between them

## Speed depends on shape
- Balanced: height is about log n, so O(log n) operations
- Built from sorted input: it becomes a linked list, O(n). Real libraries rebalance

## Python note
Python has no built-in BST. For "sorted container" needs in practice, use a
sorted list with `bisect`, or `heapq` if you only need the min/max.

## Common mistakes
- Validating by comparing each node only with its children. The rule applies
  to the WHOLE subtree, so pass a (low, high) range down
- Forgetting whether duplicates are allowed. The problem decides

Press Run to search, walk in-order, and find a common ancestor.
"""
from helpers import build_tree, print_tree

root = build_tree([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13])
print_tree(root)


def search(node, target):
    path = []
    while node:
        path.append(node.val)
        if target == node.val:
            return path
        node = node.left if target < node.val else node.right
    return path + ["not found"]


print("search 7: ", search(root, 7))
print("search 5: ", search(root, 5))


def inorder(node):
    if node:
        yield from inorder(node.left)
        yield node.val
        yield from inorder(node.right)


print("in-order (sorted!):", list(inorder(root)))


def lca(node, p, q):
    while node:
        if p < node.val and q < node.val:
            node = node.left
        elif p > node.val and q > node.val:
            node = node.right
        else:
            return node.val          # p and q split here
    return None


print("common ancestor of 4 and 7:", lca(root, 4, 7), "  of 4 and 13:", lca(root, 4, 13))
