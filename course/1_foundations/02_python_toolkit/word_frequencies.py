"""
Word frequencies                                                             [guided]

Count how often each word appears in `text`. Return a list of (word, count)
pairs, most frequent first. Words with the same count go in alphabetical order.

Example:
    word_frequencies("the cat saw the dog")
    ->  [("the", 2), ("cat", 1), ("dog", 1), ("saw", 1)]

You'll build this in three steps: make it work, make it handle real text,
then make it fast.
"""


def word_frequencies(text: str) -> list[tuple[str, int]]:
    raise NotImplementedError  # replace this line with your solution


def _reference(text):
    counts = {}
    for raw in text.split():
        word = raw.lower().strip(".,!?;:\"'()")
        if word:
            counts[word] = counts.get(word, 0) + 1
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))


def _book():
    import random
    rng = random.Random(7)
    vocab = ["".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(3, 9))) for _ in range(3000)]
    return " ".join(rng.choice(vocab) for _ in range(200_000))


_BOOK = _book()

STEPS = [
    {
        "title": "Count the words",
        "text": "Split the text on whitespace and count each word. Return (word, count) pairs, "
                "highest count first, ties in alphabetical order. All words here are already lowercase.",
        "hint": "Count with a dict: counts[w] = counts.get(w, 0) + 1. Then "
                "sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])). The minus sign flips the count to descending.",
        "tests": [
            (("the cat saw the dog",), [("the", 2), ("cat", 1), ("dog", 1), ("saw", 1)]),
            (("a b a b a",), [("a", 3), ("b", 2)]),
            (("hello",), [("hello", 1)]),
            (("zebra apple mango",), [("apple", 1), ("mango", 1), ("zebra", 1)]),
        ],
    },
    {
        "title": "Handle real text",
        "text": "Real text has capitals, punctuation and extra spaces. Lowercase every word and strip "
                ".,!?;:\"'() from both ends. Skip anything that ends up empty.",
        "hint": "word.lower().strip(\".,!?;:\\\"'()\") cleans one word. text.split() with no argument "
                "already ignores repeated spaces and newlines.",
        "tests": [
            (("The cat. THE dog!",), [("the", 2), ("cat", 1), ("dog", 1)]),
            (("  (Wait)   wait...  WAIT?  ",), [("wait", 3)]),
            (("",), []),
            (("-- !! --",), [("--", 2)]),
            (("\"Hi,\" she said. \"Hi!\"",), [("hi", 2), ("said", 1), ("she", 1)]),
        ],
    },
    {
        "title": "Make it fast",
        "text": "The last test is a 200,000-word book with 3,000 different words. Calling words.count(w) "
                "for every distinct word rescans the whole book each time. Count everything in a single pass.",
        "hint": "One loop over the words, one dict update each: O(n). collections.Counter does the same in one line. "
                "The final sort is only over distinct words.",
        "tests": [
            (("one fish two fish red fish blue fish",), [("fish", 4), ("blue", 1), ("one", 1), ("red", 1), ("two", 1)]),
            ((_BOOK,), _reference(_BOOK)),
        ],
    },
]
