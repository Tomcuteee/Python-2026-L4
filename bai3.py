# Lab Session 1 - Bai 3: Kiem tra so nguyen to
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):  # chi can check den sqrt(n)
        if n % i == 0:
            return False
    return True

n = int(input("Enter a number? "))
print(f"{n} is a prime number" if is_prime(n) else f"{n} is a NOT prime number")
