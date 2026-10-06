"""
Freelance job planner                                                          [build]

You're offered jobs as (name, start, end, pay). You can work on one job at a
time, and a job may start exactly when another ends. Return (total, names):
the most money you can earn, and the jobs that earn it, sorted by start time.

    best_job_schedule([("logo", 1, 3, 50), ("site", 2, 5, 20), ("app", 3, 10, 100), ("fix", 6, 9, 70)])
    ->  (150, ["logo", "app"])

Rules:
  - Any best plan is accepted. The tests check that your jobs don't overlap, that they
    add up to your total, and that the total is the maximum possible.
  - No jobs (or none worth taking) gives (0, []).

Aim for:  O(n log n): weighted interval scheduling.
Hint:     Sort by end time. best[i] = best total using the first i jobs = max(best[i-1],
          pay_i + best[p]), where p = how many jobs end by job i's start (bisect over the end
          times). Remember which choice won, so you can walk back and list the jobs.
"""


def best_job_schedule(jobs: list[tuple[str, int, int, int]]) -> tuple[int, list[str]]:
    raise NotImplementedError  # replace this line with your solution


def _best_total(jobs):
    import bisect as _b
    jobs = sorted(jobs, key=lambda j: j[2])
    ends = [j[2] for j in jobs]
    best = [0] * (len(jobs) + 1)
    for i, (_, s, e, pay) in enumerate(jobs, 1):
        p = _b.bisect_right(ends, s, 0, i - 1)
        best[i] = max(best[i - 1], pay + best[p])
    return best[-1]


def CHECK(got, expected, args):
    jobs = {j[0]: j for j in args[0]}
    if not (isinstance(got, (tuple, list)) and len(got) == 2):
        return False
    total, names = got
    if total != _best_total(args[0]) or len(set(names)) != len(names) or any(n not in jobs for n in names):
        return False
    chosen = sorted((jobs[n] for n in names), key=lambda j: j[1])
    if [j[0] for j in chosen] != list(names):
        return False
    if any(a[2] > b[1] for a, b in zip(chosen, chosen[1:])):
        return False
    return sum(j[3] for j in chosen) == total


def _jobs(rng, n, span):
    out = []
    for i in range(n):
        s = rng.randint(0, span)
        out.append((f"j{i}", s, s + rng.randint(1, max(2, span // 5)), rng.randint(1, 100)))
    return out


def _cases():
    import random
    rng = random.Random(310)
    out = [_jobs(rng, rng.randint(0, 10), 20) for _ in range(6)] + [_jobs(rng, 50_000, 10**6)]
    return [((jobs,), f"(total {_best_total(jobs)}, any best plan)") for jobs in out]


_EX = [("logo", 1, 3, 50), ("site", 2, 5, 20), ("app", 3, 10, 100), ("fix", 6, 9, 70)]
TESTS = [((_EX,), "(150, ['logo', 'app'])"), (([("a", 1, 2, 5), ("b", 2, 3, 5), ("c", 1, 3, 9)],), "(total 10, any best plan)"),
         (([],), "(0, [])")] + _cases()
