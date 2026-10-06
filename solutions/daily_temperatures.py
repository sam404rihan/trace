def daily_temperatures(temps: list[int]) -> list[int]:
    # Monotonic stack of day indices still waiting for a warmer day. O(n):
    # every day is pushed once and popped at most once.
    answer = [0] * len(temps)
    waiting = []
    for day, temp in enumerate(temps):
        while waiting and temps[waiting[-1]] < temp:
            earlier = waiting.pop()
            answer[earlier] = day - earlier
        waiting.append(day)
    return answer
