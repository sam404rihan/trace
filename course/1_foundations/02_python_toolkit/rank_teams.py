"""
Rank Teams by Votes                                                           [hard]

Each vote is a string ranking every team (one letter per team) from first place
to last. Order the teams like this:

- The team with the most first-place votes wins.
- If that's tied, compare second-place votes, then third, and so on.
- If two teams are tied in every position, the alphabetically earlier one goes first.

Return the teams in order as one string. Every vote ranks the same set of teams.

Example:
    rank_teams(["ABC", "ACB", "ABC", "ACB", "ACB"])  ->  "ACB"
        A has 5 first places. For second place C has 3 votes and B has 2.
    rank_teams(["WXYZ", "XYZW"])                   ->  "XWYZ"

Aim for:  O(votes * teams + teams² log teams) with one sort.
Hint:     Count a vector per team: counts[team][position]. A sort key can be a tuple or list:
          sort by the negated counts (more votes first), then by the letter.
"""


def rank_teams(votes: list[str]) -> str:
    raise NotImplementedError  # replace this line with your solution


def _ref(votes):
    teams = list(votes[0])

    def beats(a, b):
        for pos in range(len(teams)):
            ca = sum(v[pos] == a for v in votes)
            cb = sum(v[pos] == b for v in votes)
            if ca != cb:
                return ca > cb
        return a < b

    order = []
    for t in teams:                         # insertion sort with the pairwise rule
        i = 0
        while i < len(order) and beats(order[i], t):
            i += 1
        order.insert(i, t)
    return "".join(order)


def _cases():
    import random
    rng = random.Random(1366)
    out = []
    for _ in range(8):
        teams = rng.sample("ABCDEFGHIJ", rng.randint(2, 6))
        votes = ["".join(rng.sample(teams, len(teams))) for _ in range(rng.randint(1, 12))]
        out.append(((votes,), _ref(votes)))
    return out


USES = []

TESTS = [
    ((["ABC", "ACB", "ABC", "ACB", "ACB"],), "ACB"),
    ((["WXYZ", "XYZW"],), "XWYZ"),
    ((["ZMNAGUEDSJYLBOPHRQICWFXTVK"],), "ZMNAGUEDSJYLBOPHRQICWFXTVK"),
    ((["BCA", "CAB", "CBA", "ABC", "ACB", "BAC"],), "ABC"),
    ((["M", "M", "M"],), "M"),
] + _cases()
