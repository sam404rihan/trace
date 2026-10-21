"""
Reconstruct Itinerary                                                           [hard]

Each ticket is [from, to]. Someone used ALL the tickets exactly once, starting
at "JFK". Rebuild the trip as a list of airports. If several trips are
possible, return the one that is smallest in alphabetical (lexical) order.
At least one valid trip always exists.

Example:
    [["MUC","LHR"], ["JFK","MUC"], ["SFO","SJC"], ["LHR","SFO"]]
    ->  ["JFK", "MUC", "LHR", "SFO", "SJC"]

Aim for:  O(E log E): Hierholzer's algorithm for an Eulerian path.
Hint:     Sort each airport's destinations. DFS: from an airport, keep taking its smallest remaining
          ticket. When an airport has no tickets left, append it to the route. The route comes out
          backwards, so reverse it at the end. Dead ends end up in the right place automatically.
"""


def reconstruct_itinerary(tickets: list[list[str]]) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _brute(tickets):
    tickets = sorted(map(tuple, tickets))
    used = [False] * len(tickets)
    path = ["JFK"]

    def go():
        if len(path) == len(tickets) + 1:
            return True
        prev = None
        for i, (a, b) in enumerate(tickets):
            if not used[i] and a == path[-1] and (a, b) != prev:
                prev = (a, b)
                used[i] = True
                path.append(b)
                if go():
                    return True
                path.pop()
                used[i] = False
        return False
    go()
    return path


def _cases():
    import random
    rng = random.Random(91)
    out = []
    for _ in range(8):
        airports = ["JFK", "ATL", "SFO", "LAX", "ORD"][:rng.randint(2, 5)]
        cur, tickets = "JFK", []
        for _ in range(rng.randint(1, 9)):
            nxt = rng.choice([a for a in airports if a != cur])
            tickets.append([cur, nxt])
            cur = nxt
        rng.shuffle(tickets)
        out.append(((tickets,), _brute(tickets)))
    return out


USES = ["graph.euler"]

TESTS = [(([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]],), ["JFK", "MUC", "LHR", "SFO", "SJC"]),
         (([["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]],),
          ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"]),
         (([["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]],), ["JFK", "NRT", "JFK", "KUL"])] + _cases()
