"""
# Digit DP and DP speed-ups

Two ways to make dynamic programming reach much bigger inputs.

## Digit DP
"How many numbers from 1 to N have property P?" with N up to 10^18. You can't loop to
N, but you can build the numbers digit by digit, left to right, and count the choices.
The state is (position, tight, ...whatever P needs), where tight means "every digit so
far equals N's digit", so the next digit can be at most N's digit there. Otherwise it
can be anything 0-9.

    count(i, tight, state):
        if i == len(digits): return 1 if state is good else 0
        top = digits[i] if tight else 9
        return sum(count(i + 1, tight and d == top, step(state, d)) for d in 0..top)

Memoise it. The number of states is tiny (19 positions × 2 × the size of the state).
Ranges [lo, hi] = count(hi) - count(lo - 1). Leading zeros need a "started" flag when
they would change the answer (e.g. "contains no 0").

## Use it when
- Counting numbers up to a huge N with a digit-based property: digit sums, forbidden
  digits, how many times a digit appears, no two equal neighbours

## Sliding-window maximum inside a DP
dp[i] = nums[i] + max(dp[i - k .. i - 1]) costs O(k) per step if you scan the window.
A monotonic deque holds indices with decreasing dp values: the front is the window's
max, pop the front when it falls out of the window, and pop the back while it is
<= the new value. O(n) in total.

## Common mistakes
- Forgetting the tight flag, which counts numbers bigger than N
- Treating leading zeros as real digits
- Memoising on tight=True states (harmless but useless: there's only one tight path)
- Storing dp values in the deque instead of indices (you can't tell when they expire)
"""


def count_digit_sum(n, target):
    digits = list(map(int, str(n)))

    @cache
    def go(i, tight, total):
        if total > target:
            return 0
        if i == len(digits):
            return 1 if total == target else 0
        top = digits[i] if tight else 9
        return sum(go(i + 1, tight and d == top, total + d) for d in range(top + 1))
    return go(0, True, 0)


print("numbers in 0..1000 with digit sum 10:", count_digit_sum(1000, 10),
      " check:", sum(1 for x in range(1001) if sum(map(int, str(x))) == 10))
print("numbers up to 10^18 with digit sum 10:", count_digit_sum(10**18, 10))


def max_jump_score(nums, k):
    dp, window = [0] * len(nums), deque()
    for i, x in enumerate(nums):
        if window and window[0] < i - k:
            window.popleft()                     # out of reach
        dp[i] = x + (dp[window[0]] if window else 0)
        while window and dp[window[-1]] <= dp[i]:
            window.pop()                         # never the max again
        window.append(i)
    return dp[-1]


print("jump game VI on [1, -1, -2, 4, -7, 3], k = 2:", max_jump_score([1, -1, -2, 4, -7, 3], 2))
