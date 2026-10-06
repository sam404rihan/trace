def shortest_subarray_at_least_k(nums: list[int], k: int) -> int:
    prefix = [0, *accumulate(nums)]
    starts = deque()                # candidate start indices, prefix values increasing
    best = -1
    for j, p in enumerate(prefix):
        while starts and p - prefix[starts[0]] >= k:
            i = starts.popleft()            # its best partner is j: anything later is longer
            if best == -1 or j - i < best:
                best = j - i
        while starts and prefix[starts[-1]] >= p:
            starts.pop()                    # j starts later and lower: always a better start
        starts.append(j)
    return best
