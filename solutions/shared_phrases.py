def shared_phrases(doc_a: str, doc_b: str, k: int) -> list[str]:
    words_a = re.findall(r"[a-z0-9]+", doc_a.lower())
    words_b = re.findall(r"[a-z0-9]+", doc_b.lower())
    in_b = {tuple(words_b[i:i + k]) for i in range(len(words_b) - k + 1)}   # every phrase of b, hashed
    out, seen = [], set()
    for i in range(len(words_a) - k + 1):
        phrase = tuple(words_a[i:i + k])
        if phrase in in_b and phrase not in seen:
            seen.add(phrase)
            out.append(" ".join(phrase))
    return out
