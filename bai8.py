# Lab Session 1 - Bai 8: Lay cac so chan trong list
def extract_even(l):
    return [x for x in l if x % 2 == 0]  # giu so chia het cho 2

if __name__ == "__main__":
    print(extract_even([1, 4, 5, -1, 10]))  # [4, 10]
