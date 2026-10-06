# Lab Session 1 - Bai 10: Liet ke uoc so
def get_divisors(n):
    return [i for i in range(1, n + 1) if n % i == 0]

if __name__ == "__main__":
    print(get_divisors(12))  # [1, 2, 3, 4, 6, 12]
