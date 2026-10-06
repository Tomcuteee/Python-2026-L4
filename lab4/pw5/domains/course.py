# Lớp Môn học — đề pw4 yêu cầu gom các lớp dữ liệu vào package `domains`


class Course:
    """Môn học. `credits` là trọng số dùng khi tính GPA."""

    def __init__(self, cid, name, credits):
        self.cid = cid          # mã môn, dùng làm khoá tra cứu điểm
        self.name = name
        self.credits = credits  # số tín chỉ
