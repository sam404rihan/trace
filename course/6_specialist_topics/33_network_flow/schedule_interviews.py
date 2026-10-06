"""
Interview scheduler                                                            [build]

A hiring team has candidates and interviewers, and a set of time slots. Each candidate
needs one interview, with any interviewer, in a slot when both are free. An interviewer
can do at most one interview per slot, and at most their daily limit in total.
Schedule as many candidates as possible.

    candidates = {"ana": ["mon 9", "mon 10"], "bo": ["mon 9"], "cy": ["mon 9"]}
    interviewers = {"kim": (2, ["mon 9", "mon 10"]), "lee": (1, ["mon 10"])}
    schedule_interviews(candidates, interviewers)
        ->  {"bo": ("kim", "mon 9"), "ana": ("lee", "mon 10")}
            only kim is free at mon 9, so bo and cy can't both get one. 2 is the most possible.

candidates maps a name to the slots they're free. interviewers maps a name to
(limit, free slots). Return a dict candidate -> (interviewer, slot) for the candidates
you schedule. Any schedule with the largest possible number of interviews is accepted.

Aim for:  one max flow on a small graph. The last test has 400 candidates, 40 interviewers
          and 30 slots.
Hint:     Don't make a node per (interviewer, slot) pair, or per (candidate, interviewer).
          Use source -> candidate (1) -> slot (1, if the candidate is free) -> interviewer
          (1, if the interviewer is free then: one interview per slot) -> sink (limit).
          Any flow path picks a slot that both are free in. To read the schedule back, for each
          slot pair up the candidates who sent flow into it with the interviewers it sent flow to.
"""


def schedule_interviews(candidates: dict[str, list[str]], interviewers: dict[str, tuple[int, list[str]]]) -> dict[str, tuple[str, str]]:
    raise NotImplementedError  # replace this line with your solution


def _maxflow(n, edges, s, t):
    """Edmonds-Karp on an adjacency dict, for computing expected answers."""
    from collections import deque
    cap = [dict() for _ in range(n)]
    for u, v, c in edges:
        cap[u][v] = cap[u].get(v, 0) + c
        cap[v].setdefault(u, 0)
    flow = 0
    while True:
        prev = {s: None}
        q = deque([s])
        while q and t not in prev:
            u = q.popleft()
            for v, c in cap[u].items():
                if c > 0 and v not in prev:
                    prev[v] = u
                    q.append(v)
        if t not in prev:
            return flow, cap
        path, v = [], t
        while v != s:
            path.append((prev[v], v))
            v = prev[v]
        push = min(cap[u][v] for u, v in path)
        for u, v in path:
            cap[u][v] -= push
            cap[v][u] += push
        flow += push


def _best(candidates, interviewers):
    cs, ins = list(candidates), list(interviewers)
    slots = sorted({s for v in candidates.values() for s in v} | {s for _, v in interviewers.values() for s in v})
    C, S, I = len(cs), len(slots), len(ins)
    si = {s: k for k, s in enumerate(slots)}
    src, snk = C + S + I, C + S + I + 1
    edges = [(src, c, 1) for c in range(C)]
    edges += [(c, C + si[s], 1) for c, name in enumerate(cs) for s in set(candidates[name])]
    edges += [(C + si[s], C + S + i, 1) for i, name in enumerate(ins) for s in set(interviewers[name][1])]
    edges += [(C + S + i, snk, interviewers[name][0]) for i, name in enumerate(ins)]
    return _maxflow(C + S + I + 2, edges, src, snk)[0]


def CHECK(got, expected, args):
    candidates, interviewers = args
    if not isinstance(got, dict) or len(got) != expected:
        return False
    used, load = set(), {}
    for cand, pick in got.items():
        try:
            who, slot = pick
        except (TypeError, ValueError):
            return False
        if cand not in candidates or who not in interviewers:
            return False
        if slot not in candidates[cand] or slot not in interviewers[who][1]:
            return False
        if (who, slot) in used:
            return False
        used.add((who, slot))
        load[who] = load.get(who, 0) + 1
    return all(load[w] <= interviewers[w][0] for w in load)


def _random(seed, nc, ni, ns, per_c, per_i, lim):
    import random
    rng = random.Random(seed)
    slots = [f"{d} {h}" for d in ("mon", "tue", "wed", "thu", "fri") for h in range(9, 17)][:ns]
    cands = {f"c{k}": rng.sample(slots, min(len(slots), rng.randint(1, per_c))) for k in range(nc)}
    ints = {f"i{k}": (rng.randint(0, lim), rng.sample(slots, min(len(slots), rng.randint(1, per_i)))) for k in range(ni)}
    return ((cands, ints), _best(cands, ints))


def _with_traps(seed, nc, ni, ns, per_c, per_i, lim, traps):
    """A random team plus `traps` small groups where taking the first free slot strands someone:
    a is free at x and y, b only at x, and their interviewer is free at both."""
    import random
    rng = random.Random(seed)
    (cands, ints), _ = _random(seed, nc, ni, ns, per_c, per_i, lim)
    for k in range(traps):
        x, y = f"sat {k}a", f"sat {k}b"
        cands[f"a{k}"] = [x, y]
        cands[f"b{k}"] = [x]
        ints[f"t{k}"] = (2, [x, y])
    return ((cands, ints), _best(cands, ints))


_EXAMPLE = ({"ana": ["mon 9", "mon 10"], "bo": ["mon 9"], "cy": ["mon 9"]}, {"kim": (2, ["mon 9", "mon 10"]), "lee": (1, ["mon 10"])})

TESTS = [(_EXAMPLE, 2), (({}, {"kim": (3, ["mon 9"])}), 0), (({"ana": ["mon 9"]}, {}), 0),
         (({"ana": ["mon 9"], "bo": ["mon 9"]}, {"kim": (5, ["mon 9"]), "lee": (0, ["mon 9"])}), 1),
         (({"ana": ["mon 9"], "bo": ["mon 9"]}, {"kim": (5, ["mon 9"]), "lee": (1, ["mon 9"])}), 2),
         (({"ana": ["tue 9"]}, {"kim": (1, ["mon 9"])}), 0)] \
    + [_random(3308 + k, *spec) for k, spec in enumerate([(5, 2, 4, 2, 3, 2), (10, 3, 6, 3, 4, 3), (25, 5, 8, 3, 5, 4),
                                                          (60, 8, 12, 4, 6, 6)])]     + [_with_traps(3320, 300, 40, 30, 3, 8, 10, 100)]
