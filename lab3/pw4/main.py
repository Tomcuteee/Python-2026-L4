# main.py - vòng lặp menu, gọi input.py để nhập và output.py để in.
# Chạy:  python main.py [--test]

import sys

import input as ui                                  # đặt tên khác input, tên module trùng hàm input()
import output as view
from domains import sort_by_gpa

try:
    sys.stdout.reconfigure(encoding="utf-8")        # console Windows là cp1252
except (AttributeError, ValueError):
    pass


MENU = """
  1. Thêm sinh viên        4. Xếp hạng theo GPA
  2. Thêm môn học          5. Xem sinh viên
  3. Nhập điểm             0. Thoát
"""

EMPTY = "Cần có sinh viên và môn học trước."


def run(stdscr):
    view.screen = view.Screen(stdscr)
    ui.screen = view.screen                        # input.py dùng chung màn hình

    students, courses = [], {}                     # list[Student] và {mã môn: Course}
    try:
        while True:
            view.screen.clear()
            view.screen.title("QUẢN LÝ ĐIỂM SINH VIÊN")
            view.screen.line(MENU)

            c = view.screen.ask("Chọn: ")
            if c == "0":
                return
            elif c == "1":
                ui.add_students(students, ui.ask_count("Nhập bao nhiêu sinh viên?"))
            elif c == "2":
                ui.add_course(courses)
            elif c == "3":
                if students and courses:
                    view.show_marks(students, ui.enter_marks(students, courses))
                else:
                    view.screen.line(EMPTY)
            elif c == "4":
                if students and courses:
                    view.show_gpa(students, courses)
                else:
                    view.screen.line(EMPTY)
            elif c == "5":
                view.show_students(students)
            else:
                view.screen.line("Lựa chọn không hợp lệ, thử lại.")
    except (KeyboardInterrupt, EOFError):
        view.screen.line("\nKết thúc.")


def main():
    if view.curses is None or not sys.stdout.isatty():
        run(None)                                   # không có terminal thì in thường
    else:
        view.curses.wrapper(run)                   # tự gọi initscr và endwin()


def _test():
    # Chạy: python main.py --test
    from domains import Course, Student, floor1

    assert [floor1(x) for x in (8.53, 7.29, 7.3, 9.0, 0.04)] == [8.5, 7.2, 7.3, 9.0, 0.0]
    assert ui.is_mark("8.53") and not ui.is_mark("11") and not ui.is_mark("tom")
    assert ui.is_dob("24/1/2002") and not ui.is_dob("30/2/2002")

    cs = {"234": Course("234", "Đại số tuyến tính", 3),
          "235": Course("235", "Python", 4)}

    s = Student("1", "tom", "24/1/2002")
    assert s.gpa(cs) == 0.0
    s.set_mark("234", 9.0)
    s.set_mark("235", 8.0)
    assert abs(s.gpa(cs) - 59 / 7) < 1e-9

    # Tổng điểm bằng nhau nhưng trọng số khác nên GPA khác:
    #   v: (3*9  + 4*10) / 7 = 9.57        w: (3*10 + 4*9 ) / 7 = 9.43
    v, w = Student("v", "v", "1/1/2000"), Student("w", "w", "1/1/2000")
    v.set_mark("234", 9.0), v.set_mark("235", 10.0)
    w.set_mark("234", 10.0), w.set_mark("235", 9.0)
    assert sort_by_gpa([w, v], cs) == [v, w]

    s.marks.clear()
    s.set_mark("234", 8.53)
    assert s.marks["234"] == 8.5

    print("OK: nhập, GPA, xếp hạng")


if __name__ == "__main__":
    _test() if "--test" in sys.argv else main()
