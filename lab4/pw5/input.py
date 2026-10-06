# input.py — module for input (đề pw4).
# Gồm hàm kiểm tra dữ liệu và hàm hỏi để nhập SV / môn / điểm.
# Không import curses ở đây: phần curses thuộc về output.py. Đọc chuỗi qua
# `screen.ask()` để nhập và hiển thị dùng chung một con trỏ.

from domains import Course, Student

# Màn hình hiển thị, do main.py gán vào.
screen = None


# ==================================================================
# KIỂM TRA DỮ LIỆU NGƯỜI DÙNG NHẬP
# ==================================================================

def is_number(s):
    # isdecimal() chứ không isdigit(): isdigit() nhận cả ký tự Unicode
    # kiểu "2" mà int() lại báo lỗi.
    return s.isdecimal()


def is_name(s):
    # Có chữ cái và không phải toàn số. "tom" -> True, "2026" -> False
    return not s.isdecimal() and any(c.isalpha() for c in s)


def is_mark(s):
    # Điểm trong khoảng 0-10. "-5", "11", "tom" -> False
    try:
        return 0 <= float(s) <= 10
    except ValueError:
        return False


def is_dob(s):
    # Ngày sinh d/m/y và có thật. date() tự báo lỗi ngày không tồn tại
    # trong tháng, không cần tự kiểm tra từng tháng.
    try:
        day, month, year = (int(p) for p in s.split("/"))
        from datetime import date
        date(year, month, day)
        return True
    except ValueError:
        return False


def ask(prompt, check=None, error="Giá trị không hợp lệ, thử lại."):
    # Hỏi đến khi dữ liệu đúng. check=None nghĩa là chỉ cần khác rỗng.
    while True:
        s = screen.ask(prompt)
        if not s:
            screen.line("Không được để trống, thử lại.")
        elif check is None or check(s):
            return s
        else:
            screen.line(error)


def ask_count(prompt, max_n=100):
    # Chặn 0 để tránh vòng lặp vô hạn chỗ sau có `for i in range(n)`.
    return int(ask(f"{prompt} (1-{max_n}): ",
                   lambda s: s.isdecimal() and 1 <= int(s) <= max_n,
                   f"Nhập số nguyên từ 1 đến {max_n}."))


# ==================================================================
# CÁC CHỨC NĂNG NHẬP
# ==================================================================

def add_students(students, n):
    # Nhập n sinh viên liên tiếp theo số lượng main.py vừa hỏi.
    for i in range(n):
        add_student(students)


def add_student(students):
    # Mã SV trùng bị chặn: mã là khoá tra cứu điểm, trùng thì ghi đè.
    sid = ask("Mã SV: (ví dụ 203120) ",
              lambda s: is_number(s) and s not in {x.sid for x in students},
              "Mã SV phải là chữ số và không được trùng.")
    students.append(Student(
        sid,
        ask("Họ tên: (ví dụ tom) ", is_name, "Tên phải có chữ cái."),
        ask("Ngày sinh: (ví dụ 24/1/2002) ", is_dob,
            "Ngày sinh phải có dạng d/m/y và là ngày có thật.")))


def add_course(courses):
    # Mã môn trùng bị chặn: mã môn là khoá tra cứu số tín chỉ.
    cid = ask("Mã môn: (ví dụ 234) ",
              lambda s: is_number(s) and s not in courses,
              "Mã môn phải là chữ số và không được trùng.")
    courses[cid] = Course(
        cid,
        ask("Tên môn: (ví dụ lab) "),
        int(ask("Số tín chỉ: (1-10, ví dụ 3) ",
                lambda s: s.isdecimal() and int(s) >= 1,
                "Số tín chỉ phải là số nguyên dương.")))


def enter_marks(students, courses):
    # Chọn một môn rồi nhập điểm cho mọi sinh viên. Điểm được làm tròn ngay.
    cid = ask("Nhập điểm môn nào? (mã môn) ",
              lambda s: s in courses, "Môn học không tồn tại.")
    for s in students:
        s.set_mark(cid, float(ask(f"Điểm {s.name} ({s.sid}): (0-10, ví dụ 8.53 -> 8.5) ",
                                  is_mark, "Điểm từ 0 đến 10, thử lại.")))
    return cid
