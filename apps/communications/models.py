from django.conf import settings
from django.db import models

from apps.core.models import UUIDTimeStampedModel


class Event(UUIDTimeStampedModel):
    title = models.CharField(
        max_length=200,
    )

    description = models.TextField()

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    school_class = models.ForeignKey(
        "academics.SchoolClass",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="events",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_events",
    )

    class Meta:
        ordering = ("start_time",)

        constraints = [
            models.CheckConstraint(
                condition=models.Q(
                    start_time__lt=models.F("end_time"),
                ),
                name="event_start_before_end",
            ),
        ]

    def __str__(self) -> str:
        return self.title


class Announcement(UUIDTimeStampedModel):
    title = models.CharField(
        max_length=200,
    )

    description = models.TextField()

    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    school_class = models.ForeignKey(
        "academics.SchoolClass",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="announcements",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_announcements",
    )

    class Meta:
        ordering = ("-published_at", "-created_at")

    def __str__(self) -> str:
        return self.title
