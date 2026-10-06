"""
output.py - MODULE HIỂN THỊ (curses)

Đề bài: "output.py: module for curses output".

Giữ đúng 1 màn hình curses cho toàn chương trình. input.py cũng đọc chuỗi
qua `screen.ask()` — dùng chung một con trỏ nên không bị nhấp nháy và không
phải lúc nào cũng phải bật/tắt echo.

Nếu máy không cài curses (Windows: pip install windows-curses) hoặc không
chạy trong terminal thì `Screen(None)` in ra màn hình bình thường — chương
trình vẫn chạy được.
"""

from domains import sort_by_gpa

try:
    import curses
except ImportError:
    curses = None                     # không có curses thì chạy bản in thường


def _cursor(visible):
    """Hiện/ẩn con trỏ. Nhiều terminal không hỗ trợ curs_set() và báo lỗi,
    nhưng việc này không quan trọng nên bỏ qua lỗi."""
    if curses is None:
        return
    try:
        curses.curs_set(1 if visible else 0)
    except curses.error:
        pass


class Screen:
    """
    Bọc curses. Truyền None thì mọi lệnh vẽ in ra màn hình bình thường,
    nên chương trình vẫn chạy được trên máy không cài curses.
    """

    def __init__(self, win):
        self.w = win
        self.row = 1                      # dòng 0 dành cho tiêu đề

    def clear(self):
        self.row = 1
        if self.w:
            self.w.erase()

    def line(self, text=""):
        """
        In nội dung xuống dòng kế tiếp. Chuỗi có \n thì in nhiều dòng.

        Cần bộ đếm `row` vì curses KHÔNG tự cuộn màn hình: cứ in vào dòng
        cuối thì dòng mới sẽ đè dòng cũ, bảng nhiều dòng chỉ còn lại dòng
        cuối cùng.
        """
        if not self.w:
            print(text)
            return
        h, w = self.w.getmaxyx()
        for part in str(text).split("\n"):
            if self.row >= h - 1:         # dòng cuối dành cho câu hỏi nhập
                break
            self.w.addstr(self.row, 0, part[:w - 1])    # cắt w-1: chạm cột cuối sẽ vượt biên
            self.w.clrtoeol()                            # xóa phần còn sót của dòng
            self.row += 1
        self.w.refresh()

    def title(self, text):
        if not self.w:
            print(text)
            return
        _, w = self.w.getmaxyx()
        self.w.addstr(0, 0, text.center(w - 1), curses.A_BOLD)

    def ask(self, prompt):
        """
        Câu hỏi ở dòng cuối, trả về chuỗi đã bỏ khoảng trắng thừa.

        Dùng window.getstr() chứ không dùng curses.instr(): bản
        windows-curses không có instr(). getstr() chỉ đọc được khi
        chế độ echo đang bật.
        """
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


# Màn hình toàn cục: main.py thay bằng màn hình curses thật khi có terminal.
screen = Screen(None)


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


def show_students(students):
    """In danh sách sinh viên kèm ngày sinh."""
    for r in table(["Mã SV", "Họ tên", "Ngày sinh"],
                   [[s.sid, s.name, s.dob] for s in students]):
        screen.line(r)


def show_gpa(students, courses):
    """In sinh viên xếp hạng theo GPA giảm dần."""
    screen.line()
    for r in table(["Mã SV", "Họ tên", "GPA"],
                   [[s.sid, s.name, f"{s.gpa(courses):.2f}"]
                    for s in sort_by_gpa(students, courses)]):
        screen.line(r)


def show_marks(students, cid):
    """In điểm một môn vừa nhập xong."""
    for r in table(["Mã SV", "Họ tên", "Điểm"],
                   [[s.sid, s.name, s.marks[cid]] for s in students]):
        screen.line(r)
