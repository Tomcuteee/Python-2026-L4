# Kiểm tra dữ liệu và các hàm nhập sinh viên / môn học / điểm.

from datetime import date

from domains import Course, Student

screen = None                          # main.py gán vào


# --- kiểm tra dữ liệu ---

def is_number(s):
    return s.isdecimal()


def is_name(s):
    return not s.isdecimal() and any(c.isalpha() for c in s)


def is_mark(s):
    # Điểm trong khoảng 0-10
    try:
        return 0 <= float(s) <= 10
    except ValueError:
        return False


def is_dob(s):
    # Ngày sinh d/m/y, ví dụ 24/1/2002
    try:
        d, m, y = (int(p) for p in s.split("/"))
        date(y, m, d)
        return True
    except ValueError:
        return False


def ask(prompt, check=None, error="Giá trị không hợp lệ, thử lại."):
    # Hỏi đến khi dữ liệu đúng, rồi trả về
    while True:
        s = screen.ask(prompt)
        if not s:
            screen.line("Không được để trống, thử lại.")
        elif check is None or check(s):
            return s
        else:
            screen.line(error)


def ask_count(prompt, max_n=100):
    # Hỏi số lượng, chặn giá trị 0
    return int(ask(f"{prompt} (1-{max_n}): ",
                   lambda s: s.isdecimal() and 1 <= int(s) <= max_n,
                   f"Nhập số nguyên từ 1 đến {max_n}."))


# --- nhập liệu ---

def add_students(students, n):
    for _ in range(n):
        add_student(students)


def add_student(students):
    sid = ask("Mã SV: (ví dụ 203120) ",
              lambda s: is_number(s) and s not in {x.sid for x in students},
              "Mã SV phải là chữ số và không được trùng.")
    students.append(Student(
        sid,
        ask("Họ tên: (ví dụ tom) ", is_name, "Tên phải có chữ cái."),
        ask("Ngày sinh: (ví dụ 24/1/2002) ", is_dob,
            "Ngày sinh phải có dạng d/m/y và là ngày có thật.")))


def add_course(courses):
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
    # Nhập điểm của một môn cho mọi sinh viên, trả về mã môn vừa nhập
    cid = ask("Nhập điểm môn nào? (mã môn) ",
              lambda s: s in courses, "Môn học không tồn tại.")
    for s in students:
        s.set_mark(cid, float(ask(f"Điểm {s.name} ({s.sid}): (0-10, ví dụ 8.53 -> 8.5) ",
                                  is_mark, "Điểm từ 0 đến 10, thử lại.")))
    return cid
