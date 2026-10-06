# Lab Session 1 - Bai 12: In hinh chu nhat rong m x n
def print_pattern(m, n):
    for i in range(m):
        row = []
        for j in range(n):
            # vien ngoai in *, ben trong in khoang trang
            row.append("*" if i in (0, m - 1) or j in (0, n - 1) else " ")
        print(" ".join(row))

if __name__ == "__main__":
    print_pattern(4, 5)
