"""
Names that every run can use without importing anything, like LeetCode's preloaded
environment. The judge puts PRELUDE into the namespace before your code runs, so

    q = deque([root])
    heappush(heap, (dist, node))
    i = bisect_left(nums, x)
    @lru_cache(None)
    def f(n: int) -> List[int]: ...

all just work. Your own definitions (or imports) always win over these.
"""
# Whole modules, for the dotted style: math.sqrt, heapq.heappush, collections.deque ...
import bisect
import collections
import copy
import functools
import heapq
import itertools
import math
import operator
import random
import re
import string
import sys
import typing

# collections
from collections import ChainMap, Counter, OrderedDict, defaultdict, deque, namedtuple
# heapq
from heapq import heapify, heappop, heappush, heappushpop, heapreplace, nlargest, nsmallest
# bisect (the module name `bisect` stays the module, so bisect.bisect_left works too)
from bisect import bisect_left, bisect_right, insort, insort_left, insort_right
# functools
from functools import cache, cmp_to_key, lru_cache, partial, reduce
# itertools
from itertools import (accumulate, chain, combinations, combinations_with_replacement, groupby, islice,
                       pairwise, permutations, product, zip_longest)
# math
from math import ceil, comb, factorial, floor, gcd, inf, isqrt, lcm, log2, perm, prod, sqrt
# typing, for LeetCode-style signatures
from typing import Any, Callable, Deque, Dict, Iterable, Iterator, List, Optional, Set, Tuple, Union
# string constants
from string import ascii_letters, ascii_lowercase, ascii_uppercase
# the playground's own helpers
from helpers import ListNode, TreeNode, build_list, build_tree, print_tree, to_list, tree_to_list

# ── max-heaps ────────────────────────────────────────────────────────────────
# Python 3.14 added max-heap functions to heapq: a plain list kept in MAX-heap order,
# so heap[0] is the largest and you never need to negate values. The sandbox runs 3.14,
# so these are the real standard-library functions. The fallback below only exists so
# this file still works on an older Python (e.g. the server reading the list of names).
try:
    from heapq import heapify_max, heappop_max, heappush_max, heappushpop_max, heapreplace_max
except ImportError:  # Python < 3.14
    def heapify_max(heap: list) -> None:
        heapq._heapify_max(heap)

    def heappush_max(heap: list, item) -> None:
        heap.append(item)
        heapq._siftdown_max(heap, 0, len(heap) - 1)

    def heappop_max(heap: list):
        last = heap.pop()
        if heap:
            top, heap[0] = heap[0], last
            heapq._siftup_max(heap, 0)
            return top
        return last

    def heapreplace_max(heap: list, item):
        top, heap[0] = heap[0], item
        heapq._siftup_max(heap, 0)
        return top

    def heappushpop_max(heap: list, item):
        if heap and heap[0] > item:
            item, heap[0] = heap[0], item
            heapq._siftup_max(heap, 0)
        return item


class MaxHeap:
    """A max-heap object: h = MaxHeap([3, 1, 4]); h.push(9); h.peek() -> 9; h.pop() -> 9; len(h) -> 3."""

    def __init__(self, items=()):
        self._items = list(items)
        heapify_max(self._items)

    def push(self, item) -> None:
        heappush_max(self._items, item)

    def pop(self):
        return heappop_max(self._items)

    def peek(self):
        return self._items[0]

    def __len__(self):
        return len(self._items)

    def __bool__(self):
        return bool(self._items)

    def __repr__(self):
        return f"MaxHeap({sorted(self._items, reverse=True)})"


PRELUDE = {name: value for name, value in globals().items() if not name.startswith("_") and name != "PRELUDE"}
