# 10 001st prime
# https://projecteuler.net/problem=7
import math

def nth_prime(n):
    # Estimate upper bound using Prime Number Theorem
    if n < 6:
        limit = 15
    else:
        limit = int(n * (math.log(n) + math.log(math.log(n)))) + 10

    # Sieve of Eratosthenes
    sieve = bytearray([1]) * (limit + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit + 1, i):
                sieve[j] = 0

    primes = [i for i, is_p in enumerate(sieve) if is_p]
    return primes[n-1]

print(nth_prime(10001))

#Test