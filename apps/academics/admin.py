from django.contrib import admin

from .models import (AcademicYear, Assignment, Attendance, Enrollment, Exam,
                     Grade, Lesson, Result, SchoolClass, Subject)

admin.site.register(
    [
        Grade,
        AcademicYear,
        SchoolClass,
        Subject,
        Lesson,
        Enrollment,
        Exam,
        Assignment,
        Result,
        Attendance,
    ],
)
