r"""
# Tries (prefix trees)

A trie stores words letter by letter, sharing common beginnings. Looking up a
word or prefix costs O(length of the word), no matter how many words you store.

```
 car, cart, cat, dog

      (root)
      /    \
     c      d
     a      o
    / \     g*
   r*  t*
   t*               * = a word ends here
```

## Use it when
- "starts with", "prefix", "autocomplete", "dictionary of words"
- Many words share prefixes and you query prefixes a lot
- Word search on a grid with many target words

## The dict-of-dicts shortcut
A trie node is just a dict from letter to child node. Mark word ends with a
special key:
```
root = {}
for word in words:
    node = root
    for ch in word:
        node = node.setdefault(ch, {})
    node["$"] = True             # a word ends here
```
Need counts? Store `node["#"] = node.get("#", 0) + 1` at each step to know how
many words pass through that prefix.

## Search
```
node = root
for ch in prefix:
    if ch not in node: return False
    node = node[ch]
return True                      # for a whole word: return "$" in node
```

## Common mistakes
- Treating a prefix as a word. "car" being on the path to "cart" doesn't make
  it a word; check the end marker
- Choosing a marker that could also be a letter. Use something like "$"

Press Run to build a trie and autocomplete from it.
"""
import json

words = ["car", "cart", "cat", "care", "dog", "dot"]
root = {}
for word in words:
    node = root
    for ch in word:
        node = node.setdefault(ch, {})
        node["#"] = node.get("#", 0) + 1     # how many words pass through here
    node["$"] = True

print("the 'do' branch:", json.dumps(root["d"]["o"]))


def find(prefix):
    node = root
    for ch in prefix:
        if ch not in node:
            return None
        node = node[ch]
    return node


def autocomplete(prefix):
    node = find(prefix)
    found = []

    def collect(node, path):
        if "$" in node:
            found.append(path)
        for ch in sorted(k for k in node if k not in "$#"):
            collect(node[ch], path + ch)

    if node:
        collect(node, prefix)
    return found


for prefix in ["ca", "car", "do", "x"]:
    node = find(prefix)
    print(f"{prefix!r}: {node['#'] if node else 0} words start with it -> {autocomplete(prefix)}")
print("'car' is a word:", "$" in find("car"), "   'ca' is a word:", "$" in find("ca"))
