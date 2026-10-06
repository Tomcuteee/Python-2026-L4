# output.py - vẽ giao diện: bọc curses, có curses thì vẽ, không thì in thường.

from domains import sort_by_gpa

try:
    import curses
except ImportError:
    curses = None


def _cursor(visible):
    if curses is None:
        return
    try:
        curses.curs_set(1 if visible else 0)
    except curses.error:
        pass                            # nhiều terminal không hỗ trợ curs_set()


class Screen:
    # win=None nghĩa là in ra màn hình bình thường.

    def __init__(self, win):
        self.w = win
        self.row = 1                   # dòng 0 dành cho tiêu đề

    def clear(self):
        self.row = 1
        if self.w:
            self.w.erase()

    def line(self, text=""):
        # curses không tự cuộn màn hình nên phải tự tăng `row`;
        # dòng cuối (h-1) dành cho câu hỏi nhập.
        if not self.w:
            print(text)
            return
        h, w = self.w.getmaxyx()
        for part in str(text).split("\n"):
            if self.row >= h - 1:
                break
            self.w.addstr(self.row, 0, part[:w - 1])   # cắt w-1: chạm cột cuối sẽ vượt biên
            self.w.clrtoeol()                          # xóa phần còn sót của dòng
            self.row += 1
        self.w.refresh()

    def title(self, text):
        if not self.w:
            print(text)
            return
        _, w = self.w.getmaxyx()
        self.w.addstr(0, 0, text.center(w - 1), curses.A_BOLD)

    def ask(self, prompt):
        # getstr() chứ không curses.instr(): windows-curses không có instr()
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
            curses.noecho()             # finally để Ctrl+C cũng trả
            _cursor(0)


screen = Screen(None)                  # main.py thay bằng màn hình curses thật


def table(headers, rows):
    # Bảng các cột đều nhau. Rộng cột = max(tên cột, giá trị dài nhất).
    if not rows:
        return ["(chưa có dữ liệu)"]
    w = [max([len(str(h))] + [len(str(r[i])) for r in rows])
         for i, h in enumerate(headers)]
    return (["  ".join(str(h).ljust(x) for h, x in zip(headers, w)),
             "  ".join("-" * x for x in w)]
            + ["  ".join(str(c).ljust(x) for c, x in zip(r, w)) for r in rows])


def show_students(students):
    for r in table(["Mã SV", "Họ tên", "Ngày sinh"],
                   [[s.sid, s.name, s.dob] for s in students]):
        screen.line(r)


def show_gpa(students, courses):
    screen.line()
    for r in table(["Mã SV", "Họ tên", "GPA"],
                   [[s.sid, s.name, f"{s.gpa(courses):.2f}"]
                    for s in sort_by_gpa(students, courses)]):
        screen.line(r)


def show_marks(students, cid):
    for r in table(["Mã SV", "Họ tên", "Điểm"],
                   [[s.sid, s.name, s.marks[cid]] for s in students]):
        screen.line(r)
