def car_fleet(target: int, position: list[int], speed: list[int]) -> int:
    fleets, slowest_ahead = 0, 0.0
    for pos, spd in sorted(zip(position, speed), reverse=True):   # nearest to the target first
        time = (target - pos) / spd
        if time > slowest_ahead:        # can't catch the fleet ahead: it leads a new fleet
            fleets += 1
            slowest_ahead = time
    return fleets
