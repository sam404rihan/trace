def cracking_safe(n: int, k: int) -> str:
    if n == 1:
        return "".join(map(str, range(k)))
    used = set()                            # passwords (edges) already in the sequence
    digits = []
    start = "0" * (n - 1)
    stack = [(start, 0)]                    # iterative Hierholzer: (node, next digit to try)
    trail = []                              # the digit that led into each stack entry
    while stack:
        node, d = stack[-1]
        while d < k and node + str(d) in used:
            d += 1
        if d < k:                           # walk an unused edge
            stack[-1] = (node, d + 1)
            edge = node + str(d)
            used.add(edge)
            stack.append((edge[1:], 0))
            trail.append(str(d))
        else:                               # stuck: this edge's digit goes into the circuit
            stack.pop()
            if trail:
                digits.append(trail.pop())
    return start + "".join(reversed(digits))
