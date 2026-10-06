import re


class WordIndex:
    def __init__(self):
        self.ids_by_word = {}       # word -> set of doc ids   (the inverted index)
        self.words_by_id = {}       # doc id -> set of words   (so remove() knows what to undo)

    @staticmethod
    def _words(text):
        return set(re.findall(r"[a-z0-9]+", text.lower()))

    def add(self, doc_id: int, text: str) -> None:
        self.remove(doc_id)                     # adding an existing id replaces it
        words = self._words(text)
        self.words_by_id[doc_id] = words
        for w in words:
            self.ids_by_word.setdefault(w, set()).add(doc_id)

    def remove(self, doc_id: int) -> None:
        for w in self.words_by_id.pop(doc_id, ()):
            ids = self.ids_by_word[w]
            ids.discard(doc_id)
            if not ids:
                del self.ids_by_word[w]

    def search(self, word: str) -> list[int]:
        return sorted(self.ids_by_word.get(word.lower(), ()))

    def search_all(self, words: list[str]) -> list[int]:
        if not words:
            return []
        sets = [self.ids_by_word.get(w.lower(), set()) for w in words]
        return sorted(set.intersection(*sets))
