def rank_teams(votes: list[str]) -> str:
    n = len(votes[0])
    counts = {team: [0] * n for team in votes[0]}
    for vote in votes:
        for pos, team in enumerate(vote):
            counts[team][pos] += 1
    # More votes in an earlier position wins; full ties fall back to the letter.
    return "".join(sorted(counts, key=lambda t: ([-c for c in counts[t]], t)))
