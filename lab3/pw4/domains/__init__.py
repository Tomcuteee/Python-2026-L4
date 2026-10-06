"""
domains/__init__.py - GỐC CỦA PACKAGE `domains`

Dòng import này cho phép gói khác viết:
    from domains import Course, Student, sort_by_gpa
thay vì phải nhớ đường dẫn đầy đủ tới từng file.
"""

from .course import Course
from .mark import floor1
from .student import Student, sort_by_gpa

__all__ = ["Course", "Student", "floor1", "sort_by_gpa"]
