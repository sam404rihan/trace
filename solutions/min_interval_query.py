def min_interval_query(intervals: list[list[int]], queries: list[int]) -> list[int]:
    intervals = sorted(intervals)
    answers, heap, i = {}, [], 0
    for q in sorted(set(queries)):              # offline: handle queries in increasing order
        while i < len(intervals) and intervals[i][0] <= q:
            l, r = intervals[i]
            heappush(heap, (r - l + 1, r))      # candidates that have started
            i += 1
        while heap and heap[0][1] < q:          # ...minus those that already ended
            heappop(heap)
        answers[q] = heap[0][0] if heap else -1
    return [answers[q] for q in queries]
