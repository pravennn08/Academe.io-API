from django.contrib import admin

from .models import Parent, StudentParent


class StudentParentInline(admin.TabularInline):
    model = StudentParent
    extra = 0
    autocomplete_fields = ("student",)


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "email",
        "phone_number",
        "created_at",
    )

    search_fields = (
        "phone_number",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    autocomplete_fields = ("user",)
    list_select_related = ("user",)

    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )

    inlines = (StudentParentInline,)

    @admin.display(
        description="Name",
        ordering="user__first_name",
    )
    def full_name(self, parent: Parent) -> str:
        return parent.user.get_full_name()

    @admin.display(
        description="Email",
        ordering="user__email",
    )
    def email(self, parent: Parent) -> str:
        return parent.user.email


@admin.register(StudentParent)
class StudentParentAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "parent",
        "relationship",
        "is_primary_contact",
    )

    list_filter = (
        "relationship",
        "is_primary_contact",
    )

    search_fields = (
        "student__student_number",
        "student__user__first_name",
        "student__user__last_name",
        "parent__user__first_name",
        "parent__user__last_name",
    )

    autocomplete_fields = (
        "student",
        "parent",
    )

    list_select_related = (
        "student__user",
        "parent__user",
    )
