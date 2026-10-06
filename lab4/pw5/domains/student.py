# Lớp Sinh viên + GPA có trọng số bằng numpy.array.
# Quy tắc làm tròn điểm nằm ở mark.py.

import numpy as np

from .mark import floor1


class Student:
    # marks = {mã môn: điểm}, ví dụ {"234": 8.5}, thang 0-10

    def __init__(self, sid, name, dob):
        self.sid = sid
        self.name = name
        self.dob = dob
        self.marks = {}                 # rỗng lúc mới tạo, điền dần khi nhập điểm

    def set_mark(self, cid, mark):
        # Làm tròn ngay lúc ghi để mọi đường ghi điểm đều qua cùng quy tắc
        self.marks[cid] = floor1(mark)

    def gpa(self, courses):
        # GPA = tổng(tín chỉ × điểm) / tổng(tín chỉ)
        # ví dụ 3tc@8.5 + 4tc@9.7 -> (3*8.5 + 4*9.7)/7 = 9.19
        ids = list(self.marks)
        credits = np.array([courses[c].credits for c in ids], dtype=float)
        marks = np.array([self.marks[c] for c in ids], dtype=float)
        if credits.size == 0 or credits.sum() == 0:
            return 0.0                     # chưa có điểm: trả 0 để khỏi chia 0
        # `credits * marks` nhân từng phần tử theo đúng vị trí:
        # tín chỉ môn 234 × điểm môn 234, tín chỉ môn 235 × điểm môn 235.
        return float(np.sum(credits * marks) / np.sum(credits))


def sort_by_gpa(students, courses):
    """Xếp GPA giảm dần. Trả về danh sách mới, danh sách cũ không đổi."""
    return sorted(students, key=lambda s: s.gpa(courses), reverse=True)
