# Lab Session 1 - Bai 11: Khoang cach 2 diem
import math

def calculate_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

if __name__ == "__main__":
    print(calculate_distance((0, 0), (3, 4)))  # 5.0
