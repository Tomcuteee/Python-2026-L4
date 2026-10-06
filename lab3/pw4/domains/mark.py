"""
domains/mark.py - QUY TẮC LÀM TRÒN ĐIỂM

Tách riêng vì đây là quy tắc nghiệp vụ dùng chung: ai ghi điểm — nhập tay,
đọc từ file, hay sửa lại — đều phải đi qua cùng một hàm.
"""

import math


def floor1(x):
    """
    Làm tròn xuống còn 1 chữ số thập phân:  8.53 -> 8.5,  7.29 -> 7.2

    Cộng 1e-9 trước khi floor để bù lỗi số thực: 7.3*10 ra 72.99999999999999,
    không có 1e-9 thì floor ra 72, chia 10 ra 7.2 — sai, trong khi người
    dùng gõ 7.3 thì phải giữ 7.3.
    """
    return math.floor(x * 10 + 1e-9) / 10
