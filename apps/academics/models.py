from django.core.validators import MinValueValidator
from django.db import models

from apps.core.models import UUIDTimeStampedModel


class Day(models.TextChoices):
    MONDAY = "MONDAY", "Monday"
    TUESDAY = "TUESDAY", "Tuesday"
    WEDNESDAY = "WEDNESDAY", "Wednesday"
    THURSDAY = "THURSDAY", "Thursday"
    FRIDAY = "FRIDAY", "Friday"


class Grade(UUIDTimeStampedModel):
    level = models.PositiveSmallIntegerField(
        unique=True,
        validators=[MinValueValidator(1)],
    )

    class Meta:
        ordering = ("level",)

    def __str__(self) -> str:
        return f"Grade {self.level}"


class AcademicYear(UUIDTimeStampedModel):
    name = models.CharField(
        max_length=20,
        unique=True,
    )

    start_date = models.DateField()
    end_date = models.DateField()

    is_active = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = ("-start_date",)

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    start_date__lt=models.F("end_date"),
                ),
                name="academic_year_start_before_end",
            ),
        ]

    def __str__(self) -> str:
        return self.name


class SchoolClass(UUIDTimeStampedModel):
    name = models.CharField(
        max_length=100,
    )

    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
    )

    supervisor = models.ForeignKey(
        "teachers.Teacher",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="supervised_classes",
    )

    grade = models.ForeignKey(
        Grade,
        on_delete=models.PROTECT,
        related_name="classes",
    )

    students = models.ManyToManyField(
        "students.Student",
        through="Enrollment",
        related_name="school_classes",
        blank=True,
    )

    class Meta:
        ordering = ("grade__level", "name")

        constraints = [
            models.UniqueConstraint(
                fields=("grade", "name"),
                name="unique_class_name_per_grade",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.grade} — {self.name}"


class Subject(UUIDTimeStampedModel):
    name = models.CharField(
        max_length=100,
        unique=True,
    )

    teachers = models.ManyToManyField(
        "teachers.Teacher",
        related_name="subjects",
        blank=True,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Lesson(UUIDTimeStampedModel):
    name = models.CharField(
        max_length=150,
    )

    day = models.CharField(
        max_length=10,
        choices=Day.choices,
    )

    start_time = models.TimeField()
    end_time = models.TimeField()

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="lessons",
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.PROTECT,
        related_name="lessons",
    )

    teacher = models.ForeignKey(
        "teachers.Teacher",
        on_delete=models.PROTECT,
        related_name="lessons",
    )

    class Meta:
        ordering = ("day", "start_time")

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    start_time__lt=models.F("end_time"),
                ),
                name="lesson_start_before_end",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} — {self.school_class}"


class Enrollment(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        ENROLLED = "ENROLLED", "Enrolled"
        COMPLETED = "COMPLETED", "Completed"
        WITHDRAWN = "WITHDRAWN", "Withdrawn"

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    school_class = models.ForeignKey(
        SchoolClass,
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="enrollments",
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ENROLLED,
    )

    class Meta:
        ordering = ("-academic_year__start_date",)

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "student",
                    "school_class",
                    "academic_year",
                ),
                name="unique_student_class_enrollment",
            ),
            models.UniqueConstraint(
                fields=(
                    "student",
                    "academic_year",
                ),
                condition=models.Q(status="ENROLLED"),
                name="unique_active_enrollment_per_year",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.student} — {self.school_class} " f"({self.academic_year})"


class Exam(UUIDTimeStampedModel):
    title = models.CharField(
        max_length=150,
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.PROTECT,
        related_name="exams",
    )

    class Meta:
        ordering = ("start_time",)

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    start_time__lt=models.F("end_time"),
                ),
                name="exam_start_before_end",
            ),
        ]

    def __str__(self) -> str:
        return self.title


class Assignment(UUIDTimeStampedModel):
    title = models.CharField(
        max_length=150,
    )

    start_date = models.DateTimeField()
    due_date = models.DateTimeField()

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.PROTECT,
        related_name="assignments",
    )

    class Meta:
        ordering = ("due_date",)

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    start_date__lt=models.F("due_date"),
                ),
                name="assignment_start_before_due",
            ),
        ]

    def __str__(self) -> str:
        return self.title


class Result(UUIDTimeStampedModel):
    score = models.PositiveIntegerField()

    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="results",
    )

    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="results",
    )

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="results",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(
                        exam__isnull=False,
                        assignment__isnull=True,
                    )
                    | models.Q(
                        exam__isnull=True,
                        assignment__isnull=False,
                    )
                ),
                name="result_has_exactly_one_assessment",
            ),
            models.UniqueConstraint(
                fields=("student", "exam"),
                condition=models.Q(exam__isnull=False),
                name="unique_student_exam_result",
            ),
            models.UniqueConstraint(
                fields=("student", "assignment"),
                condition=models.Q(assignment__isnull=False),
                name="unique_student_assignment_result",
            ),
        ]

    def __str__(self) -> str:
        assessment = self.exam or self.assignment
        return f"{self.student} — {assessment}: {self.score}"


class Attendance(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        PRESENT = "PRESENT", "Present"
        ABSENT = "ABSENT", "Absent"
        LATE = "LATE", "Late"
        EXCUSED = "EXCUSED", "Excused"

    date = models.DateField()

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PRESENT,
    )

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.PROTECT,
        related_name="attendances",
    )

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.PROTECT,
        related_name="attendances",
    )

    class Meta:
        ordering = ("-date",)

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "student",
                    "lesson",
                    "date",
                ),
                name="unique_student_lesson_attendance",
            ),
        ]

    def __str__(self) -> str:
        return (
            f"{self.student} — {self.lesson} "
            f"({self.date}): {self.get_status_display()}"
        )
