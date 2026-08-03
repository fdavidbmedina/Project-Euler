# Summation of Primes
# https://projecteuler.net/problem=10

def sum_primes(limit):
  is_prime = [True] * limit # list of all numbers
  is_prime[0] = is_prime[1] = False

  for i in range(2, int(limit ** 0.5) + 1): # 2 to closest int sqr of limit + 1
    if is_prime[i]: # check if current number is still not checked if prime
      for multiple in range(i*i, limit, i): # check for multiples to not run through every single number
        is_prime[multiple] = False # change to false

  total = sum(i for i in range(limit) if is_prime[i])

  print(total)

sum_primes(2000000)