r"""
Binary search tree — every node's left subtree is smaller, right subtree larger.

            8
          /   \
         3     10
        / \      \
       1   6      14
          / \    /
         4   7  13

Searching is like binary search: at each node, go left or right.

Operation              Balanced tree   Degenerate tree (inserted in sorted order)
search/insert/delete   O(log n)        O(n)  — it's basically a linked list
in-order traversal     O(n)            O(n)  — visits values in sorted order

Self-balancing variants (AVL, red-black) guarantee O(log n) by rotating nodes.

Traversals (for the tree above):
    in-order   (left, node, right):  1 3 4 6 7 8 10 13 14   ← sorted!
    pre-order  (node, left, right):  8 3 1 6 4 7 10 14 13   ← copy a tree
    post-order (left, right, node):  1 4 7 6 3 13 14 10 8   ← delete a tree
    level-order (BFS):               8 3 10 1 6 14 4 7 13

Press Run to see the demo at the bottom of this file.
"""
from collections import deque

from helpers import TreeNode, tree_str


class BST:
    def __init__(self, values=()):
        self.root = None
        for v in values:
            self.insert(v)

    def insert(self, val):
        if self.root is None:
            self.root = TreeNode(val)
            return
        node = self.root
        while True:
            if val < node.val:
                if node.left is None:
                    node.left = TreeNode(val)
                    return
                node = node.left
            elif val > node.val:
                if node.right is None:
                    node.right = TreeNode(val)
                    return
                node = node.right
            else:
                return                  # no duplicates

    def contains(self, val):
        node = self.root
        while node:
            if val == node.val:
                return True
            node = node.left if val < node.val else node.right
        return False

    def delete(self, val):
        self.root = self._delete(self.root, val)

    def _delete(self, node, val):
        if node is None:
            return None
        if val < node.val:
            node.left = self._delete(node.left, val)
        elif val > node.val:
            node.right = self._delete(node.right, val)
        else:
            # Case 1 & 2: zero or one child — replace the node with that child.
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            # Case 3: two children — copy in the smallest value from the right
            # subtree (the in-order successor), then delete that value there.
            successor = node.right
            while successor.left:
                successor = successor.left
            node.val = successor.val
            node.right = self._delete(node.right, successor.val)
        return node

    def min(self):
        node = self.root
        while node and node.left:
            node = node.left
        return node.val if node else None

    def height(self, node="root"):
        node = self.root if node == "root" else node
        if node is None:
            return 0
        return 1 + max(self.height(node.left), self.height(node.right))

    def inorder(self):
        out = []

        def walk(node):
            if node:
                walk(node.left)
                out.append(node.val)
                walk(node.right)
        walk(self.root)
        return out

    def preorder(self):
        out, stack = [], [self.root] if self.root else []
        while stack:                     # iterative, using an explicit stack
            node = stack.pop()
            out.append(node.val)
            if node.right:
                stack.append(node.right)  # push right first so left pops first
            if node.left:
                stack.append(node.left)
        return out

    def postorder(self):
        out = []

        def walk(node):
            if node:
                walk(node.left)
                walk(node.right)
                out.append(node.val)
        walk(self.root)
        return out

    def level_order(self):
        out, queue = [], deque([self.root] if self.root else [])
        while queue:
            node = queue.popleft()
            out.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return out

    def __str__(self):
        return tree_str(self.root) if self.root else "(empty)"


if __name__ == "__main__":
    tree = BST([8, 3, 10, 1, 6, 14, 4, 7, 13])
    print("The tree (sideways: right is up, left is down):\n")
    print(tree)
    print("in-order:   ", tree.inorder())
    print("pre-order:  ", tree.preorder())
    print("post-order: ", tree.postorder())
    print("level-order:", tree.level_order())
    print("height:", tree.height(), "  min:", tree.min(), "  contains(6):", tree.contains(6))

    tree.delete(3)
    print("\nafter delete(3) — a node with two children, replaced by its successor 4:\n")
    print(tree)

    sorted_tree = BST(range(1, 8))
    print("inserting 1..7 in order gives a degenerate tree of height", sorted_tree.height(), "\n")
    print(sorted_tree)
