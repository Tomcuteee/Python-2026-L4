# Vẽ giao diện: có curses thì vẽ trên màn hình, không thì in thường.

from domains import sort_by_gpa

try:
    import curses
except ImportError:
    curses = None


def _cursor(visible):
    try:
        curses.curs_set(1 if visible else 0)
    except curses.error:
        pass                            # terminal này không đổi được con trỏ


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


screen = Screen(None)                  # main.py thay bằng màn hình curses thật


def table(headers, rows):
    # Bảng căn cột, trả về danh sách dòng chuỗi
    if not rows:
        return ["(chưa có dữ liệu)"]
    w = [max([len(str(h))] + [len(str(r[i])) for r in rows])
         for i, h in enumerate(headers)]
    return (["  ".join(str(h).ljust(x) for h, x in zip(headers, w)),
             "  ".join("-" * x for x in w)]
            + ["  ".join(str(c).ljust(x) for c, x in zip(r, w)) for r in rows])


def show_students(students):
    # Bảng sinh viên kèm ngày sinh
    for r in table(["Mã SV", "Họ tên", "Ngày sinh"],
                   [[s.sid, s.name, s.dob] for s in students]):
        screen.line(r)


def show_gpa(students, courses):
    # Bảng sinh viên xếp hạng theo GPA
    screen.line()
    for r in table(["Mã SV", "Họ tên", "GPA"],
                   [[s.sid, s.name, f"{s.gpa(courses):.2f}"]
                    for s in sort_by_gpa(students, courses)]):
        screen.line(r)


def show_marks(students, cid):
    # Bảng điểm một môn
    for r in table(["Mã SV", "Họ tên", "Điểm"],
                   [[s.sid, s.name, s.marks[cid]] for s in students]):
        screen.line(r)
