# storage.py - ghi 3 file txt rồi nén vào students.dat, và nạp lại khi chạy.
# Đường dẫn tuyệt đối theo thư mục chứa file này để chạy từ đâu cũng ghi đúng chỗ.

import os
import zipfile

from domains import Course, Student

DIR = os.path.dirname(os.path.abspath(__file__))
FILES = ("students.txt", "courses.txt", "marks.txt")
DAT = os.path.join(DIR, "students.dat")


def save(students, courses):
    # ponytail: tên chứa dấu phẩy sẽ vỡ dòng. Dùng repr/json khi cần nhập tên lạ.
    with open(os.path.join(DIR, "students.txt"), "w", encoding="utf-8") as f:
        for s in students:
            f.write(f"{s.sid},{s.name},{s.dob}\n")
    with open(os.path.join(DIR, "courses.txt"), "w", encoding="utf-8") as f:
        for c in courses.values():
            f.write(f"{c.cid},{c.name},{c.credits}\n")
    with open(os.path.join(DIR, "marks.txt"), "w", encoding="utf-8") as f:
        for s in students:
            for cid, m in s.marks.items():
                f.write(f"{s.sid},{cid},{m}\n")

    with zipfile.ZipFile(DAT, "w", zipfile.ZIP_DEFLATED) as z:
        for name in FILES:
            z.write(os.path.join(DIR, name), name)


def load():
    # Trả về (students, courses). Chưa có students.dat thì trả về rỗng.
    if not os.path.exists(DAT):
        return [], {}

    def rows(z, name):
        # Bỏ dòng trống phòng khi file kết thúc bằng dòng rỗng.
        return [ln for ln in z.read(name).decode("utf-8").splitlines() if ln.strip()]

    students, courses = [], {}
    with zipfile.ZipFile(DAT) as z:
        for ln in rows(z, "students.txt"):
            sid, name, dob = ln.split(",")
            students.append(Student(sid, name, dob))
        for ln in rows(z, "courses.txt"):
            cid, name, credits = ln.split(",")
            courses[cid] = Course(cid, name, int(credits))

        by_sid = {s.sid: s for s in students}
        for ln in rows(z, "marks.txt"):
            sid, cid, m = ln.split(",")
            if sid in by_sid:                        # SV không có trong students.txt thì bỏ
                by_sid[sid].set_mark(cid, float(m))
    return students, courses
