"""
Sort List                                                                     [hard]

Sort a linked list in increasing order and return the new head. Relink the
nodes: don't copy the values into a Python list and sort that.

Example:
    4 → 2 → 1 → 3          ->   1 → 2 → 3 → 4
    -1 → 5 → 3 → 4 → 0     ->   -1 → 0 → 3 → 4 → 5

Aim for:  O(n log n) time. The big test has 100,000 nodes, so insertion sort (O(n²)) is too slow.
          Bonus: O(1) extra space with bottom-up merging.
Hint:     Merge sort fits linked lists well. Split the list in half with slow/fast pointers,
          sort each half recursively, then merge two sorted lists with a dummy head. (The
          recursion is only log n deep.)
"""
from helpers import ListNode, build_list, to_list



def sort_list(head: ListNode | None) -> ListNode | None:
    raise NotImplementedError  # replace this line with your solution


def PREPARE(values):
    return (build_list(values),)


def FINISH(head):
    return to_list(head, limit=200_000)


def _cases():
    import random
    rng = random.Random(148)
    out = []
    for _ in range(8):
        values = [rng.randint(-20, 20) for _ in range(rng.randint(0, 15))]
        out.append(((values,), sorted(values)))
    big = [rng.randint(-10**6, 10**6) for _ in range(100_000)]
    out.append(((big,), sorted(big)))
    return out


USES = ["recursion.trust", "pointers.two_sequences", "sort.merge_count", "list.dummy", "list.fast_slow"]

TESTS = [
    (([4, 2, 1, 3],), [1, 2, 3, 4]),
    (([-1, 5, 3, 4, 0],), [-1, 0, 3, 4, 5]),
    (([],), []),
    (([1],), [1]),
    (([2, 1],), [1, 2]),
    (([3, 3, 1, 3],), [1, 3, 3, 3]),
] + _cases()
