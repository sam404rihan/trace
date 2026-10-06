def max_equal_freq(nums: list[int]) -> int:
    count = Counter()       # count[x]: how many times x appears in the prefix
    freq = Counter()        # freq[c]: how many distinct numbers appear exactly c times
    best = top = 0
    for i, x in enumerate(nums, 1):
        if count[x]:
            freq[count[x]] -= 1
        count[x] += 1
        freq[count[x]] += 1
        top = max(top, count[x])
        if (top == 1                                          # all once: drop any one
                or freq[top] * top + 1 == i                   # all top times, plus one single
                or freq[top] == 1 and freq[top - 1] * (top - 1) + top == i):   # one extra copy on top
            best = i
    return best
