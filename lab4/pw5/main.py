# main.py - SCRIPT ĐIỀU PHỐI
# Chỉ lo vòng lặp menu và nối input.py với output.py, không viết logic nhập
# hay logic vẽ. Đó là điểm của việc tách module: đổi cách hiển thị không phải
# sửa lại phần nghiệp vụ.
# Chạy:  python main.py [--test]

import sys

import input as ui                                  # tên module trùng với hàm input() của Python
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


def run(stdscr):
    view.screen = view.Screen(stdscr)
    ui.screen = view.screen                          # input.py đọc qua cùng con trỏ

    students, courses = storage.load()              # nạp dữ liệu cũ nếu có students.dat
    if students or courses:
        view.screen.line(f"Đã nạp {len(students)} sinh viên và "
                         f"{len(courses)} môn học từ students.dat.\n")
    try:
        while True:
            view.screen.clear()                      # xóa để menu không đè lên bảng đã hiện
            view.screen.title("QUẢN LÝ ĐIỂM SINH VIÊN")
            view.screen.line(MENU)

            c = view.screen.ask("Chọn: ")
            if c == "0":
                return                              # thoát -> finally sẽ lưu
            elif c == "1":
                # Hỏi số lượng trước rồi mới nhập từng người, thay vì bắt
                # người dùng gõ "0" để kết thúc.
                n = ui.ask_count("Nhập bao nhiêu sinh viên?")
                ui.add_students(students, n)
            elif c == "2":
                ui.add_course(courses)
            elif c == "3":
                # Cần cả hai thì mới tính được: không có SV hoặc không có môn
                if students and courses:
                    view.show_marks(students, ui.enter_marks(students, courses))
                else:
                    view.screen.line("Cần có sinh viên và môn học trước.")
            elif c == "4":
                if students and courses:
                    view.show_gpa(students, courses)
                else:
                    view.screen.line("Cần có sinh viên và môn học trước.")
            elif c == "5":
                view.show_students(students)
            else:
                view.screen.line("Lựa chọn không hợp lệ, thử lại.")
    except (KeyboardInterrupt, EOFError):
        view.screen.line("\nKết thúc.")
    finally:
        # finally: Ctrl+C hay chọn 0 đều lưu được, không mất dữ liệu đã nhập.
        storage.save(students, courses)
        view.screen.line("Đã lưu vào students.dat.")


def main():
    if view.curses is None or not sys.stdout.isatty():
        run(None)                                   # không có terminal thì in thường
    else:
        # wrapper tự gọi initscr + noecho + cbreak, và endwin() khi thoát.
        view.curses.wrapper(run)


# ==================================================================
# TỰ KIỂM TRA
# ==================================================================

def _test():
    # Chạy: python main.py --test
    from domains import Course, Student, floor1

    # Làm tròn xuống 1 chữ số, kể cả lỗi số thực 7.3*10 = 72.999...
    assert [floor1(x) for x in (8.53, 7.29, 7.3, 9.0, 0.04)] == [8.5, 7.2, 7.3, 9.0, 0.0]
    assert ui.is_mark("8.53") and not ui.is_mark("11") and not ui.is_mark("tom")
    assert ui.is_dob("24/1/2002") and not ui.is_dob("30/2/2002")   # tháng 2 không có ngày 30

    cs = {"234": Course("234", "Đại số tuyến tính", 3),
          "235": Course("235", "Python", 4)}

    s = Student("1", "tom", "24/1/2002")
    assert s.gpa(cs) == 0.0                         # chưa có điểm -> 0, không chia cho 0
    s.set_mark("234", 9.0)
    s.set_mark("235", 8.0)
    assert abs(s.gpa(cs) - 59 / 7) < 1e-9          # (3*9 + 4*8) / 7

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

    # pw5: lưu rồi nạp lại phải ra đúng dữ liệu cũ
    import os
    import shutil
    import tempfile
    saved, tmp = (storage.DIR, storage.DAT), tempfile.mkdtemp()
    storage.DIR, storage.DAT = tmp, os.path.join(tmp, "students.dat")
    try:
        assert storage.load() == ([], {})            # chưa có .dat thì rỗng
        storage.save([s, v], cs)
        for name in storage.FILES:                  # đề yêu cầu ghi 3 file txt
            assert os.path.exists(os.path.join(tmp, name)), name
        s2, cs2 = storage.load()
        assert [x.sid for x in s2] == ["1", "v"]
        assert [(x.name, x.dob) for x in s2] == [(s.name, s.dob), ("v", "1/1/2000")]
        assert {k: (c.name, c.credits) for k, c in cs2.items()} == \
               {k: (c.name, c.credits) for k, c in cs.items()}
        assert s2[0].marks == s.marks                # điểm giữ nguyên qua .dat
        assert abs(s2[0].gpa(cs2) - s.gpa(cs)) < 1e-9
    finally:
        storage.DIR, storage.DAT = saved             # trở lại đường dẫn thật
        shutil.rmtree(tmp, ignore_errors=True)       # dọn file test vừa sinh

    print("OK: 3 module import được, làm tròn, kiểm tra dữ liệu, GPA, xếp hạng, "
          "lưu/nạp students.dat")


if __name__ == "__main__":
    _test() if "--test" in sys.argv else main()
