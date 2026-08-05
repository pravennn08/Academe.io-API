import uuid

from django.conf import settings
from django.db import models


class Parent(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="parent_profile",
    )

    phone_number = models.CharField(
        max_length=20,
        unique=True,
    )

    address = models.TextField()

    students = models.ManyToManyField(
        "students.Student",
        through="StudentParent",
        related_name="parents",
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("user__last_name", "user__first_name")

    def __str__(self) -> str:
        full_name = self.user.get_full_name().strip()
        return full_name or self.phone_number


class StudentParent(models.Model):
    class Relationship(models.TextChoices):
        MOTHER = "MOTHER", "Mother"
        FATHER = "FATHER", "Father"
        GUARDIAN = "GUARDIAN", "Legal guardian"
        OTHER = "OTHER", "Other"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    parent = models.ForeignKey(
        Parent,
        on_delete=models.CASCADE,
        related_name="student_links",
    )

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="parent_links",
    )

    relationship = models.CharField(
        max_length=10,
        choices=Relationship.choices,
    )

    is_primary_contact = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=("parent", "student"),
                name="unique_parent_student_relationship",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.parent} — " f"{self.student} ({self.get_relationship_display()})"
