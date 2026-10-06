"""
Hash map (what Python's dict and set are built on).

    key ──hash()──→ bucket index ──→ [ (key, value), (key, value) ]

1. hash(key) turns the key into a big integer.
2. hash % number_of_buckets picks a bucket.
3. Different keys can land in the same bucket (a "collision"), so each bucket
   holds a small list — this is called "separate chaining".
4. When the map gets too full (load factor > 0.75), double the buckets and
   re-insert everything, so buckets stay short.

Operation         Average   Worst case (everything collides)
get / put / del   O(1)      O(n)
resize            O(n), but rare enough that put is still O(1) amortised

Python's real dict uses "open addressing" (probing other slots instead of
chaining), but the idea is the same.

Press Run to see the demo at the bottom of this file.
"""


class HashMap:
    def __init__(self, capacity=8):
        self.buckets = [[] for _ in range(capacity)]
        self.size = 0

    def _bucket(self, key):
        return self.buckets[hash(key) % len(self.buckets)]

    def put(self, key, value):
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)     # update existing key
                return
        bucket.append((key, value))
        self.size += 1
        if self.size / len(self.buckets) > 0.75:
            self._resize(len(self.buckets) * 2)

    def get(self, key, default=None):
        for k, v in self._bucket(key):
            if k == key:
                return v
        return default

    def remove(self, key):
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return True
        return False

    def _resize(self, capacity):
        old_items = [pair for bucket in self.buckets for pair in bucket]
        self.buckets = [[] for _ in range(capacity)]
        for k, v in old_items:
            self._bucket(k).append((k, v))

    def __contains__(self, key):
        return any(k == key for k, _ in self._bucket(key))

    def __len__(self):
        return self.size

    def show(self):
        for i, bucket in enumerate(self.buckets):
            print(f"  bucket {i:2}: {bucket}")


if __name__ == "__main__":
    m = HashMap(capacity=4)
    for word in ["apple", "banana", "cherry"]:
        m.put(word, len(word))
    print("3 items in 4 buckets:")
    m.show()
    m.put("date", 4)   # 4/4 > 0.75 → resize to 8 buckets
    print("\nafter the 4th item it resizes to 8 buckets:")
    m.show()
    print("\nget('banana') =", m.get("banana"), "  'fig' in m =", "fig" in m)
