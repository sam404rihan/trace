"""
Number of Atoms                                                               [hard]

A chemical formula is made of:
- elements: an uppercase letter, maybe followed by lowercase letters ("H", "Mg")
- an optional count after an element (no count means 1): "H2", "O"
- groups in parentheses with an optional count after them: "(OH)2"

Groups can be nested. Return the total count of each element as a string: the
elements in alphabetical order, each followed by its count if it's more than 1.

Example:
    count_of_atoms("H2O")             ->  "H2O"
    count_of_atoms("Mg(OH)2")         ->  "H2MgO2"
    count_of_atoms("K4(ON(SO3)2)2")   ->  "K4N2O14S4"

Aim for:  O(n²) at worst (counts get multiplied as groups close); fine for these sizes.
Hint:     Write parse(i) that reads until ")" or the end and returns (Counter, next index).
          On "(" it calls itself, then reads the multiplier after the ")" and multiplies the
          inner Counter into its own. Read an element as uppercase + lowercase*, then digits.
"""


def count_of_atoms(formula: str) -> str:
    raise NotImplementedError  # replace this line with your solution


def _ref(formula):
    import re
    # Expand from the innermost group outwards with regular expressions.
    group = re.compile(r"\(([A-Za-z0-9]*)\)(\d*)")
    while "(" in formula:
        def expand(m):
            times = int(m.group(2) or 1)
            return "".join(el + str(int(n or 1) * times) for el, n in re.findall(r"([A-Z][a-z]*)(\d*)", m.group(1)))
        formula = group.sub(expand, formula)
    counts = {}
    for el, n in re.findall(r"([A-Z][a-z]*)(\d*)", formula):
        counts[el] = counts.get(el, 0) + int(n or 1)
    return "".join(el + (str(c) if c > 1 else "") for el, c in sorted(counts.items()))


def _random_formula(rng, depth):
    parts = []
    for _ in range(rng.randint(1, 3)):
        if depth and rng.random() < 0.35:
            parts.append("(" + _random_formula(rng, depth - 1) + ")" + rng.choice(["", "2", "3", "11"]))
        else:
            parts.append(rng.choice(["H", "He", "C", "O", "Na", "Cl", "Mg", "Uuo"]) + rng.choice(["", "", "2", "7", "10"]))
    return "".join(parts)


def _cases():
    import random
    rng = random.Random(726)
    return [((f,), _ref(f)) for f in (_random_formula(rng, 3) for _ in range(10))]


USES = ["recursion.parse", "recursion.trust"]

TESTS = [
    (("H2O",), "H2O"),
    (("Mg(OH)2",), "H2MgO2"),
    (("K4(ON(SO3)2)2",), "K4N2O14S4"),
    (("Be32",), "Be32"),
    (("H",), "H"),
    (("((N42)24(OB40Li30CHe3O48LiNN26)33(C12Li48N30H13HBe31)21(BHN30Li26BCBe47N40)15(H5)16)14",),
     "B18900Be18984C4200H5446He1386Li33894N50106O22638"),
    (("(H)",), "H"),
    (("((H2O)2)3",), "H12O6"),
] + _cases()
