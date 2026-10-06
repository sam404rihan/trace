def count_of_atoms(formula: str) -> str:
    def read_number(i):
        j = i
        while j < len(formula) and formula[j].isdigit():
            j += 1
        return (int(formula[i:j]) if j > i else 1), j

    def parse(i):
        """Counts from s[i] up to the matching ')' (or the end), and the index of that ')'."""
        counts = Counter()
        while i < len(formula) and formula[i] != ")":
            if formula[i] == "(":
                inner, i = parse(i + 1)
                times, i = read_number(i + 1)       # skip the ')' and read its multiplier
                for el, c in inner.items():
                    counts[el] += c * times
            else:
                j = i + 1
                while j < len(formula) and formula[j].islower():
                    j += 1
                n, k = read_number(j)
                counts[formula[i:j]] += n
                i = k
        return counts, i

    counts, _ = parse(0)
    return "".join(el + (str(c) if c > 1 else "") for el, c in sorted(counts.items()))
