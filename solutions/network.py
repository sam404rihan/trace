class Network:
    def __init__(self):
        self.parent = {}
        self.size = {}
        self.group_count = 0
        self.biggest = 0

    def add(self, name: str) -> None:
        if name not in self.parent:
            self.parent[name] = name
            self.size[name] = 1
            self.group_count += 1
            self.biggest = max(self.biggest, 1)

    def _find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:       # path compression
            self.parent[x], x = root, self.parent[x]
        return root

    def connect(self, a: str, b: str) -> bool:
        self.add(a)
        self.add(b)
        ra, rb = self._find(a), self._find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:   # union by size: small tree under big root
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.group_count -= 1
        self.biggest = max(self.biggest, self.size[ra])
        return True

    def connected(self, a: str, b: str) -> bool:
        if a not in self.parent or b not in self.parent:
            return False
        return self._find(a) == self._find(b)

    def groups(self) -> int:
        return self.group_count

    def largest(self) -> int:
        return self.biggest

    def size_of(self, name: str) -> int:
        return self.size[self._find(name)] if name in self.parent else 0
