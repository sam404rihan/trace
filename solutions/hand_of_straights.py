def hand_of_straights(hand: list[int], group_size: int) -> bool:
    if len(hand) % group_size:
        return False
    count = Counter(hand)
    for v in sorted(count):                 # smallest values first: each must start its own groups
        need = count[v]
        if need == 0:
            continue
        for x in range(v, v + group_size):
            if count[x] < need:
                return False
            count[x] -= need
    return True
