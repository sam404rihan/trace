"""
# Bit tricks

Every integer is a row of bits. A handful of bit operations solve some
problems in O(1) space with one line. You only need a few.

## The operators
- `a & b`: 1 where both have a 1 (AND)
- `a | b`: 1 where either has a 1 (OR)
- `a ^ b`: 1 where they differ (XOR)
- `x << k`: shift left, same as `x * 2**k`; `x >> k`: shift right, like `x // 2**k`
- `bin(x)` shows the bits; `x.bit_count()` counts the 1s (Python 3.10+)

## The tricks worth memorising
- `x & 1`: is x odd?
- `x & (x - 1)`: removes the lowest 1 bit. So `x > 0 and x & (x - 1) == 0` means "x is a power of two"
- `x & -x`: keeps only the lowest 1 bit
- `x ^ x == 0` and `x ^ 0 == x`: XOR all numbers and pairs cancel out,
  leaving the one without a partner
- `(x >> i) & 1`: bit i of x. `x | (1 << i)` sets it; `x & ~(1 << i)` clears it
- **Subsets as bitmasks:** for n items, the numbers 0 .. 2ⁿ - 1 are all the
  subsets; bit i says whether item i is in

## When to use them
- "Every element appears twice except one": XOR
- Counting bits, powers of two, "Hamming distance": `bin(a ^ b).count("1")`
- Small sets (n ≤ 20) as a single integer, e.g. in DP over subsets

## Common mistakes
- Operator precedence: `x & 1 == 0` means `x & (1 == 0)`. Write `(x & 1) == 0`
- Python ints never overflow, and negatives behave as if they had infinite 1s
  on the left. Tricks that rely on 32-bit wraparound need `& 0xFFFFFFFF`

Press Run to see the tricks on real numbers.
"""
for x in [12, 16, 7]:
    print(f"x={x:>2}  bits={bin(x):>7}  odd={bool(x & 1)!s:<5}  "
          f"drop lowest 1: {bin(x & (x - 1)):>7}  power of two: {x > 0 and x & (x - 1) == 0}")

nums = [4, 1, 2, 1, 2]
single = 0
for n in nums:
    single ^= n
print("\nXOR of", nums, "=", single, "(the pairs cancel)")

print("bit counts 0..8:", [n.bit_count() for n in range(9)])

items = ["a", "b", "c"]
print("\nall subsets via bitmasks:")
for mask in range(1 << len(items)):
    subset = [items[i] for i in range(len(items)) if (mask >> i) & 1]
    print(f"  {mask:03b} -> {subset}")
