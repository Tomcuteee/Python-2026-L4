# BÀI 3 - QUẢN LÝ ĐIỂM SINH VIÊN
# Practical work 3 (slide 18/19): lấy bài 2 rồi thêm 4 thứ
#   - math.floor()  : làm tròn xuống 1 chữ số thập phân ngay khi nhập điểm
#   - numpy.array() : GPA có trọng số = tổng(tín chỉ × điểm) / tổng(tín chỉ)
#   - sắp xếp        : danh sách sinh viên theo GPA giảm dần
#   - curses         : giao diện tiêu đề + menu, xóa sạch màn hình mỗi vòng lặp
# Chạy:  python "3.student.mark.oop.math.py" [--test]

import math
import sys
from datetime import date

import numpy as np

try:
    import curses                     # Windows: pip install windows-curses
except ImportError:
    curses = None                     # không có curses thì chạy bản in thường

try:
    sys.stdout.reconfigure(encoding="utf-8")    # console Windows là cp1252
except (AttributeError, ValueError):
    pass


# ==================================================================
# KIỂM TRA DỮ LIỆU NGƯỜI DÙNG NHẬP
# ==================================================================

def floor1(x):
    # Làm tròn xuống còn 1 chữ số thập phân: 8.53 -> 8.5, 7.29 -> 7.2.
    # Cộng 1e-9 trước khi floor để bù lỗi số thực: 7.3*10 ra 72.99999999999999,
    # không có 1e-9 thì floor ra 72, chia 10 ra 7.2 — sai.
    return math.floor(x * 10 + 1e-9) / 10


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
        date(year, month, day)
        return True
    except ValueError:
        return False


def ask(prompt, check=None, error="Giá trị không hợp lệ, thử lại."):
    # Hỏi đến khi dữ liệu đúng. check=None nghĩa là chỉ cần khác rỗng.
    # Đọc qua `screen` chứ không gọi input() trực tiếp: khi curses đang bật,
    # input() in câu hỏi ra ngoài màn hình curses rồi bị curses ghi đè mất.
    while True:
        s = screen.ask(prompt)
        if not s:
            screen.line("Không được để trống, thử lại.")
        elif check is None or check(s):
            return s
        else:
            screen.line(error)


# ==================================================================
# LỚP ĐỐI TƯỢNG
# ==================================================================

class Course:
    """Môn học. `credits` là trọng số dùng khi tính GPA."""

    def __init__(self, cid, name, credits):
        self.cid = cid
        self.name = name
        self.credits = credits


class Student:
    # Sinh viên. `marks` = {mã môn: điểm}, ví dụ {"234": 8.5}, thang 0-10.

    def __init__(self, sid, name, dob):
        self.sid = sid
        self.name = name
        self.dob = dob
        self.marks = {}                 # rỗng lúc mới tạo, điền dần khi nhập điểm

    def set_mark(self, cid, mark):
        # Làm tròn ngay lúc ghi để mọi đường ghi điểm đều qua cùng quy tắc
        self.marks[cid] = floor1(mark)

    def gpa(self, courses):
        # GPA = tổng(tín chỉ × điểm) / tổng(tín chỉ)
        # ví dụ 3tc@8.5 + 4tc@9.7 -> (3*8.5 + 4*9.7)/7 = 9.19
        # Môn chưa nhập điểm không tính, vì `marks` chỉ chứa môn đã có điểm.
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


# ==================================================================
# GIAO DIỆN CURSES
# ==================================================================

def _cursor(visible):
    # Nhiều terminal không hỗ trợ curs_set() và báo lỗi, nhưng việc này không
    # quan trọng nên bỏ qua lỗi.
    try:
        curses.curs_set(1 if visible else 0)
    except curses.error:
        pass


class Screen:
    # Bọc curses. Truyền None thì mọi lệnh vẽ in ra màn hình bình thường,
    # nên chương trình vẫn chạy được trên máy không cài curses.

    def __init__(self, win):
        self.w = win
        self.row = 1                      # dòng 0 dành cho tiêu đề

    def clear(self):
        self.row = 1
        if self.w:
            self.w.erase()

    def line(self, text=""):
        # In nội dung xuống dòng kế tiếp. Chuỗi có \n thì in nhiều dòng.
        # Cần bộ đếm `row` vì curses KHÔNG tự cuộn màn hình: cứ in vào dòng
        # cuối thì dòng mới sẽ đè dòng cũ.
        if not self.w:
            print(text)
            return
        h, w = self.w.getmaxyx()
        for part in str(text).split("\n"):
            if self.row >= h - 1:         # dòng cuối dành cho câu hỏi nhập
                break
            self.w.addstr(self.row, 0, part[:w - 1])    # cắt w-1: chạm cột cuối sẽ vượt biên
            self.w.clrtoeol()                            # xóa phần cũ còn sót của dòng
            self.row += 1
        self.w.refresh()

    def title(self, text):
        if not self.w:
            print(text)
            return
        _, w = self.w.getmaxyx()
        self.w.addstr(0, 0, text.center(w - 1), curses.A_BOLD)

    def ask(self, prompt):
        # Câu hỏi ở dòng cuối, trả về chuỗi đã bỏ khoảng trắng thừa.
        # Dùng window.getstr() chứ không curses.instr(): bản windows-curses
        # không có instr(). getstr() chỉ đọc được khi echo đang bật.
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
        finally:                           # finally để Ctrl+C cũng trả
            curses.noecho()                # con trỏ và echo về đúng trạng thái
            _cursor(0)


screen = Screen(None)      # main() thay bằng màn hình curses thật


def table(headers, rows):
    """Dựng bảng các cột đều nhau, trả về danh sách dòng đã căn."""
    if not rows:
        return ["(chưa có dữ liệu)"]
    # Độ rộng cột = max(tên cột, giá trị dài nhất trong cột đó).
    w = [max([len(str(h))] + [len(str(r[i])) for r in rows])
         for i, h in enumerate(headers)]
    return (["  ".join(str(h).ljust(x) for h, x in zip(headers, w)),
             "  ".join("-" * x for x in w)]
            + ["  ".join(str(c).ljust(x) for c, x in zip(r, w)) for r in rows])


def add_student(students):
    """Mã SV trùng bị chặn: mã là khoá tra cứu điểm, trùng thì ghi đè."""
    sid = ask("Mã SV: (ví dụ 203120) ",
              lambda s: is_number(s) and s not in {x.sid for x in students},
              "Mã SV phải là chữ số và không được trùng.")
    students.append(Student(
        sid,
        ask("Họ tên: (ví dụ tom) ", is_name, "Tên phải có chữ cái."),
        ask("Ngày sinh: (ví dụ 24/1/2002) ", is_dob,
            "Ngày sinh phải có dạng d/m/y và là ngày có thật.")))


def add_course(courses):
    """Mã môn trùng bị chặn: mã môn là khoá tra cứu số tín chỉ."""
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
    """Chọn một môn rồi nhập điểm cho mọi sinh viên. Điểm được floor1 ngay."""
    cid = ask("Nhập điểm môn nào? (mã môn) ",
              lambda s: s in courses, "Môn học không tồn tại.")
    for s in students:
        s.set_mark(cid, float(ask(f"Điểm {s.name} ({s.sid}): (0-10, ví dụ 8.53 -> 8.5) ",
                                  is_mark, "Điểm từ 0 đến 10, thử lại.")))
    for r in table(["Mã SV", "Họ tên", "Điểm"],
                   [[s.sid, s.name, s.marks[cid]] for s in students]):
        screen.line(r)


def show_gpa(students, courses):
    """In sinh viên xếp hạng theo GPA giảm dần."""
    screen.line()
    for r in table(["Mã SV", "Họ tên", "GPA"],
                   [[s.sid, s.name, f"{s.gpa(courses):.2f}"]
                    for s in sort_by_gpa(students, courses)]):
        screen.line(r)


# ==================================================================
# CHƯƠNG TRÌNH CHÍNH
# ==================================================================

MENU = """
  1. Thêm sinh viên        4. Xếp hạng theo GPA
  2. Thêm môn học          5. Xem sinh viên
  3. Nhập điểm             0. Thoát
"""


def run(stdscr):
    global screen
    screen = Screen(stdscr)

    students, courses = [], {}            # list[Student] và {mã môn: Course}
    try:
        while True:
            screen.clear()                # xóa để menu không đè lên bảng đã hiện
            screen.title("QUẢN LÝ ĐIỂM SINH VIÊN")
            screen.line(MENU)

            c = screen.ask("Chọn: ")
            if c == "0":
                return
            elif c == "1":
                add_student(students)
            elif c == "2":
                add_course(courses)
            elif c == "3" or c == "4":
                if students and courses:
                    (enter_marks if c == "3" else show_gpa)(students, courses)
                else:
                    screen.line("Cần có sinh viên và môn học trước.")
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
        run(None)                           # không có terminal thì in thường
    else:
        # wrapper tự gọi initscr + noecho + cbreak, và endwin() khi thoát.
        curses.wrapper(run)


# ==================================================================
# TỰ KIỂM TRA
# ==================================================================

def _test():
    # Chạy: python "3.student.mark.oop.math.py" --test
    # Làm tròn xuống 1 chữ số, kể cả lỗi số thực 7.3*10 = 72.999...
    assert [floor1(x) for x in (8.53, 7.29, 7.3, 9.0, 0.04)] == [8.5, 7.2, 7.3, 9.0, 0.0]
    assert is_mark("8.53") and not is_mark("11") and not is_mark("tom")
    assert is_dob("24/1/2002") and not is_dob("30/2/2002")   # tháng 2 không có ngày 30

    cs = {"234": Course("234", "Đại số tuyến tính", 3),
          "235": Course("235", "Python", 4)}

    s = Student("1", "tom", "24/1/2002")
    assert s.gpa(cs) == 0.0                 # chưa có điểm -> 0, không chia cho 0
    s.set_mark("234", 9.0)
    s.set_mark("235", 8.0)
    assert abs(s.gpa(cs) - 59 / 7) < 1e-9  # (3*9 + 4*8) / 7

    # Hai SV có tổng điểm thường bằng nhau nhưng trọng số khác nên GPA khác:
    #   v: (3*9  + 4*10) / 7 = 9.57        w: (3*10 + 4*9 ) / 7 = 9.43
    v, w = Student("v", "v", "1/1/2000"), Student("w", "w", "1/1/2000")
    v.set_mark("234", 9.0), v.set_mark("235", 10.0)
    w.set_mark("234", 10.0), w.set_mark("235", 9.0)
    assert sort_by_gpa([w, v], cs) == [v, w]

    # Nhập 8.53 phải lưu thành 8.5
    s.marks.clear()
    s.set_mark("234", 8.53)
    assert s.marks["234"] == 8.5

    print("OK: làm tròn, kiểm tra dữ liệu, GPA có trọng số, xếp hạng")


if __name__ == "__main__":
    _test() if "--test" in sys.argv else main()
