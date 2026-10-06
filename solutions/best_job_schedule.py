def best_job_schedule(jobs):
    jobs = sorted(jobs, key=lambda j: j[2])             # by end time
    ends = [j[2] for j in jobs]
    best = [0] * (len(jobs) + 1)                        # best[i]: using only the first i jobs
    prev = [0] * (len(jobs) + 1)                        # where taking job i jumps back to
    for i, (_, start, end, pay) in enumerate(jobs, 1):
        p = bisect_right(ends, start, 0, i - 1)         # jobs that end by this one's start
        prev[i] = p
        best[i] = max(best[i - 1], pay + best[p])
    names, i = [], len(jobs)
    while i > 0:                                        # walk back through the decisions
        if best[i] == best[i - 1]:
            i -= 1                                      # job i wasn't needed
        else:
            names.append(jobs[i - 1])
            i = prev[i]
    names.sort(key=lambda j: j[1])
    return best[-1], [j[0] for j in names]
