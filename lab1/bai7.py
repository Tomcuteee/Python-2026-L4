# ============================================================
# Lab Session 1 - Bai 7: Xoa ky tu dollar ($) khoi chuoi
# ============================================================

def remove_dollar_sign(s: str) -> str:
    """
    Loai bo toan bo ky tu '$' trong chuoi s.

    Args:
        s: chuoi dau vao (vi du "$100").

    Returns:
        Chuoi moi khong con '$' (vi du "100").
    """
    # str.replace se thay THE TOAN BO ky tu '$' bang chuoi rong ''
    return s.replace("$", "")


if __name__ == "__main__":
    # --- Demo 1: vi du co dinh de kiem tra nhanh ---
    print(remove_dollar_sign("$100 and $50"))  # Ky vong: 100 and 50

    # --- Demo 2: nhap tu ban phim (bo comment de dung) ---
    # user_input = input("Enter a string? ")
    # print(remove_dollar_sign(user_input))
