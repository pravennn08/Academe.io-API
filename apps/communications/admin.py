from django.contrib import admin

from .models import Announcement, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "school_class",
        "start_time",
        "end_time",
        "created_by",
    )

    list_filter = (
        "school_class",
        "start_time",
    )

    search_fields = (
        "title",
        "description",
        "school_class__name",
    )

    list_select_related = (
        "school_class",
        "created_by",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "school_class",
        "published_at",
        "expires_at",
        "created_by",
    )

    list_filter = (
        "school_class",
        "published_at",
    )

    search_fields = (
        "title",
        "description",
        "school_class__name",
    )

    list_select_related = (
        "school_class",
        "created_by",
    )

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
