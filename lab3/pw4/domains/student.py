# Lớp Sinh viên + GPA có trọng số.

import numpy as np

from .mark import floor1


class Student:
    def __init__(self, sid, name, dob):
        self.sid = sid
        self.name = name
        self.dob = dob
        self.marks = {}                 # {mã môn: điểm} thang 0-10, ví dụ {"234": 8.5}

    def set_mark(self, cid, mark):
        self.marks[cid] = floor1(mark)  # làm tròn ngay lúc ghi

    def gpa(self, courses):
        # GPA = tổng(tín chỉ × điểm) / tổng(tín chỉ)
        # ví dụ 3tc@8.5 + 4tc@9.7 -> (3*8.5 + 4*9.7)/7 = 9.19
        ids = list(self.marks)
        credits = np.array([courses[c].credits for c in ids], dtype=float)
        marks = np.array([self.marks[c] for c in ids], dtype=float)
        if credits.size == 0 or credits.sum() == 0:
            return 0.0
        return float(np.sum(credits * marks) / np.sum(credits))


def sort_by_gpa(students, courses):
    # Xếp GPA giảm dần, trả về danh sách mới.
    return sorted(students, key=lambda s: s.gpa(courses), reverse=True)
