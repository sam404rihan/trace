def falling_squares(positions: list[list[int]]) -> list[int]:
    xs = sorted({x for left, side in positions for x in (left, left + side)})
    index = {x: i for i, x in enumerate(xs)}
    m = len(xs) - 1                     # cell i is [xs[i], xs[i + 1])
    top = [0] * (4 * m)                 # max height in each segment-tree node's range
    lazy = [None] * (4 * m)             # pending "set the whole range to this height"

    def push(node):
        if lazy[node] is not None:
            for child in (2 * node, 2 * node + 1):
                top[child] = lazy[child] = lazy[node]
            lazy[node] = None

    def highest(node, lo, hi, a, b):
        if b < lo or hi < a:
            return 0
        if a <= lo and hi <= b:
            return top[node]
        push(node)
        mid = (lo + hi) // 2
        return max(highest(2 * node, lo, mid, a, b), highest(2 * node + 1, mid + 1, hi, a, b))

    def set_height(node, lo, hi, a, b, h):
        if b < lo or hi < a:
            return
        if a <= lo and hi <= b:
            top[node] = lazy[node] = h          # covered: settle it lazily
            return
        push(node)
        mid = (lo + hi) // 2
        set_height(2 * node, lo, mid, a, b, h)
        set_height(2 * node + 1, mid + 1, hi, a, b, h)
        top[node] = max(top[2 * node], top[2 * node + 1])

    heights, tallest = [], 0
    for left, side in positions:
        a, b = index[left], index[left + side] - 1      # the cells under this square
        landed = highest(1, 0, m - 1, a, b) + side
        set_height(1, 0, m - 1, a, b, landed)
        tallest = max(tallest, landed)
        heights.append(tallest)
    return heights
