# Quy tắc làm tròn điểm — tách riêng vì mọi đường ghi điểm đều phải qua
# cùng một hàm này.

import math


def floor1(x):
    # 8.53 -> 8.5, 7.29 -> 7.2. Cộng 1e-9 để bù lỗi số thực: 7.3*10 ra
    # 72.99999999999999, không có 1e-9 thì floor ra 72 -> 7.2, sai.
    return math.floor(x * 10 + 1e-9) / 10
