# main.py - vòng lặp menu, nối input.py (nhập) với output.py (hiển thị).
# Chạy:  python main.py [--test]

import sys

import input as ui                                  # module trùng tên hàm input() của Python
import output as view
import storage
from domains import sort_by_gpa

try:
    sys.stdout.reconfigure(encoding="utf-8")        # console Windows là cp1252
except (AttributeError, ValueError):
    pass


MENU = """
  1. Thêm sinh viên        4. Xếp hạng theo GPA
  2. Thêm môn học          5. Xem sinh viên
  3. Nhập điểm             0. Thoát (lưu vào students.dat)
"""

EMPTY = "Cần có sinh viên và môn học trước."


def run(stdscr):
    view.screen = view.Screen(stdscr)
    ui.screen = view.screen                        # input.py đọc qua cùng con trỏ

    students, courses = storage.load()
    if students or courses:
        view.screen.line(f"Đã nạp {len(students)} sinh viên và "
                         f"{len(courses)} môn học từ students.dat.\n")
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
    finally:
        storage.save(students, courses)             # Ctrl+C hay chọn 0 đều lưu
        view.screen.line("Đã lưu vào students.dat.")


def main():
    if view.curses is None or not sys.stdout.isatty():
        run(None)                                   # không có terminal thì in thường
    else:
        view.curses.wrapper(run)                   # tự gọi initscr và endwin()


def _test():
    # Chạy: python main.py --test
    import os
    import shutil
    import tempfile
    from domains import Course, Student, floor1

    assert [floor1(x) for x in (8.53, 7.29, 7.3, 9.0, 0.04)] == [8.5, 7.2, 7.3, 9.0, 0.0]
    assert ui.is_mark("8.53") and not ui.is_mark("11") and not ui.is_mark("tom")
    assert ui.is_dob("24/1/2002") and not ui.is_dob("30/2/2002")

    cs = {"234": Course("234", "Đại số tuyến tính", 3),
          "235": Course("235", "Python", 4)}

    s = Student("1", "tom", "24/1/2002")
    assert s.gpa(cs) == 0.0                         # chưa có điểm -> 0
    s.set_mark("234", 9.0)
    s.set_mark("235", 8.0)
    assert abs(s.gpa(cs) - 59 / 7) < 1e-9          # (3*9 + 4*8) / 7

    # Tổng điểm bằng nhau nhưng trọng số khác nên GPA khác:
    #   v: (3*9  + 4*10) / 7 = 9.57        w: (3*10 + 4*9 ) / 7 = 9.43
    v, w = Student("v", "v", "1/1/2000"), Student("w", "w", "1/1/2000")
    v.set_mark("234", 9.0), v.set_mark("235", 10.0)
    w.set_mark("234", 10.0), w.set_mark("235", 9.0)
    assert sort_by_gpa([w, v], cs) == [v, w]

    s.marks.clear()
    s.set_mark("234", 8.53)
    assert s.marks["234"] == 8.5                    # nhập 8.53 -> lưu 8.5

    # pw5: lưu rồi nạp lại phải ra đúng dữ liệu cũ
    saved, tmp = (storage.DIR, storage.DAT), tempfile.mkdtemp()
    storage.DIR, storage.DAT = tmp, os.path.join(tmp, "students.dat")
    try:
        assert storage.load() == ([], {})            # chưa có .dat thì rỗng
        storage.save([s, v], cs)
        for name in storage.FILES:
            assert os.path.exists(os.path.join(tmp, name)), name
        s2, cs2 = storage.load()
        assert [(x.sid, x.name, x.dob) for x in s2] == \
               [("1", "tom", "24/1/2002"), ("v", "v", "1/1/2000")]
        assert {k: (c.name, c.credits) for k, c in cs2.items()} == \
               {k: (c.name, c.credits) for k, c in cs.items()}
        assert s2[0].marks == s.marks
        assert abs(s2[0].gpa(cs2) - s.gpa(cs)) < 1e-9
    finally:
        storage.DIR, storage.DAT = saved
        shutil.rmtree(tmp, ignore_errors=True)

    print("OK: nhập, GPA, xếp hạng, lưu/nạp students.dat")


if __name__ == "__main__":
    _test() if "--test" in sys.argv else main()
