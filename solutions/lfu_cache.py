class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.value = {}                         # key -> value
        self.count = {}                         # key -> use count
        self.buckets = defaultdict(OrderedDict) # count -> its keys, least recent first
        self.min_count = 0

    def _touch(self, key):
        c = self.count[key]
        del self.buckets[c][key]
        if not self.buckets[c] and self.min_count == c:
            self.min_count += 1                 # key was the last one with the minimum count
        self.count[key] = c + 1
        self.buckets[c + 1][key] = None         # newest at the end

    def get(self, key: int) -> int:
        if key not in self.value:
            return -1
        self._touch(key)
        return self.value[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity == 0:
            return
        if key in self.value:
            self.value[key] = value
            self._touch(key)
            return
        if len(self.value) >= self.capacity:
            victim, _ = self.buckets[self.min_count].popitem(last=False)   # least recent of the least used
            del self.value[victim], self.count[victim]
        self.value[key] = value
        self.count[key] = 1
        self.buckets[1][key] = None
        self.min_count = 1
