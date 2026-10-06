# Gốc package `domains`: gom các lớp ra để gói khác chỉ cần
# from domains import Course, Student, sort_by_gpa


from .course import Course
from .mark import floor1
from .student import Student, sort_by_gpa

__all__ = ["Course", "Student", "floor1", "sort_by_gpa"]
