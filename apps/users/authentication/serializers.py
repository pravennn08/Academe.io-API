from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class AuthUserSerializer(serializers.ModelSerializer):
    roles = serializers.SlugRelatedField(
        source="groups",
        many=True,
        read_only=True,
        slug_field="name",
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "is_active",
            "is_staff",
            "is_superuser",
            "roles",
        ]
        read_only_fields = fields
