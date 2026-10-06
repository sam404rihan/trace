"""
Text Justification                                                            [hard]

Lay out `words` in lines exactly `width` characters wide. Pack as many words as
fit on each line (with at least one space between them). Then pad each line:

- Spread the extra spaces between the words as evenly as possible. If they
  don't divide evenly, the gaps on the left get one more than the gaps on the right.
- A line with a single word is left-aligned and padded with spaces on the right.
- The last line is left-aligned: single spaces between words, padding on the right.

Every word is at most `width` characters long.

Example:
    text_justify(["This", "is", "an", "example", "of", "text", "justification."], 16)
        ->  ["This    is    an",
             "example  of text",
             "justification.  "]

Aim for:  O(total characters). One pass to group words into lines, then build each line.
Hint:     A line takes words while letters so far + spaces so far + 1 + next word <= width.
          For a middle line: gaps = words - 1, spaces = width - letters, and
          divmod(spaces, gaps) gives the base gap and how many left gaps get one extra.
"""


def text_justify(words: list[str], width: int) -> list[str]:
    raise NotImplementedError  # replace this line with your solution


def _ref(words, width):
    lines, cur = [], []
    for w in words:
        if cur and len(" ".join(cur + [w])) > width:
            lines.append(cur)
            cur = []
        cur.append(w)
    lines.append(cur)
    out = []
    for i, line in enumerate(lines):
        if i == len(lines) - 1 or len(line) == 1:
            out.append(" ".join(line).ljust(width))
            continue
        spaces = width - sum(map(len, line))
        text = ""
        for j, w in enumerate(line[:-1]):
            gap = spaces // (len(line) - 1) + (1 if j < spaces % (len(line) - 1) else 0)
            text += w + " " * gap
        out.append(text + line[-1])
    return out


def _cases():
    import random
    rng = random.Random(1001)
    out = []
    for _ in range(8):
        width = rng.randint(6, 24)
        words = ["".join(rng.choice("abcdefgh") for _ in range(rng.randint(1, min(width, 9))))
                 for _ in range(rng.randint(1, 14))]
        out.append(((words, width), _ref(words, width)))
    return out


TESTS = [
    ((["This", "is", "an", "example", "of", "text", "justification."], 16),
     ["This    is    an", "example  of text", "justification.  "]),
    ((["What", "must", "be", "acknowledgment", "shall", "be"], 16),
     ["What   must   be", "acknowledgment  ", "shall be        "]),
    ((["Science", "is", "what", "we", "understand", "well", "enough", "to", "explain", "to", "a", "computer.",
       "Art", "is", "everything", "else", "we", "do"], 20),
     ["Science  is  what we", "understand      well", "enough to explain to", "a  computer.  Art is",
      "everything  else  we", "do                  "]),
    ((["a"], 1), ["a"]),
    ((["a", "b", "c", "d", "e"], 3), ["a b", "c d", "e  "]),
    ((["hello"], 8), ["hello   "]),
] + _cases()
