import uuid
from django.conf import settings
from apps.core.choices import BloodType, Sex
from django.db import models


class Student(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    student_number = models.CharField(
        max_length=30,
        unique=True,
    )

    phone_number = models.CharField(
        max_length=20,
        blank=True,
    )

    address = models.TextField()

    image_url = models.URLField(
        blank=True,
    )

    blood_type = models.CharField(
        max_length=3,
        choices=BloodType.choices,
        blank=True,
    )

    sex = models.CharField(
        max_length=10,
        choices=Sex.choices,
    )

    date_of_birth = models.DateField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ("student_number",)

    def __str__(self) -> str:
        full_name = self.user.get_full_name().strip()
        return full_name or self.student_number
