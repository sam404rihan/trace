ONES = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve",
        "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
SCALES = ["", "Thousand", "Million", "Billion"]


def number_to_words(num: int) -> str:
    if num == 0:
        return "Zero"

    def below_1000(n):
        words = []
        if n >= 100:
            words += [ONES[n // 100], "Hundred"]
            n %= 100
        if n >= 20:
            words.append(TENS[n // 10])
            n %= 10
        if n:
            words.append(ONES[n])           # 1..19 are single words
        return words

    words, scale = [], 0
    while num:
        num, group = divmod(num, 1000)
        if group:                           # skip empty groups: no "Million Thousand"
            words = below_1000(group) + ([SCALES[scale]] if scale else []) + words
        scale += 1
    return " ".join(words)
