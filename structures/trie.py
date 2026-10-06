r"""
Trie (prefix tree) — stores strings letter by letter, sharing common prefixes.

    words: car, cart, cat, dog

        (root)
        /    \
       c      d
       |      |
       a      o
      / \     |
     r*  t*   g*        * = a word ends here
     |
     t*

Operation                 Cost (L = length of the word/prefix)
insert / search           O(L)  — independent of how many words are stored!
starts_with               O(L)
list words with prefix    O(L + size of the output)

Used for: autocomplete, spell checkers, word games (Boggle), IP routing.

Press Run to see the demo at the bottom of this file.
"""


class TrieNode:
    def __init__(self):
        self.children = {}      # letter -> TrieNode
        self.is_word = False


class Trie:
    def __init__(self, words=()):
        self.root = TrieNode()
        for w in words:
            self.insert(w)

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_word = True

    def _walk(self, prefix):
        node = self.root
        for ch in prefix:
            node = node.children.get(ch)
            if node is None:
                return None
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and node.is_word

    def starts_with(self, prefix):
        return self._walk(prefix) is not None

    def words_with_prefix(self, prefix):
        node = self._walk(prefix)
        found = []

        def collect(node, path):
            if node.is_word:
                found.append(path)
            for ch in sorted(node.children):
                collect(node.children[ch], path + ch)
        if node:
            collect(node, prefix)
        return found


if __name__ == "__main__":
    trie = Trie(["car", "cart", "cat", "care", "dog", "dot"])
    print("search('car'):       ", trie.search("car"))
    print("search('ca'):        ", trie.search("ca"), " (a prefix, not a word)")
    print("starts_with('ca'):   ", trie.starts_with("ca"))
    print("autocomplete 'car':  ", trie.words_with_prefix("car"))
    print("autocomplete 'do':   ", trie.words_with_prefix("do"))
