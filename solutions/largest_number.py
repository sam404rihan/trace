from functools import cmp_to_key


def largest_number(nums: list[int]) -> str:
    # a goes before b when a+b > b+a as strings (e.g. "9"+"30" beats "30"+"9").
    def compare(a, b):
        if a + b > b + a:
            return -1
        if a + b < b + a:
            return 1
        return 0

    digits = sorted(map(str, nums), key=cmp_to_key(compare))
    result = "".join(digits)
    return "0" if result[0] == "0" else result     # [0, 0] -> "0", not "00"
