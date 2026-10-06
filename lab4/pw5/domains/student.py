# Lớp Sinh viên và hàm xếp hạng.

import numpy as np

from .mark import floor1


class Student:
    # Mã SV, họ tên, ngày sinh, điểm theo từng môn
    def __init__(self, sid, name, dob):
        self.sid = sid
        self.name = name
        self.dob = dob
        self.marks = {}                 # {mã môn: điểm}, ví dụ {"234": 8.5}

    def set_mark(self, cid, mark):
        self.marks[cid] = floor1(mark)

    def gpa(self, courses):
        # Điểm trung bình có trọng số theo số tín chỉ
        ids = list(self.marks)
        credits = np.array([courses[c].credits for c in ids], dtype=float)
        marks = np.array([self.marks[c] for c in ids], dtype=float)
        if credits.size == 0 or credits.sum() == 0:
            return 0.0
        return float(np.sum(credits * marks) / np.sum(credits))


def sort_by_gpa(students, courses):
    # Xếp GPA giảm dần
    return sorted(students, key=lambda s: s.gpa(courses), reverse=True)
