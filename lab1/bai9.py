# Lab Session 1 - Bai 9: Tinh giai thua
def factorial(n):
    result = 1
    for i in range(2, n + 1):  # 0! = 1! = 1
        result *= i
    return result

if __name__ == "__main__":
    print(factorial(5))  # 120
