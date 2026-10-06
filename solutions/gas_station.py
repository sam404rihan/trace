def gas_station(gas: list[int], cost: list[int]) -> int:
    if sum(gas) < sum(cost):
        return -1
    start, tank = 0, 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:                # can't reach i + 1 from start, or from anywhere in between
            start, tank = i + 1, 0
    return start
