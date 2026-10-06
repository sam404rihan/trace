def concat_all_words(s: str, words: list[str]) -> list[int]:
    w, k, need = len(words[0]), len(words), Counter(words)
    found = []
    for offset in range(w):                 # pieces starting at offset, offset + w, offset + 2w, ...
        have, left, count = Counter(), offset, 0
        for right in range(offset, len(s) - w + 1, w):
            piece = s[right:right + w]
            if piece not in need:           # no window can contain this piece: start over after it
                have.clear()
                left, count = right + w, 0
                continue
            have[piece] += 1
            count += 1
            while have[piece] > need[piece]:    # too many copies: shrink from the left
                have[s[left:left + w]] -= 1
                left += w
                count -= 1
            if count == k:
                found.append(left)
    return sorted(found)
