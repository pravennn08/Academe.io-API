from django.contrib import admin

from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "employee_number",
        "full_name",
        "email",
        "phone_number",
        "sex",
        "created_at",
    )

    search_fields = (
        "employee_number",
        "phone_number",
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
    def full_name(self, teacher: Teacher) -> str:
        return teacher.user.get_full_name()

    @admin.display(
        description="Email",
        ordering="user__email",
    )
    def email(self, teacher: Teacher) -> str:
        return teacher.user.email
