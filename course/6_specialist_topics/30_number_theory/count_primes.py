"""
Count Primes                                                                  [guided]

Return how many prime numbers are strictly less than n.

Example:
    count_primes(10)  ->  4        2, 3, 5, 7
    count_primes(2)   ->  0
"""


def count_primes(n: int) -> int:
    raise NotImplementedError  # replace this line with your solution


_SMALL = [(10, 4), (20, 8), (30, 10), (100, 25), (1000, 168)]

TEACHES = ["nt.sieve"]
USES = []

STEPS = [
    {
        "title": "Make it work",
        "text": "Test each number from 2 to n - 1 for primality and count the primes. A number k is prime when "
                "no d with 2 <= d and d * d <= k divides it.",
        "hint": "def is_prime(k): return k >= 2 and all(k % d for d in range(2, isqrt(k) + 1))",
        "tests": [((n,), want) for n, want in _SMALL],
    },
    {
        "title": "Edges",
        "text": "n = 0, 1, 2 have no primes below them. n = 3 has just one. 0 and 1 are not prime.",
        "hint": "If your loop starts at 2 and the range is empty, the count is already 0.",
        "tests": [((0,), 0), ((1,), 0), ((2,), 0), ((3,), 1), ((5,), 2)],
    },
    {
        "title": "Make it fast: the sieve",
        "text": "n = 3,000,000. Trial division costs up to sqrt(k) per number, around a billion steps here. "
                "The sieve of Eratosthenes flips it around: start with every number marked prime, and for each prime p "
                "cross out p*p, p*p + p, p*p + 2p, … What survives is prime. Total work O(n log log n).",
        "hint": "is_prime = bytearray([1]) * n, then zero out 0 and 1. For p up to isqrt(n - 1): if is_prime[p], "
                "is_prime[p*p::p] = bytes(len(range(p*p, n, p))). Slice assignment does the crossing out in C. "
                "The answer is sum(is_prime).",
        "tests": [((3_000_000,), 216_816), ((1_000_001,), 78_498)],
    },
]
