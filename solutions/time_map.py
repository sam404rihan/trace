import bisect


class TimeMap:
    def __init__(self):
        self.times = {}     # key -> sorted timestamps (sorted for free: they only increase)
        self.values = {}    # key -> values, parallel to times

    def set(self, key: str, value: str, t: int) -> None:
        self.times.setdefault(key, []).append(t)
        self.values.setdefault(key, []).append(value)

    def get(self, key: str, t: int) -> str:
        times = self.times.get(key, [])
        i = bisect.bisect_right(times, t) - 1     # latest timestamp <= t
        return self.values[key][i] if i >= 0 else ""

    def history(self, key: str, t1: int, t2: int) -> list[str]:
        times = self.times.get(key, [])
        lo = bisect.bisect_left(times, t1)
        hi = bisect.bisect_right(times, t2)
        return self.values[key][lo:hi] if times else []
