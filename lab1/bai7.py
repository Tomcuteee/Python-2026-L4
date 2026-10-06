# Lab Session 1 - Bai 7: Xoa ky tu dollar ($) khoi chuoi
def remove_dollar_sign(s: str) -> str:
    # Bo het ky tu '$': "$100 and $50" -> "100 and 50"
    return s.replace("$", "")


if __name__ == "__main__":
    print(remove_dollar_sign("$100 and $50"))
