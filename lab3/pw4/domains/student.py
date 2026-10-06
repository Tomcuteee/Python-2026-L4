"""
domains/student.py - LỚP SINH VIÊN + GPA

Phần "nghiệp vụ" của bài: tính GPA có trọng số bằng numpy.array.
Quy tắc làm tròn điểm nằm ở mark.py vì dùng chung cho mọi đường ghi điểm.
"""

import numpy as np

from .mark import floor1


class Student:
    """
    Sinh viên. `marks` = {mã môn: điểm}, ví dụ {"234": 8.5}.
    Điểm lưu ở thang 0-10 như đề bài yêu cầu.
    """

    def __init__(self, sid, name, dob):
        self.sid = sid
        self.name = name
        self.dob = dob
        self.marks = {}                 # rỗng lúc mới tạo, điền dần khi nhập điểm

    def set_mark(self, cid, mark):
        """Làm tròn ngay lúc ghi, để mọi đường ghi điểm đều qua cùng quy tắc."""
        self.marks[cid] = floor1(mark)

    def gpa(self, courses):
        """
        GPA = tổng(tín chỉ × điểm) / tổng(tín chỉ).

        Ví dụ môn 3 tín chỉ điểm 8.5 + môn 4 tín chỉ điểm 9.7
            -> (3×8.5 + 4×9.7) / (3+4) = 9.19

        Môn chưa nhập điểm không tính, vì `marks` chỉ chứa môn đã có điểm.
        """
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
