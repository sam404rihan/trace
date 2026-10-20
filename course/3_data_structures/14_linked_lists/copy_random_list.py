"""
Copy List with Random Pointer                                                 [medium]

Each Node has .val, .next, and .random, which points at any node of the list
or is None. Return a deep copy: all brand-new nodes, wired up the same way.
None of your nodes may be original nodes.

Tests write a list as [[val, random_index], ...], where random_index is None
or the position the random pointer goes to.

Example:
    [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]]   copies to the same shape with new nodes

Aim for:  O(n) time.
Hint:     Two passes with a dict original → copy. First pass: create every copy. Second pass:
          copy.next = map[orig.next] and copy.random = map[orig.random]. (map.get handles None.)
"""


class Node:
    def __init__(self, val: int, next=None, random=None):
        self.val = val
        self.next = next
        self.random = random


def copy_random_list(head: Node | None) -> Node | None:
    raise NotImplementedError  # replace this line with your solution


_ORIGINAL = []


def PREPARE(spec):
    nodes = [Node(v) for v, _ in spec]
    for i, (_, r) in enumerate(spec):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        nodes[i].random = nodes[r] if r is not None else None
    _ORIGINAL[:] = [set(map(id, nodes))]
    return (nodes[0] if nodes else None,)


def FINISH(head):
    seen, out, index = [], [], {}
    node = head
    while node is not None and len(seen) < 10_000:
        if id(node) in _ORIGINAL[0]:
            return "returned an original node instead of a copy"
        index[id(node)] = len(seen)
        seen.append(node)
        node = node.next
    for n in seen:
        out.append([n.val, None if n.random is None else index.get(id(n.random), "points outside the copy")])
    return out


_CASES = [
    [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]],
    [[1, 1], [2, 1]],
    [[3, None], [3, 0], [3, None]],
    [],
    [[5, 0]],
]
USES = []

TESTS = [((c,), c) for c in _CASES]
