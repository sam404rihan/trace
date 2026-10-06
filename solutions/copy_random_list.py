def copy_random_list(head):
    copy = {}
    node = head
    while node:                                 # pass 1: a new node for every old one
        copy[node] = Node(node.val)
        node = node.next
    for old, new in copy.items():               # pass 2: wire the copies to each other
        new.next = copy.get(old.next)
        new.random = copy.get(old.random)
    return copy.get(head)


class Node:
    def __init__(self, val, next=None, random=None):
        self.val, self.next, self.random = val, next, random
