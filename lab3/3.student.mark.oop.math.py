# Quản lý điểm sinh viên: làm tròn điểm, GPA có trọng số, xếp hạng, giao diện curses.
# Chạy:  python "3.student.mark.oop.math.py" [--test]

import math
import sys
from datetime import date

import numpy as np

try:
    import curses                     # Windows: pip install windows-curses
except ImportError:
    curses = None

try:
    sys.stdout.reconfigure(encoding="utf-8")    # console Windows là cp1252
except (AttributeError, ValueError):
    pass


# --- kiểm tra dữ liệu người dùng nhập ---

def floor1(x):
    # Điểm làm tròn xuống 1 chữ số: 8.53 -> 8.5
    return math.floor(x * 10 + 1e-9) / 10


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


# --- lớp đối tượng ---

class Course:
    # Môn học: mã, tên, số tín chỉ
    def __init__(self, cid, name, credits):
        self.cid = cid
        self.name = name
        self.credits = credits


class Student:
    # Sinh viên: mã, họ tên, ngày sinh, điểm theo từng môn
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


# --- giao diện ---

def _cursor(visible):
    try:
        curses.curs_set(1 if visible else 0)
    except curses.error:
        pass


class Screen:
    # Bọc curses. win=None thì in ra màn hình bình thường.
    def __init__(self, win):
        self.w = win
        self.row = 1                   # dòng đang in, dòng 0 dành cho tiêu đề

    def clear(self):
        self.row = 1
        if self.w:
            self.w.erase()

    def line(self, text=""):
        # In xuống dòng kế tiếp, dòng h-1 dành cho câu hỏi nhập
        if not self.w:
            print(text)
            return
        h, w = self.w.getmaxyx()
        for part in str(text).split("\n"):
            if self.row >= h - 1:
                break
            self.w.addstr(self.row, 0, part[:w - 1])
            self.w.clrtoeol()
            self.row += 1
        self.w.refresh()

    def title(self, text):
        # In tiêu đề căn giữa ở dòng 0
        if not self.w:
            print(text)
            return
        _, w = self.w.getmaxyx()
        self.w.addstr(0, 0, text.center(w - 1), curses.A_BOLD)

    def ask(self, prompt):
        # Hỏi ở dòng cuối, trả về chuỗi đã bỏ khoảng trắng
        if not self.w:
            return input(prompt)
        h, w = self.w.getmaxyx()
        self.w.addstr(h - 1, 0, prompt[:w - 1])
        self.w.clrtoeol()
        self.w.refresh()
        _cursor(1)
        curses.echo()
        try:
            return self.w.getstr(h - 1, 0, w - 2).decode("utf-8", "ignore").strip()
        finally:
            curses.noecho()
            _cursor(0)


screen = Screen(None)                  # run() thay bằng màn hình curses thật


def table(headers, rows):
    # Bảng căn cột, trả về danh sách dòng chuỗi
    if not rows:
        return ["(chưa có dữ liệu)"]
    w = [max([len(str(h))] + [len(str(r[i])) for r in rows])
         for i, h in enumerate(headers)]
    return (["  ".join(str(h).ljust(x) for h, x in zip(headers, w)),
             "  ".join("-" * x for x in w)]
            + ["  ".join(str(c).ljust(x) for c, x in zip(r, w)) for r in rows])


# --- nhập liệu ---

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
    # Nhập điểm của một môn cho mọi sinh viên, rồi in bảng điểm
    cid = ask("Nhập điểm môn nào? (mã môn) ",
              lambda s: s in courses, "Môn học không tồn tại.")
    for s in students:
        s.set_mark(cid, float(ask(f"Điểm {s.name} ({s.sid}): (0-10, ví dụ 8.53 -> 8.5) ",
                                  is_mark, "Điểm từ 0 đến 10, thử lại.")))
    for r in table(["Mã SV", "Họ tên", "Điểm"],
                   [[s.sid, s.name, s.marks[cid]] for s in students]):
        screen.line(r)


def show_gpa(students, courses):
    # In bảng sinh viên xếp hạng theo GPA
    screen.line()
    for r in table(["Mã SV", "Họ tên", "GPA"],
                   [[s.sid, s.name, f"{s.gpa(courses):.2f}"]
                    for s in sort_by_gpa(students, courses)]):
        screen.line(r)


# --- chương trình chính ---

MENU = """
  1. Thêm sinh viên        4. Xếp hạng theo GPA
  2. Thêm môn học          5. Xem sinh viên
  3. Nhập điểm             0. Thoát
"""

EMPTY = "Cần có sinh viên và môn học trước."


def run(stdscr):
    global screen
    screen = Screen(stdscr)

    students, courses = [], {}         # list[Student] và {mã môn: Course}
    try:
        while True:
            screen.clear()
            screen.title("QUẢN LÝ ĐIỂM SINH VIÊN")
            screen.line(MENU)

            c = screen.ask("Chọn: ")
            if c == "0":
                return
            elif c == "1":
                add_student(students)
            elif c == "2":
                add_course(courses)
            elif c == "3":
                if students and courses:
                    enter_marks(students, courses)
                else:
                    screen.line(EMPTY)
            elif c == "4":
                if students and courses:
                    show_gpa(students, courses)
                else:
                    screen.line(EMPTY)
            elif c == "5":
                for r in table(["Mã SV", "Họ tên", "Ngày sinh"],
                               [[s.sid, s.name, s.dob] for s in students]):
                    screen.line(r)
            else:
                screen.line("Lựa chọn không hợp lệ, thử lại.")
    except (KeyboardInterrupt, EOFError):
        screen.line("\nKết thúc.")


def main():
    if curses is None or not sys.stdout.isatty():
        run(None)
    else:
        curses.wrapper(run)


def _test():
    # Chạy: python "3.student.mark.oop.math.py" --test
    assert [floor1(x) for x in (8.53, 7.29, 7.3, 9.0, 0.04)] == [8.5, 7.2, 7.3, 9.0, 0.0]
    assert is_mark("8.53") and not is_mark("11") and not is_mark("tom")
    assert is_dob("24/1/2002") and not is_dob("30/2/2002")

    cs = {"234": Course("234", "Đại số tuyến tính", 3),
          "235": Course("235", "Python", 4)}

    s = Student("1", "tom", "24/1/2002")
    assert s.gpa(cs) == 0.0
    s.set_mark("234", 9.0)
    s.set_mark("235", 8.0)
    assert abs(s.gpa(cs) - 59 / 7) < 1e-9

    v, w = Student("v", "v", "1/1/2000"), Student("w", "w", "1/1/2000")
    v.set_mark("234", 9.0), v.set_mark("235", 10.0)
    w.set_mark("234", 10.0), w.set_mark("235", 9.0)
    assert sort_by_gpa([w, v], cs) == [v, w]

    s.marks.clear()
    s.set_mark("234", 8.53)
    assert s.marks["234"] == 8.5

    print("OK: làm tròn, kiểm tra dữ liệu, GPA, xếp hạng")


if __name__ == "__main__":
    _test() if "--test" in sys.argv else main()
