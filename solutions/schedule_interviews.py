def schedule_interviews(candidates: dict[str, list[str]], interviewers: dict[str, tuple[int, list[str]]]) -> dict[str, tuple[str, str]]:
    # nodes: ("c", name), ("s", slot), ("i", name), plus SRC and SNK
    cap = defaultdict(dict)

    def edge(u, v, c):
        cap[u][v] = cap[u].get(v, 0) + c
        cap[v].setdefault(u, 0)
    SRC, SNK = "src", "snk"
    for cand, free in candidates.items():
        edge(SRC, ("c", cand), 1)
        for slot in set(free):
            edge(("c", cand), ("s", slot), 1)
    for who, (limit, free) in interviewers.items():
        for slot in set(free):
            edge(("s", slot), ("i", who), 1)    # one interview per interviewer per slot
        edge(("i", who), SNK, limit)
    while True:
        prev = {SRC: None}
        q = deque([SRC])
        while q and SNK not in prev:
            u = q.popleft()
            for v, c in cap[u].items():
                if c > 0 and v not in prev:
                    prev[v] = u
                    q.append(v)
        if SNK not in prev:
            break
        v = SNK
        while v != SRC:
            u = prev[v]
            cap[u][v] -= 1
            cap[v][u] += 1
            v = u
    # flow on an edge = the reverse edge's capacity (it started at 0)
    booked = defaultdict(list)                  # slot -> candidates sent there
    for cand, free in candidates.items():
        for slot in set(free):
            if cap[("s", slot)].get(("c", cand), 0) > 0:
                booked[slot].append(cand)
    plan = {}
    for slot, cands in booked.items():
        hosts = [who for who, (_, free) in interviewers.items()
                 if slot in free and cap[("i", who)].get(("s", slot), 0) > 0]
        for cand, who in zip(cands, hosts):     # flow in == flow out, so the lists line up
            plan[cand] = (who, slot)
    return plan
