# Lab Session 1 - Bai 7: Xoa dau $ trong chuoi
def remove_dollar_sign(s):
    return s.replace("$", "")  # thay $ bang chuoi rong

if __name__ == "__main__":
    print(remove_dollar_sign("$100 and $50"))  # 100 and 50
