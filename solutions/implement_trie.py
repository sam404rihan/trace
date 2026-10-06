class Trie:
    def __init__(self):
        self.root = {}                          # letter -> child dict; "$" marks a word end

    def _walk(self, s):
        node = self.root
        for ch in s:
            node = node.get(ch)
            if node is None:
                return None
        return node

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and "$" in node

    def starts_with(self, prefix: str) -> bool:
        node = self._walk(prefix)
        return node is not None and bool(node)   # some word passes through or ends here
