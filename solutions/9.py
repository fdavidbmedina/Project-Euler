# Special Pythagorean Triplet
# https://projecteuler.net/problem=9    

def find_special_pythagorean_triplet(sum_value):
    for a in range(1, sum_value // 3):
        numerator = sum_value * (sum_value - 2 * a)
        denominator = 2 * (sum_value - a)
        if numerator % denominator == 0:
            b = numerator // denominator
            c = sum_value - a - b
            if a < b < c:
                return a, b, c
    return None

triplet = find_special_pythagorean_triplet(1000)
if triplet:
    a, b, c = triplet
    product = a * b * c
    print(product)
