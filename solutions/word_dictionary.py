class _Node:
    __slots__ = ("kids", "end", "count")

    def __init__(self):
        self.kids = {}      # letter -> _Node
        self.end = False    # a word ends here
        self.count = 0      # how many words pass through (or end at) this node


class WordDictionary:
    def __init__(self):
        self.root = _Node()

    def add(self, word: str) -> bool:
        if self.search(word):               # no wildcards in added words, so this is an exact check
            return False
        node = self.root
        node.count += 1
        for ch in word:
            node = node.kids.setdefault(ch, _Node())
            node.count += 1
        node.end = True
        return True

    def search(self, pattern: str) -> bool:
        def match(node, i):
            if i == len(pattern):
                return node.end
            ch = pattern[i]
            if ch == ".":                   # the only place the search branches
                return any(match(kid, i + 1) for kid in node.kids.values())
            kid = node.kids.get(ch)
            return kid is not None and match(kid, i + 1)
        return match(self.root, 0)

    def count_prefix(self, prefix: str) -> int:
        node = self.root
        for ch in prefix:
            node = node.kids.get(ch)
            if node is None:
                return 0
        return node.count
