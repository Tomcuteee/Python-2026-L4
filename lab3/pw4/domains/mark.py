# Hàm làm tròn điểm, mọi đường ghi điểm đều qua đây.

import math


def floor1(x):
    # Làm tròn xuống 1 chữ số: 8.53 -> 8.5
    return math.floor(x * 10 + 1e-9) / 10
