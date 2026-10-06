# Lớp Môn học.


class Course:
    def __init__(self, cid, name, credits):
        self.cid = cid          # mã môn, dùng làm khoá tra cứu điểm
        self.name = name
        self.credits = credits  # số tín chỉ, là trọng số khi tính GPA
