def plus_one(digits: list[int]) -> list[int]:
    digits = digits[:]
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1              # no carry: done
            return digits
        digits[i] = 0                   # 9 + 1 = 10: write 0, carry left
    return [1] + digits                 # every digit was 9
