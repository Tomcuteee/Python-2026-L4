# Lab Session 1 - Bai 4: Kiem tra so hoan hao
def is_perfect(n):
    if n <= 1:
        return False
    total = sum(i for i in range(1, n // 2 + 1) if n % i == 0)  # tong uoc < n
    return total == n

n = int(input("Enter a number? "))
print(f"{n} is a perfect number" if is_perfect(n) else f"{n} is a NOT perfect number")
