"""
Integer to English Words                                                      [hard]

Write a non-negative integer below 2**31 in English words, with each word
capitalized and single spaces between words. No "and", no hyphens, no commas.

Example:
    number_to_words(123)          ->  "One Hundred Twenty Three"
    number_to_words(12345)        ->  "Twelve Thousand Three Hundred Forty Five"
    number_to_words(1_000_010)    ->  "One Million Ten"
    number_to_words(0)            ->  "Zero"

Aim for:  O(number of digits). Handle three digits at a time.
Hint:     Write one helper for 0..999 (hundreds, then 1..19 as single words, then tens and ones).
          Then walk the groups with the scales ["", "Thousand", "Million", "Billion"], skipping
          groups that are 0 so 1_000_000 doesn't become "One Million Thousand".
"""


def number_to_words(num: int) -> str:
    raise NotImplementedError  # replace this line with your solution


TESTS = [
    ((0,), "Zero"),
    ((5,), "Five"),
    ((13,), "Thirteen"),
    ((20,), "Twenty"),
    ((99,), "Ninety Nine"),
    ((100,), "One Hundred"),
    ((101,), "One Hundred One"),
    ((123,), "One Hundred Twenty Three"),
    ((1000,), "One Thousand"),
    ((12345,), "Twelve Thousand Three Hundred Forty Five"),
    ((50_868,), "Fifty Thousand Eight Hundred Sixty Eight"),
    ((1_000_010,), "One Million Ten"),
    ((7_011_000,), "Seven Million Eleven Thousand"),
    ((100_000_017,), "One Hundred Million Seventeen"),
    ((1_234_567,), "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"),
    ((1_000_000_000,), "One Billion"),
    ((2_147_483_647,),
     "Two Billion One Hundred Forty Seven Million Four Hundred Eighty Three Thousand Six Hundred Forty Seven"),
]
