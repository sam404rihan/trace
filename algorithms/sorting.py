"""
Sorting algorithms, written as generators that report every step they take.

Each one sorts the list `a` in place. Wherever you see a `yield`, the
algorithm is reporting what it just did, so we can count the work:
    yield "compare", i, j     it looked at a[i] and a[j]
    yield "swap", i, j        it swapped a[i] and a[j]
    yield "write", k          it wrote a new value into a[k]
Ignore the yields and you're reading the plain algorithm.

Algorithm   Best        Average     Worst       Space      Stable?
bubble      O(n)        O(n²)       O(n²)       O(1)       yes
selection   O(n²)       O(n²)       O(n²)       O(1)       no
insertion   O(n)        O(n²)       O(n²)       O(1)       yes   ← great on nearly-sorted data
merge       O(n log n)  O(n log n)  O(n log n)  O(n)       yes
quick       O(n log n)  O(n log n)  O(n²)       O(log n)   no    ← fastest in practice
heap        O(n log n)  O(n log n)  O(n log n)  O(1)       no

"Stable" = equal items keep their original relative order.
Python's own sorted() is Timsort: a merge/insertion hybrid, O(n log n), stable.

Press Run to race them all against each other.
"""


def bubble_sort(a):
    """Bubble sort · O(n²) · swap neighbours that are out of order; big values bubble right."""
    for end in range(len(a) - 1, 0, -1):
        swapped = False
        for i in range(end):
            yield "compare", i, i + 1
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                yield "swap", i, i + 1
                swapped = True
        if not swapped:
            return                                  # no swaps → already sorted


def selection_sort(a):
    """Selection sort · O(n²) · find the smallest remaining item, put it next in line."""
    n = len(a)
    for start in range(n - 1):
        smallest = start
        for i in range(start + 1, n):
            yield "compare", smallest, i
            if a[i] < a[smallest]:
                smallest = i
        if smallest != start:
            a[start], a[smallest] = a[smallest], a[start]
            yield "swap", start, smallest


def insertion_sort(a):
    """Insertion sort · O(n²), O(n) if nearly sorted · slide each item left into place."""
    for i in range(1, len(a)):
        j = i
        while j > 0:
            yield "compare", j - 1, j
            if a[j - 1] <= a[j]:
                break
            a[j - 1], a[j] = a[j], a[j - 1]
            yield "swap", j - 1, j
            j -= 1


def merge_sort(a, lo=0, hi=None):
    """Merge sort · O(n log n) · sort each half, then merge the two sorted halves."""
    if hi is None:
        hi = len(a)
    if hi - lo <= 1:
        return
    mid = (lo + hi) // 2
    yield from merge_sort(a, lo, mid)
    yield from merge_sort(a, mid, hi)

    left, right = a[lo:mid], a[mid:hi]              # copies: this is the O(n) space
    i = j = 0
    k = lo
    while i < len(left) and j < len(right):
        yield "compare", k, mid + j
        if left[i] <= right[j]:                     # <= keeps it stable
            a[k] = left[i]
            i += 1
        else:
            a[k] = right[j]
            j += 1
        yield "write", k
        k += 1
    for value in left[i:] + right[j:]:
        a[k] = value
        yield "write", k
        k += 1


def quick_sort(a, lo=0, hi=None):
    """Quick sort · O(n log n) avg · partition around a pivot, then sort each side."""
    if hi is None:
        hi = len(a) - 1
    if lo >= hi:
        return
    # Lomuto partition: pivot = last item. Everything < pivot moves to the front.
    pivot = a[hi]
    boundary = lo                                   # a[lo:boundary] are all < pivot
    for i in range(lo, hi):
        yield "compare", i, hi
        if a[i] < pivot:
            a[boundary], a[i] = a[i], a[boundary]
            yield "swap", boundary, i
            boundary += 1
    a[boundary], a[hi] = a[hi], a[boundary]         # pivot lands in its final spot
    yield "swap", boundary, hi
    yield from quick_sort(a, lo, boundary - 1)
    yield from quick_sort(a, boundary + 1, hi)


def heap_sort(a):
    """Heap sort · O(n log n) · build a max-heap, then keep moving the max to the end."""
    n = len(a)

    def sift_down(root, size):
        while True:
            child = 2 * root + 1
            if child >= size:
                return
            if child + 1 < size:
                yield "compare", child, child + 1
                if a[child + 1] > a[child]:
                    child += 1                      # pick the bigger child
            yield "compare", root, child
            if a[root] >= a[child]:
                return
            a[root], a[child] = a[child], a[root]
            yield "swap", root, child
            root = child

    for start in range(n // 2 - 1, -1, -1):         # heapify
        yield from sift_down(start, n)
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]                 # max goes to its final place
        yield "swap", 0, end
        yield from sift_down(0, end)


ALGORITHMS = {
    "bubble": bubble_sort,
    "selection": selection_sort,
    "insertion": insertion_sort,
    "merge": merge_sort,
    "quick": quick_sort,
    "heap": heap_sort,
}


def run(name, values):
    """Sort a copy of values with the named algorithm. Returns (sorted_list, counts)."""
    a = list(values)
    counts = {"compare": 0, "swap": 0, "write": 0}
    for kind, *_ in ALGORITHMS[name](a):
        counts[kind] += 1
    return a, counts


if __name__ == "__main__":
    import random
    import time

    print("Operation counts show the growth rate; watch O(n²) explode as n doubles.\n")
    sizes = [100, 200, 400, 800]
    print(f"{'':12}" + "".join(f"{f'n={n}':>22}" for n in sizes))
    for name in ALGORITHMS:
        row = f"{name:12}"
        for n in sizes:
            data = [random.random() for _ in range(n)]
            start = time.perf_counter()
            result, counts = run(name, data)
            ms = (time.perf_counter() - start) * 1000
            assert result == sorted(data), name
            ops = counts["compare"] + counts["swap"] + counts["write"]
            row += f"{ops:>12,} ops {ms:>5.0f}ms"
        print(row)

    print("\nNow on already-sorted input (n=800):")
    data = list(range(800))
    for name in ALGORITHMS:
        _, counts = run(name, data)
        print(f"  {name:12}{sum(counts.values()):>12,} ops")
    print("\nInsertion and bubble become O(n). Quick sort with a last-item pivot hits its O(n²) worst case!")
