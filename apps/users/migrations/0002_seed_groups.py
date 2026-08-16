from django.db import migrations

GROUP_NAMES = [
    "Administrator",
    "Teacher",
    "Student",
    "Parent",
]


def seed_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")

    for name in GROUP_NAMES:
        Group.objects.get_or_create(name=name)


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            seed_groups,
            migrations.RunPython.noop,
        ),
    ]
