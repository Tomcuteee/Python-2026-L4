# storage.py - LƯU VÀ NẠP LẠI DỮ LIỆU (pw5).
# Đề bài: sau khi nhập xong thì ghi students.txt / courses.txt / marks.txt,
# nén cả 3 file đó vào students.dat; khi chạy lại thì nạp từ students.dat.

import os
import zipfile

# Đường dẫn tuyệt đối theo thư mục chứa file này, để chạy script từ bất kỳ
# đâu cũng ghi đúng chỗ, không phụ thuộc thư mục đang đứng.
DIR = os.path.dirname(os.path.abspath(__file__))
FILES = ("students.txt", "courses.txt", "marks.txt")
DAT = os.path.join(DIR, "students.dat")


def _write_txt(students, courses):
    # ponytail: trường tách bằng dấu phẩy nên tên có dấu phẩy sẽ vỡ dòng.
    # Dùng repr/json khi thực tế cần nhập tên lạ.
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


def save(students, courses):
    # ZIP_DEFLATED là phương pháp nén có sẵn trong thư viện chuẩn, không cài
    # thêm gói nào.
    _write_txt(students, courses)
    with zipfile.ZipFile(DAT, "w", zipfile.ZIP_DEFLATED) as z:
        for name in FILES:
            z.write(os.path.join(DIR, name), name)     # arcname: tên phẳng trong .dat


def load():
    # Trả về (students, courses). Chưa có students.dat thì trả về rỗng.
    if not os.path.exists(DAT):
        return [], {}
    from domains import Course, Student

    def rows(zf, name):
        # Bỏ dòng trống cho chắc, phòng khi file kết thúc bằng dòng rỗng.
        return [ln for ln in zf.read(name).decode("utf-8").splitlines() if ln.strip()]

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
            if sid in by_sid:            # SV không có trong students.txt thì bỏ
                by_sid[sid].set_mark(cid, float(m))
    return students, courses
