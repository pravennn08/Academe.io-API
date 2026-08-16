from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_number",
        "full_name",
        "email",
        "sex",
        "date_of_birth",
        "created_at",
    )

    search_fields = (
        "student_number",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    list_filter = (
        "sex",
        "blood_type",
        "created_at",
    )

    autocomplete_fields = ("user",)
    list_select_related = ("user",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    @admin.display(
        description="Name",
        ordering="user__first_name",
    )
    def full_name(self, student: Student) -> str:
        return student.user.get_full_name()

    @admin.display(
        description="Email",
        ordering="user__email",
    )
    def email(self, student: Student) -> str:
        return student.user.email
