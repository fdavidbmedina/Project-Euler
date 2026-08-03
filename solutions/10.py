# Summation of Primes
# https://projecteuler.net/problem=10

def sum_primes(limit):
  is_prime = [True] * limit
  is_prime[0] = is_prime[1] = False

  for i in range(2, int(limit ** 0.5) + 1):
    if is_prime[i]:
      for multiple in range(i*i, limit, i):
        is_prime[multiple] = False

  total = sum(i for i in range(limit) if is_prime[i])

  print(total)

sum_primes(2000000)